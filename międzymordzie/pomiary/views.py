from django.shortcuts import render
from django.http import JsonResponse

from .models import Pomiar, Sonda

context = {}

def index(request):
    context['sondy'] = [sonda for sonda in Sonda.objects.all()]

    return render(request, 'pomiary/index.html', context)

def live_update(request):
    dict = {}
    for sonda in context['sondy']:
        dict[sonda.__str__()] = {'value': sonda.pomiary()[-1].wynik, 'time':{'godzina': sonda.pomiary()[-1].godzina(), 'data': sonda.pomiary()[-1].data.day}}

    return JsonResponse(dict)
