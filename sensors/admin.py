from django.contrib import admin

from .models import *

class SequenceAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'patient',
        )

class ParameterAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        )

class MeasurementAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'parameter',
        'sequence',
        'timestamp_start',
        'value',
        )

    list_filter = (
        'parameter',

        )

for i in [
    'Sequence', 
    'Parameter',
    'Measurement',
    ]:
    admin.site.register(globals()[i], globals()[i+'Admin'])

# Register your models here.


