from rest_framework import serializers

from .models import *

class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement

class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter

class SequenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sequence 


