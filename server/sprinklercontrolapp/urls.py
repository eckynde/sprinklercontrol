from django.urls import path
from .views import overview, settings, create_sprinkler, alter_sprinkler, delete_sprinkler, alter_weekly_timers, create_weekly_timers, CalendarView, weather, alter_irrigation_plan, create_irrigation_plan, delete_irrigation_plan, delete_weekly_timers, statistics, intervallSettings
from django.views.generic import TemplateView
from django.conf.urls import re_path
from sprinklercontrolapp import views

urlpatterns = [
    path("settings/", views.settings, name="settings"),
    path("", overview.as_view(), name="overview"),
    path("settings/create_sprinkler", create_sprinkler.as_view(), name="create_sprinkler"),
    path("settings/<int:id>_alter_sprinkler", alter_sprinkler.as_view(), name="alter_sprinkler"),
    path("settings/<int:id>_delete_sprinkler", delete_sprinkler.as_view(), name="delete_sprinkler"),
    path("calendar/", CalendarView, name="calendar"),
    path("settings/create_timer", create_weekly_timers.as_view(), name="create_timer"),
    path("settings/<int:id>_alter_timer", alter_weekly_timers.as_view(), name="alter_timer"),
    path("settings/<int:id>_delete_timer", delete_weekly_timers.as_view(), name="delete_timer"),
    path("settings/<int:id>_alter_irrigation_plan", alter_irrigation_plan.as_view(), name="alter_irrigation_plan"),
    path("settings/<int:id>_delete_irrigation_plan", delete_irrigation_plan.as_view(), name="delete_irrigation_plan"),
    path("settings/create_irrigation_plan", create_irrigation_plan.as_view(), name="create_irrigation_plan"),
    path("weather/", weather.as_view(), name="weather"),
    path("statistics/", statistics.as_view(), name="weather"),
    path("settings/timer_list", intervallSettings.as_view(), name="intervallSettings"),
    re_path(r'^api/sprinkler/(?P<pk>[0-9]+)/activate$', views.sprinkler_activate),
    re_path(r'^api/sprinkler/(?P<pk>[0-9]+)/deactivate$', views.sprinkler_deactivate),
    re_path(r'^api/sprinkler/(?P<pk>[0-9]+)/mode/(?P<mode>[a-z]+)$', views.sprinkler_mode),
    re_path(r'^api/update_city/(?P<city>(\w|,)+)$', views.update_city),
    re_path(r'^api/update_apikey/(?P<apikey>[0-9a-f]{32})$', views.update_apikey),
]
# api calls use regex with named capture groups which are passed as named args