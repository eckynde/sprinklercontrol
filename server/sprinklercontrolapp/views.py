from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, CreateView, UpdateView
from sprinklercontrolapp.models import Sprinkler, WeeklyRepeatingTimer
from sprinklercontrolapp.forms import SprinklerForm, WeeklyTimersForm

# Create your views here.
class overview(ListView):
    template_name = 'sprinklercontrolapp/overview.html'
    model = Sprinkler
    context_object_name = "Sprinkler"


class settings(TemplateView):
    template_name = 'sprinklercontrolapp/settings.html'


class statistics(TemplateView):
    template_name = 'sprinklercontrolapp/statistics.html'


class create_sprinkler(CreateView):
    template_name = 'sprinklercontrolapp/create_sprinkler.html'
    model = Sprinkler
    form_class = SprinklerForm
    success_url = "/"


class alter_sprinkler(UpdateView):
    template_name = 'sprinklercontrolapp/alter_sprinkler.html'
    model = Sprinkler
    form_class = SprinklerForm
    success_url = '/'
    
    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Sprinkler, id=id_)


class weekly_timers_list(ListView):
    template_name = 'sprinklercontrolapp/weekly_timers_list.html'
    model = WeeklyRepeatingTimer
    context_object_name = "WeeklyRepeatingTimer"


class alter_weekly_timers(UpdateView):
    template_name = 'sprinklercontrolapp/alter_timer.html'
    model = WeeklyRepeatingTimer
    form_class = WeeklyTimersForm
    success_url = "weekly_timers_list"

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(WeeklyRepeatingTimer, id=id_)

class create_weekly_timers(CreateView):
    template_name = 'sprinklercontrolapp/alter_timer.html'
    model = WeeklyRepeatingTimer
    form_class = WeeklyTimersForm
    success_url = "weekly_timers_list"

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(WeeklyRepeatingTimer, id=id_)