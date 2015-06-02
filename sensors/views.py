from django.shortcuts import render

from rest_framework import viewsets


from .serializers import *
from .models import *


class MeasurementViewSet(viewsets.ModelViewSet):
    serializer_class = MeasurementSerializer
    queryset = Measurement.objects.all()

class SequenceViewSet(viewsets.ModelViewSet):
    serializer_class = SequenceSerializer
    queryset = Sequence.objects.all()

class ParameterViewSet(viewsets.ModelViewSet):
    serializer_class = ParameterSerializer
    queryset = Parameter.objects.all()

# Create your views here.
