from django.contrib import admin
from models import SketchCollection, SketchCollectionPermission, SketchMapper

admin.site.register(SketchCollection)
admin.site.register(SketchCollectionPermission)
admin.site.register(SketchMapper)