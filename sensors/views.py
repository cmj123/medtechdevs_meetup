from django.shortcuts import render

from rest_framework import viewsets


from .serializers import MeasurementSerializer
from .models import Measurement


class MeasurementViewSet(viewsets.ModelViewSet):
    serializer_class = MeasurementSerializer
    queryset = Measurement.objects.all()

# Create your views here.
