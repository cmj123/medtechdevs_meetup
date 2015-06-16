from django.shortcuts import render

from rest_framework import viewsets
from rest_framework_bulk import (
    BulkListSerializer, 
    BulkSerializerMixin,
    ListBulkCreateUpdateDestroyAPIView, 
)


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

class MeasurementListView(ListBulkCreateUpdateDestroyAPIView):
    serializer_class = MeasurementSerializer
    queryset = Measurement.objects.all()


# Create your views here.
