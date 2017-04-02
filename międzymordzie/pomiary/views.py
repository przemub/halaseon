from django.shortcuts import render
from django.http import JsonResponse

from .models import Pomiar, Sonda

context = {}

def index(request):
    context['sondy'] = [sonda for sonda in Sonda.objects.all()]

    return render(request, 'pomiary/index.html', context)

def initial(request):
    return render(request, 'pomiary/initialScreen.html')

def live_update(request):
    dict = {}
    for sonda in context['sondy']:
        dict[sonda.__str__()] = {'value': sonda.pomiary()[-1].wynik, 'time':{'godzina': sonda.pomiary()[-1].godzina(), 'hour': sonda.pomiary()[-1].data.hour(), 'minute': sonda.pomiary()[-1].data.minute(), 'data': sonda.pomiary()[-1].data.day}}

    return JsonResponse(dict)

def handler400(request):
    return render(request, 'pomiary/400.html')

def handler403(request):
    return render(request, 'pomiary/403.html')

def handler404(request):
    return render(request, 'pomiary/404.html')

def handler500(request):
    return render(request, 'pomiary/500.html')
