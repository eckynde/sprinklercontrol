from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from sprinklercontrolapp.models import Sprinkler, WeeklyRepeatingTimer, IrrigationPlan
from sprinklercontrolapp.forms import SprinklerForm, WeeklyTimersForm, IrrigationPlanForm

from datetime import datetime, timedelta, date
from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.utils.safestring import mark_safe
from .utils import Calendar
import calendar

# Create your views here.
class overview(ListView):
    template_name = 'sprinklerControlDesign/overview.html'
    model = Sprinkler
    context_object_name = "Sprinkler"


class settings(TemplateView):
    template_name = 'sprinklercontrolapp/settings.html'


class create_sprinkler(CreateView):
    template_name = 'sprinklercontrolapp/create_form.html'
    model = Sprinkler
    form_class = SprinklerForm
    success_url = "/"
    

class delete_sprinkler(DeleteView):
    template_name = 'sprinklercontrolapp/delete_form.html'
    model = Sprinkler
    success_url = "/"

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Sprinkler, id=id_)

class alter_sprinkler(UpdateView):
    template_name = 'sprinklercontrolapp/alter_form.html'
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
    template_name = 'sprinklercontrolapp/alter_form.html'
    form_class = WeeklyTimersForm
    success_url = "/calendar"

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(WeeklyRepeatingTimer, id=id_)

class create_weekly_timers(CreateView):
    template_name = 'sprinklercontrolapp/create_form.html'
    model = WeeklyRepeatingTimer
    form_class = WeeklyTimersForm
    success_url = "/calendar"

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(WeeklyRepeatingTimer, id=id_)

class CalendarView(generic.ListView):
    model = WeeklyRepeatingTimer
    template_name = 'sprinklercontrolapp/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

class create_IrrigationPlan(CreateView):
    template_name = 'sprinklercontrolapp/create_form.html'
    model = IrrigationPlan
    form_class = IrrigationPlanForm
    success_url = "/"

class delete_IrrigationPlan(DeleteView):
    template_name = 'sprinklercontrolapp/delete_form.html'
    model = IrrigationPlan
    success_url = "/"

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(IrrigationPlan, id=id_)

class alter_IrrigationPlan(UpdateView):
    template_name = 'sprinklercontrolapp/alter_form.html'
    model = IrrigationPlan
    form_class = IrrigationPlanForm
    success_url = '/'
    
    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(IrrigationPlan, id=id_)


def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


class weather(TemplateView):
    template_name = 'sprinklercontrolapp/weather.html'