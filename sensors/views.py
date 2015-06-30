from datetime import datetime
from django.shortcuts import render

from rest_framework import viewsets, filters
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
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

class MeasurementListByTimeView(ListAPIView):
    """
    Returns a list of measurements whose start timestamp is eariler than end_time and end timestamp is later than start_time.
    """
    serializer_class = MeasurementSerializer
    def get_queryset(self):
        format_str = "%Y%m%d%H%M%S"
        queryset = Measurement.objects.all()
        start_time_str = self.request.query_params.get('start_time', None)
        end_time_str = self.request.query_params.get('end_time', None)
        parameter_name = self.request.query_params.get('sensor_name', None)
        patient_id = self.request.query_params.get('patient_id', None)
        queryset = queryset.filter(parameter__name = parameter_name)
        queryset = queryset.filter(sequence__patient = patient_id)
        if start_time_str is not None and end_time_str is not None:
            start_time = datetime.strptime(start_time_str, format_str)
            end_time = datetime.strptime(end_time_str, format_str)
            print repr(start_time) + " " + repr(end_time)
            queryset = queryset.filter(timestamp_end__gt = start_time).filter(timestamp_start__lt = end_time)
            return queryset

