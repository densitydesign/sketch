from django.contrib import admin
from models import SketchCollection, SketchCollectionPermission, SketchMapper


class SketchCollectionPermissionAdmin(admin.TabularInline):
    model = SketchCollectionPermission



class SketchCollectionAdmin(admin.ModelAdmin):
    model = SketchCollection
    inlines = [SketchCollectionPermissionAdmin]


admin.site.register(SketchCollection, SketchCollectionAdmin)
admin.site.register(SketchMapper)