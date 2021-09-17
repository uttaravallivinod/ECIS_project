from django.contrib.gis.admin import OSMGeoAdmin
from django.contrib import admin
from .models import Whether

# Register your models here.
@admin.register(Whether)
class WhetherAdmin(OSMGeoAdmin):
    list_display=['location','date']
