from datetime import datetime, timedelta, date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView

from sprinklercontrolapp.models import Sprinkler, WeeklyRepeatingTimer, IrrigationPlan, Weekday, Preferences, WeatherCurrent, WeatherForecast, SprinklerPoweredHistory
from sprinklercontrolapp.forms import SprinklerForm, WeeklyTimersForm, IrrigationPlanForm, IrrigationPlanFormCreate
import calendar
from datetime import datetime
import pytz
import time

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from sprinklercontrolapp.serializers import SprinklerSerializer
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect

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


@login_required
def settings(request):
    return render(request, 'SprinklerControlDesign/settings.html', {'preferences': Preferences.load()})


class create_sprinkler(LoginRequiredMixin, CreateView):
    template_name = 'sprinklerControlDesign/sprinklercreateform.html'
    model = Sprinkler
    fields=['label','description','demand','output']
    success_url = "/"


class delete_sprinkler(LoginRequiredMixin, DeleteView):
    template_name = 'sprinklerControlDesign/sprinklerdeleteform.html'
    model = Sprinkler
    success_url = "/"

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Sprinkler, id=id_)


class alter_sprinkler(LoginRequiredMixin, UpdateView):
    template_name = 'sprinklerControlDesign/sprinkleralterform.html'
    model = Sprinkler
    fields=['label','description','demand','output']
    success_url = '/'

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Sprinkler, id=id_)


class alter_weekly_timers(LoginRequiredMixin, UpdateView):
    template_name = 'sprinklerControlDesign/intervallAlterForm.html'
    form_class = WeeklyTimersForm

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(WeeklyRepeatingTimer, id=id_)

    def post(self, request, *args, **kwargs):
        id_ = self.kwargs.get("id")
        instance = WeeklyRepeatingTimer.objects.get(id=id_)
        form = WeeklyTimersForm(request.POST or None, instance=instance)
        if form.is_valid():
            form.save()
            next = request.POST.get('next', '/')
            print("Next: " + next)
            if next:
                return HttpResponseRedirect(next)
            else:
                return HttpResponseRedirect("/")


class create_weekly_timers(LoginRequiredMixin, CreateView):
    template_name = 'sprinklerControlDesign/intervallCreateForm.html'
    model = WeeklyRepeatingTimer
    form_class = WeeklyTimersForm
    success_url = "/settings"

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(WeeklyRepeatingTimer, id=id_)


class delete_weekly_timers(LoginRequiredMixin, DeleteView):
    template_name = 'sprinklerControlDesign/intervallDeleteForm.html'
    model = WeeklyRepeatingTimer
    success_url = "/"

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(WeeklyRepeatingTimer, id=id_)


class alter_irrigation_plan(LoginRequiredMixin, UpdateView):
    template_name = 'sprinklerControlDesign/irrigationPlanAlterForm.html'
    model = IrrigationPlan
    form_class = IrrigationPlanForm
    success_url = "/"

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(IrrigationPlan, id=id_)


class create_irrigation_plan(LoginRequiredMixin, CreateView):
    template_name = 'sprinklerControlDesign/irrigationPlanCreateForm.html'
    model = IrrigationPlan
    form_class = IrrigationPlanFormCreate
    success_url = "/"


class delete_irrigation_plan(LoginRequiredMixin, DeleteView):
    template_name = 'sprinklerControlDesign/irrigationPlanDeleteForm.html'
    model = IrrigationPlan
    success_url = "/"

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(IrrigationPlan, id=id_)


class statistics(LoginRequiredMixin, TemplateView):
    template_name = "sprinklerControlDesign/statistics.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        d = datetime.now(tz=pytz.timezone("Europe/Berlin"))

        dates = []
        dates.insert(1, (d-timedelta(days=1)))
        dates.insert(2, (d-timedelta(days=2)))
        dates.insert(3, (d-timedelta(days=3)))
        dates.insert(4, (d-timedelta(days=4)))
        dates.insert(5, (d-timedelta(days=5)))
        dates.insert(6, (d-timedelta(days=6)))
        dates.insert(7, (d-timedelta(days=7)))

        sprinklers = []

        for s in Sprinkler.objects.all():
            times = []
            for d in dates:
                anfang = d.replace(hour=0, minute=0, second=0, microsecond=0)
                ende = d.replace(hour=23, minute=59, second=59, microsecond=0)
                alltimes = SprinklerPoweredHistory.objects.filter(timeofevent__range=(anfang, ende), sprinkler=s.pk).order_by("timeofevent")

                zeitinsek = 0

                for a in alltimes:
                    if a.powered == True:
                        zeitinsek = zeitinsek - a.timeofevent.time().hour*60*60 - a.timeofevent.minute*60 - a.timeofevent.second
                    else:
                        zeitinsek = zeitinsek + a.timeofevent.time().hour*60*60 + a.timeofevent.minute*60 + a.timeofevent.second
                
                if alltimes.count()>0:
                    if alltimes[alltimes.count()-1].powered == True:
                        zeitinsek = zeitinsek + 24*60*60

                times.append(zeitinsek/60)
            
            data = {
                'id': s.pk,
                'label': s.label,
                'times': times,
            }
            sprinklers.append(data)
        
        datesf = []

        for d in dates:
            datesf.append(d.date().strftime("%d.%m.%Y"))

        
        context['sprinklers'] = sprinklers
        context['dates'] = datesf

        return context


