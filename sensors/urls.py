from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from rest_framework.routers import DefaultRouter

from .views import MeasurementViewSet

router = DefaultRouter()
router.register(r'measurement', MeasurementViewSet)

urlpatterns = (
    url(r'api/v1.0/', include(router.urls)),
)
