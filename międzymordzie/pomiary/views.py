from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone

from .models import Pomiar, Sonda

context = {}

def index(request):
    context['sondy'] = [sonda for sonda in Sonda.objects.all()]

    return render(request, 'pomiary/index.html', context)

def initial(request):
    return render(request, 'pomiary/initialScreen.html')

def live_update(request):
    dict = {}
    for sonda in Sonda.objects.all():
        dict[sonda.__str__()] = {'y': sonda.ostatni_pomiar_wynik, 'x': sonda.ostatni_pomiar_data}
    return JsonResponse(dict)

#def aktPrzerwa():
#    temp = []
#    for p in Przerwa:
#        temp.append(p)
#    sorted(temp, key=lambda x: x.godzina_koniec())
#    for i in range(len(temp)-1, 0, -1):
#        if temp[i].czas_koniec < timezone.now:
#            return temp[i]
#    return -1

def getData(request):
    period = request.GET.get("type","")
    dataset = []
    for sonda in context['sondy']:
        prep = {}
        prep['label'] = sonda.__str__()
        prep['borderColor'] = sonda.kolor
        prep['backgroundColor'] = sonda.kolor_alpha()
        data = []
        if period == 'break':
            time_threshold = timezone.now() - timezone.timedelta(hours=1)
            for pomiar in sonda.pomiary().filter(data__day=timezone.now().day).filter(data__gt=time_threshold):
                data.append({'x': pomiar.data, 'y': int(pomiar.wynik)})
            for pomiar in sonda.pomiary().filter(data__day=timezone.now().day).filter(data__gt=time_threshold):
                data.append({'x': pomiar.data, 'y': int(pomiar.wynik)})
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
