from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class overview(TemplateView):
    template_name = 'sprinklercontrolapp/overview.html'


class settings(TemplateView):
    template_name = 'sprinklercontrolapp/settings.html'


class statistics(TemplateView):
    template_name = 'sprinklercontrolapp/statistics.html'