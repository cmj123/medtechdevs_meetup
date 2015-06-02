from django.contrib import admin

from .models import *

class SequenceAdmin(admin.ModelAdmin):
    pass

class ParameterAdmin(admin.ModelAdmin):
    pass

class MeasurementAdmin(admin.ModelAdmin):
    pass

for i in [
    'Sequence', 
    'Parameter',
    'Measurement',
    ]:
    admin.site.register(globals()[i], globals()[i+'Admin'])

# Register your models here.


