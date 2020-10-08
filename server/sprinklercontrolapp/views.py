from datetime import datetime, timedelta, date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView

from sprinklercontrolapp.models import Sprinkler, WeeklyRepeatingTimer, IrrigationPlan, Weekday
from sprinklercontrolapp.forms import SprinklerForm, WeeklyTimersForm, IrrigationPlanForm
import calendar

# Create your views here.
class overview(LoginRequiredMixin, ListView):
    template_name = 'sprinklerControlDesign/overview.html'
    model = Sprinkler
    context_object_name = "Sprinkler"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['IrrigationPlan'] = IrrigationPlan.objects.all()
        context['Weekdays'] = Weekday.objects.all()
        context['Sprinklers'] = Sprinkler.objects.all()
        return context


class settings(LoginRequiredMixin, TemplateView):
    template_name = 'sprinklercontrolapp/settings.html'


class create_sprinkler(LoginRequiredMixin, CreateView):
    template_name = 'sprinklercontrolapp/create_form.html'
    model = Sprinkler
    form_class = SprinklerForm
    success_url = "/"
    

class delete_sprinkler(LoginRequiredMixin, DeleteView):
    template_name = 'sprinklercontrolapp/delete_form.html'
    model = Sprinkler
    success_url = "/"

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Sprinkler, id=id_)

class alter_sprinkler(LoginRequiredMixin, UpdateView):
    template_name = 'sprinklercontrolapp/alter_form.html'
    model = Sprinkler
    form_class = SprinklerForm
    success_url = '/'
    
    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Sprinkler, id=id_)


class weekly_timers_list(LoginRequiredMixin, ListView):
    template_name = 'sprinklercontrolapp/weekly_timers_list.html'
    model = WeeklyRepeatingTimer
    context_object_name = "WeeklyRepeatingTimer"


class alter_weekly_timers(LoginRequiredMixin, UpdateView):
    template_name = 'sprinklercontrolapp/alter_form.html'
    form_class = WeeklyTimersForm
    success_url = "/calendar"

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(WeeklyRepeatingTimer, id=id_)

class create_weekly_timers(LoginRequiredMixin, CreateView):
    template_name = 'sprinklercontrolapp/create_form.html'
    model = WeeklyRepeatingTimer
    form_class = WeeklyTimersForm
    success_url = "/calendar"

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(WeeklyRepeatingTimer, id=id_)

def CalendarView(request):
    active_plan = IrrigationPlan.objects.get(active=True)
    context = {
        "plan":active_plan,
    }
    return render(request,'sprinklerControlDesign/calendar.html',context)

class weather(TemplateView):
    template_name = 'sprinklercontrolapp/weather.html'