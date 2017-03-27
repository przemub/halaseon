from django.shortcuts import render

from .models import Pomiar, Sonda

def index(request):
    context = {}

    wyniki = []
    opisy = []
    pomiary = []
    for sonda in Sonda.objects.all():
        wyniki += [[pomiar.wynik for pomiar in Pomiar.objects.filter(sonda=sonda)]]
        opisy += [[pomiar.data for pomiar in Pomiar.objects.filter(sonda=sonda)]]
        pomiary += [[pomiar for pomiar in Pomiar.objects.filter(sonda=sonda)]]

    context['wyniki'] = wyniki
    context['opisy'] = opisy
    context['sondy'] = [sonda for sonda in Sonda.objects.all()]
    context['pomiary'] = pomiary

    return render(request, 'pomiary/index.html', context)

