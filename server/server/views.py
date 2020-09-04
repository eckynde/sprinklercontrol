from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    context = { 'title': 'World' }
    return render(request, 'server/index.html', context)
