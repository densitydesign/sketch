from django.db import models
from django.contrib.auth.models import User
from json_field import JSONField


SKETCH_ACCESS_LEVELS = ((1, 'read'), (2, 'write'))


class SketchPermission(models.Model):
    user = models.ForeignKey(User)
    access_level = models.IntegerField(choices = SKETCH_ACCESS_LEVELS)

    class Meta:
        abstract = True

class SketchCollectionPermission(SketchPermission):
    collection = models.ForeignKey('SketchCollection', related_name = "sketch_permissions")
    
    class Meta:
        unique_together = ['user', 'collection']
    
    

class SketchMapper(models.Model):
    name = models.CharField(max_length=200, unique=True)
    mapper = JSONField(null=False, blank=False)
    owner = models.ForeignKey(User)
    access = models.IntegerField(choices = SKETCH_ACCESS_LEVELS)    
    
    def clean(self):    
        from django.core.exceptions import ValidationError
        from mappermanager import mappingManager
        print "mpp", self.mapper, type(self.mapper)
        try:
            mappingManager.validateMapping(self.mapper)
        except Exception, e:
            raise ValidationError(str(e))
    
    
    def save(self, *args, **kwargs):
        
        super(SketchMapper, self).save(*args, **kwargs)
    
    
class SketchCollection(models.Model):
    name = models.CharField(max_length=200,)
    database = models.CharField(max_length=200,)
    owner = models.ForeignKey(User)
    access_level = models.IntegerField(choices = SKETCH_ACCESS_LEVELS, null=True, blank=True)
    
    class Meta:
        unique_together = ['name', 'database']
    
    def __unicode__(self):
        return u'%s' % self.name


    #helpers to get permissions
    
    def isOwner(self, user):

        return self.owner == user
    
    def getAccessLevelForUser(self, user):
         try:
            perm = self.sketch_permissions.get(user=user)
            return perm.access_level
         except:
            return None

    def hasWriteAccess(self, user):
        if self.isOwner(user):
            return True

        level = self.getAccessLevelForUser(user)
        if level:
            return level >= 2
            
        return False
    
    def hasReadAccess(self, user):
        if self.isOwner(user):
            return True
        level = self.getAccessLevelForUser(user)
        if level:
            return level >= 1
            
        return False
        
    #helpers for granting permissions to users

    def setAccessLevel(self, user, access_level):
        try:
            perm = self.sketch_permissions.get(user=user)
            perm.access_level = access_level
        except:
            perm = SketchCollectionPermission(collection=self, user=user, access_level=access_level)
 
        perm.save()
            
    def grantReadAccess(self, user):
        if not self.isOwner(user):
            self.setAccessLevel(user, 1)
       
    def revokeReadAccess(self, user):
        try:
            perm = self.sketch_permissions.get(user=user)
            perm.delete()
        except:
            pass


    def grantWriteAccess(self, user):
        if not self.isOwner(user):
            self.setAccessLevel(user, 2)

    def revokeWriteAccess(self, user):
        if self.hasWriteAccess(user):
            self.grantReadAccess(user)

        
        
        


