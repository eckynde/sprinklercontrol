from django.urls import path
from .views import overview, settings, statistics
from django.views.generic import TemplateView

urlpatterns = [
    path("", overview.as_view(), name="overview"),
    path("settings/", settings.as_view(), name="settings"),
    path("statistics/", statistics.as_view(), name="statistics")
]