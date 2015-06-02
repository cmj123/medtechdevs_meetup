from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register(r'measurement', MeasurementViewSet)
router.register(r'sequence',    SequenceViewSet)
router.register(r'parameter',   ParameterViewSet)

urlpatterns = (
    url(r'api/v1.0/', include(router.urls)),
)
