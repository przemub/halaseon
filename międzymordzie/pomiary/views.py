from django.shortcuts import render
from django.http import JsonResponse

from .models import Pomiar, Sonda

def index(request):
    context = {}

    context['sondy'] = [sonda for sonda in Sonda.objects.all()]

    return render(request, 'pomiary/index.html', context)

def live_update(request):
    data = {
        'value': '30'
    }
    return JsonResponse(data);
