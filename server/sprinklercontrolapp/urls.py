from django.urls import path
from .views import overview, settings, create_sprinkler, alter_sprinkler, delete_sprinkler, weekly_timers_list, alter_weekly_timers, create_weekly_timers, CalendarView, create_IrrigationPlan, alter_IrrigationPlan, delete_IrrigationPlan
from django.views.generic import TemplateView

urlpatterns = [
    path("settings/", settings.as_view(), name="settings"),
    path("", overview.as_view(), name="overview"),
    path("settings/create_sprinkler", create_sprinkler.as_view(), name="create_sprinkler"),
    path("settings/<int:id>_alter_sprinkler", alter_sprinkler.as_view(), name="alter_sprinkler"),
    path("settings/<int:id>_delete_sprinkler", delete_sprinkler.as_view(), name="delete_sprinkler"),
    path("calendar/", CalendarView.as_view(), name="calendar"),
    path("settings/create_timer", create_weekly_timers.as_view(), name="create_timer"),
    path("settings/<int:id>_alter_timer", alter_weekly_timers.as_view(), name="alter_timer"),
    path("settings/create_plan", create_IrrigationPlan.as_view(), name="create_IrrigationPlan"),
    path("settings/<int:id>_alter_plan",alter_IrrigationPlan.as_view(), name="alter_IrrigationPlan"),
    path("settings/<int:id>_delete_plan", delete_IrrigationPlan.as_view(), name="delete_IrrigationPlan"),
    path("weather/", weather.as_view(), name="weather"),
]
