from django.shortcuts import render

from .models import Pomiar, Sonda

def index(request):
    context = {}

    context['sondy'] = [sonda for sonda in Sonda.objects.all()]

    return render(request, 'pomiary/index.html', context)

