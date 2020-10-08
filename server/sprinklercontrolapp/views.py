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
    all_events = WeeklyRepeatingTimer.objects.all()
    context = {
        "events":all_events,
    }
    return render(request,'sprinklerControlDesign/calendar.html',context)

class weather(TemplateView):
    template_name = 'sprinklercontrolapp/weather.html'


#CRUD API Views
#@api_view(['GET', 'POST', 'DELETE'])
#def sprinklercontrolapp_list(request):
#    # GET list of sprinklers, POST a new sprinkler, DELETE all sprinklers
 
 
#@api_view(['GET', 'PUT', 'DELETE'])
#def sprinkler_detail(request, pk):
#    # find sprinkler by pk (id)
#    try: 
#        sprinkler = Sprinkler.objects.get(pk=pk) 
#    except sprinkler.DoesNotExist: 
#        return JsonResponse({'message': 'The Sprinkler does not exist'}, status=status.HTTP_404_NOT_FOUND) 
# 
#    # GET / PUT / DELETE tutorial
    
        
#@api_view(['GET'])
#def sprinklercontrolapp_published(request):
#    # GET all published tutorials

#Custom API Views
#@api_view(['GET', 'PUT', 'DELETE'])
#def sprinkler_detail(request, pk):
#    sprinkler = Sprinkler.objects.get(pk=pk)
#    # ...
# 
#    if request.method == 'PUT': 
#        sprinkler_data = JSONParser().parse(request) 
#        sprinkler_serializer = SprinklerSerializer(sprinkler, data=sprinkler_data) 
#        if sprinkler_serializer.is_valid(): 
#            sprinkler_serializer.save() 
#            return JsonResponse(sprinkler_serializer.data) 
#        return JsonResponse(sprinkler_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# 
@api_view(['GET', 'PUT', 'DELETE'])
def sprinkler_detail(request, pk):

    try: 
        sprinkler = Sprinkler.objects.get(pk=pk) 
    except Sprinkler.DoesNotExist: 
        return JsonResponse({'message': 'The sprinkler does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
    if request.method == 'GET': 
        sprinkler_serializer = SprinklerSerializer(sprinkler) 
        return JsonResponse(sprinkler_serializer.data) 
 
    elif request.method == 'PUT': 
        sprinkler_data = JSONParser().parse(request) 
        sprinkler_serializer = SprinklerSerializer(sprinkler, data=sprinkler_data) 
        if sprinkler_serializer.is_valid(): 
            sprinkler_serializer.save() 
            return JsonResponse(sprinkler_serializer.data) 
        return JsonResponse(sprinkler_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
    elif request.method == 'DELETE': 
        sprinkler.delete() 
        return JsonResponse({'message': 'Sprinkler was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def sprinkler_activate(request, pk):

    try: 
        sprinkler = Sprinkler.objects.get(pk=pk) 
    except Sprinkler.DoesNotExist: 
        return JsonResponse({'message': 'The sprinkler does not exist'}, status=status.HTTP_404_NOT_FOUND) 

    Sprinkler.objects.filter(pk=pk).update(power=True)
    #Sprinkler.objects.save()

    return JsonResponse({'message': 'Sprinkler has been activated successfully!'}, status=status.HTTP_200_OK)

@api_view(['GET'])
def sprinkler_deactivate(request, pk):

    try: 
        sprinkler = Sprinkler.objects.get(pk=pk) 
    except Sprinkler.DoesNotExist: 
        return JsonResponse({'message': 'The sprinkler does not exist'}, status=status.HTTP_404_NOT_FOUND) 

    Sprinkler.objects.filter(pk=pk).update(power=False)
    #Sprinkler.objects.save()

    return JsonResponse({'message': 'Sprinkler has been deactivated successfully!'}, status=status.HTTP_200_OK)



