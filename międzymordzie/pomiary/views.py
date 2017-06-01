from django.shortcuts import render
from django.http import JsonResponse

from .models import Pomiar, Sonda, newValue
import datetime

context = {}

def index(request):
    context['sondy'] = [sonda for sonda in Sonda.objects.all()]

    return render(request, 'pomiary/index.html', context)

def initial(request):
    return render(request, 'pomiary/initialScreen.html')

def live_update(request):
    dict = {}
    if len(newValue) > 0:
        dict[newValue['sonda'].__str__()] = {'value': newValue['pomiar'].wynik, 'data': newValue['pomiar'].data}
    return JsonResponse(dict)

def getData(request):
    period = request.GET.get("type","")
    dataset = []
    for sonda in context['sondy']:
        prep = {}
        prep['label'] = sonda.__str__()
        prep['borderColor'] = sonda.kolor
        prep['backgroundColor'] = sonda.kolor_alpha()
        if period == 'break':
            data = [{'x': pomiar.data, 'y': int(pomiar.wynik)} for pomiar in sonda.pomiary()]
        elif period == 'day':
            data = [{'x': frag.data, 'y': int(frag.wynik)} for frag in sonda.fragmenty()]
        elif period == 'month':
            data = [{'x': dzn.data, 'y': int(dzn.wynik)} for dzn in sonda.dni()]
        elif period == 'year':
            data = [{'x': mie.data, 'y': int(mie.wynik)} for mie in sonda.miesiace()]
        prep['data'] = data
        dataset.append(prep)


    dane = {'data': dataset}
    return JsonResponse(dane)


def handler400(request):
    return render(request, 'pomiary/400.html')

def handler403(request):
    return render(request, 'pomiary/403.html')

def handler404(request):
    return render(request, 'pomiary/404.html')

def handler500(request):
    return render(request, 'pomiary/500.html')
