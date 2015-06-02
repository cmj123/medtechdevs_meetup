from django.db import models

# Create your models here.
class Sequence(models.Model):
    def __unicode__(self):
        return '%s:%d' % (self._meta.model_name, self.pk)

class Parameter(models.Model):
    name = models.CharField(max_length=64)
    def __unicode__(self):
        return self.name if self.name else '%s:%d' % (self._meta.model_name, self.pk)


class Measurement(models.Model):
    parameter = models.ForeignKey(Parameter)
    sequence  = models.ForeignKey(Sequence)

    created_at  = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    timestamp_start = models.DateTimeField()
    timestamp_end   = models.DateTimeField()

    value = models.DecimalField(max_digits=10, decimal_places=6) 
