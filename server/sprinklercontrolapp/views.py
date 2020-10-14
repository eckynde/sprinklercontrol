from datetime import datetime, timedelta, date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView

from sprinklercontrolapp.models import Sprinkler, WeeklyRepeatingTimer, IrrigationPlan, Weekday
from sprinklercontrolapp.forms import SprinklerForm, WeeklyTimersForm, IrrigationPlanForm
import calendar

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


class settings(LoginRequiredMixin, TemplateView):
    template_name = 'SprinklerControlDesign/settings.html'


class create_sprinkler(LoginRequiredMixin, CreateView):
    template_name = 'sprinklerControlDesign/sprinklercreateform.html'
    model = Sprinkler
    fields=['label','description']
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
    fields=['label','description']
    success_url = '/'
    
    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Sprinkler, id=id_)


class weekly_timers_list(LoginRequiredMixin, ListView):
    template_name = 'sprinklercontrolapp/weekly_timers_list.html'
    model = WeeklyRepeatingTimer
    context_object_name = "WeeklyRepeatingTimer"


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

class alter_irrigation_plan(LoginRequiredMixin, UpdateView):
    template_name = 'sprinklerControlDesign/irrigationPlanAlterForm.html'
    model = IrrigationPlan
    form_class = IrrigationPlanForm
    success_url = "/"

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(IrrigationPlan, id=id_)



def CalendarView(request):
    active_plan = IrrigationPlan.objects.get(active=True)
    context = {
        "plan":active_plan,
    }
    return render(request,'sprinklerControlDesign/calendar.html',context)

class weather(TemplateView):
    template_name = 'sprinklercontrolapp/weather.html'




@api_view(['POST'])
@login_required
def sprinkler_activate(request, pk):

    try: 
        sprinkler = Sprinkler.objects.get(pk=pk) 
    except Sprinkler.DoesNotExist: 
        return JsonResponse({'message': 'The sprinkler does not exist'}, status=status.HTTP_404_NOT_FOUND) 

    Sprinkler.objects.filter(pk=pk).update(mode='M', power=True)

    return JsonResponse({'message': 'Sprinkler has been activated successfully!'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@login_required
def sprinkler_deactivate(request, pk):

    try: 
        sprinkler = Sprinkler.objects.get(pk=pk) 
    except Sprinkler.DoesNotExist: 
        return JsonResponse({'message': 'The sprinkler does not exist'}, status=status.HTTP_404_NOT_FOUND) 

    Sprinkler.objects.filter(pk=pk).update(mode='M', power=False)

    return JsonResponse({'message': 'Sprinkler has been deactivated successfully!'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@login_required
def sprinkler_mode(request, pk, mode):

    try: 
        sprinkler = Sprinkler.objects.get(pk=pk) 
    except Sprinkler.DoesNotExist: 
        return JsonResponse({'message': 'The sprinkler does not exist'}, status=status.HTTP_404_NOT_FOUND) 

    if mode=='manual':
        Sprinkler.objects.filter(pk=pk).update(mode='M')
    elif mode=='plan':
        Sprinkler.objects.filter(pk=pk).update(mode='P')
    elif mode=='smart':
        Sprinkler.objects.filter(pk=pk).update(mode='S')
    else:
        return JsonResponse({'message': 'The mode ' + mode + ' does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    
    

    return JsonResponse({'message': 'Sprinkler has been set to ' + mode + 'successfully!'}, status=status.HTTP_200_OK)