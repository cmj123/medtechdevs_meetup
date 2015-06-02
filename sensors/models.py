from django.db import models

# Create your models here.
class Sequence(models.Model):
    pass 

class Parameter(models.Model):
    name = models.CharField(max_length=64)

class Measurement(models.Model):
    parameter = models.ForeignKey(Parameter)
    sequence  = models.ForeignKey(Sequence)

    created_at  = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    timestamp_start = models.DateTimeField()
    timestamp_end   = models.DateTimeField()

    value = models.DecimalField(max_digits=10, decimal_places=6) 
