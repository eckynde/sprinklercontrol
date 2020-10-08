from django.urls import path
from .views import overview, settings, create_sprinkler, alter_sprinkler, delete_sprinkler, weekly_timers_list, alter_weekly_timers, create_weekly_timers, CalendarView, weather
from django.views.generic import TemplateView
from django.conf.urls import url
from sprinklercontrolapp import views

urlpatterns = [
    path("settings/", settings.as_view(), name="settings"),
    path("", overview.as_view(), name="overview"),
    path("settings/create_sprinkler", create_sprinkler.as_view(), name="create_sprinkler"),
    path("settings/<int:id>_alter_sprinkler", alter_sprinkler.as_view(), name="alter_sprinkler"),
    path("settings/<int:id>_delete_sprinkler", delete_sprinkler.as_view(), name="delete_sprinkler"),
    path("calendar/", CalendarView, name="calendar"),
    path("settings/create_timer", create_weekly_timers.as_view(), name="create_timer"),
    path("settings/<int:id>_alter_timer", alter_weekly_timers.as_view(), name="alter_timer"),
    path("weather/", weather.as_view(), name="weather"),
    url(r'^api/sprinklercontrolapp$', views.overview),
    url(r'^api/sprinklercontrolapp/(?P<pk>[0-9]+)$', views.overview),
]