@login_required
def CalendarView(request):
    try:
        active_plan = IrrigationPlan.objects.get(active=True)
    except IrrigationPlan.DoesNotExist:
        active_plan = None
    context = {
        "plan": active_plan,
    }
    return render(request, 'sprinklerControlDesign/calendar.html', context)


class weather(LoginRequiredMixin, ListView):
    template_name = 'sprinklerControlDesign/weather.html'
    model = WeatherCurrent
    context_object_name = "WeatherCurrent"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['WeatherCurrent'] = WeatherCurrent.objects.latest('id')
        except WeatherCurrent.DoesNotExist:
            context['WeatherCurrent'] = None
        try:
            context['WeatherForecast'] = WeatherForecast.objects.latest('id')
        except WeatherForecast.DoesNotExist:
            context['WeatherForecast'] = None
        return context

class intervallSettings(LoginRequiredMixin, ListView):
    template_name = 'sprinklerControlDesign/intervallSettings.html'
    model = WeeklyRepeatingTimer
    context_object_name = "WeeklyRepeatingTimer"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['WeeklyRepeatingTimer'] = WeeklyRepeatingTimer.objects.all()
        return context

@api_view(['POST'])
@login_required
def sprinkler_activate(request, pk):

    # check if sprinkler exists
    try:
        sprinkler = Sprinkler.objects.get(pk=pk)
    except Sprinkler.DoesNotExist:
        return JsonResponse({'message': 'The sprinkler does not exist'}, status=status.HTTP_404_NOT_FOUND)

    # set mode to manual, turn on
    Sprinkler.objects.filter(pk=pk).update(mode='M', power=True)

    # add to history
    SprinklerPoweredHistory.objects.create(sprinkler=Sprinkler.objects.get(
        pk=pk), timeofevent=datetime.now(tz=pytz.timezone("Europe/Berlin")), powered=True)
    return JsonResponse({'message': 'Sprinkler has been activated successfully!'}, status=status.HTTP_200_OK)

# overview page api endpoint: turn off sprinkler
@api_view(['POST'])
@login_required
def sprinkler_deactivate(request, pk):

    # check if sprinkler exists
    try:
        sprinkler = Sprinkler.objects.get(pk=pk)
    except Sprinkler.DoesNotExist:
        return JsonResponse({'message': 'The sprinkler does not exist'}, status=status.HTTP_404_NOT_FOUND)

    # set mode to manual, turn off
    Sprinkler.objects.filter(pk=pk).update(mode='M', power=False)

    # add to history
    SprinklerPoweredHistory.objects.create(sprinkler=Sprinkler.objects.get(
        pk=pk), timeofevent=datetime.now(tz=pytz.timezone("Europe/Berlin")), powered=False)
    return JsonResponse({'message': 'Sprinkler has been deactivated successfully!'}, status=status.HTTP_200_OK)

# overview page api endpoint: set sprinkler mode
@api_view(['POST'])
@login_required
def sprinkler_mode(request, pk, mode):

    # check if sprinkler exists
    try:
        sprinkler = Sprinkler.objects.get(pk=pk)
    except Sprinkler.DoesNotExist:
        return JsonResponse({'message': 'The sprinkler does not exist'}, status=status.HTTP_404_NOT_FOUND)

    # apply mode
    if mode == 'manual':
        # set mode to manual, turn off
        Sprinkler.objects.filter(pk=pk).update(mode='M', power=False)

    elif mode == 'plan':
        # set mode to plan
        Sprinkler.objects.filter(pk=pk).update(mode='P')
        # check if sprinkler is scheduled to be running now and set state accordingly
        for i in IrrigationPlan.objects.filter(active=True).values("timers"):
            times = WeeklyRepeatingTimer.objects.filter(
                pk=i.get("timers")).values()
            now = datetime.now().time()
            if now > times[0]["timestart"] and now < times[0]["timestop"]:
                Sprinkler.objects.filter(pk=pk).update(power=True)
                return JsonResponse({'message': 'Sprinkler has been set to ' + mode + ' successfully!'}, status=status.HTTP_200_OK)
        Sprinkler.objects.filter(pk=pk).update(power=False)

    elif mode == 'smart':
        # set mode to smart
        Sprinkler.objects.filter(pk=pk).update(mode='S')
    else:
        return JsonResponse({'message': 'The mode ' + mode + ' does not exist'}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({'message': 'Sprinkler has been set to ' + mode + ' successfully!'}, status=status.HTTP_200_OK)


# settings page api endpoint: set OpenWeatherMap city
@api_view(['POST'])
@login_required
def update_city(request, city):

    Preferences.objects.filter(pk=1).update(city=city)

    return JsonResponse({'message': 'City has been set to ' + city + ' successfully!'}, status=status.HTTP_200_OK)


# settings page api endpoint: set OpenWeatherMap api key
@api_view(['POST'])
@login_required
def update_apikey(request, apikey):

    Preferences.objects.filter(pk=1).update(apikey = apikey)
    
    return JsonResponse({'message': 'API-Key has been set to ' + apikey + ' successfully!'}, status=status.HTTP_200_OK)