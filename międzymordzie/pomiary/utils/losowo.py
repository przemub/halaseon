#!/usr/bin/env python3

from ..models import Pomiar, Sonda, Fragment, Dzien, Miesiac

import django
django.setup()

from django.utils import timezone

import datetime
import random
import time


def s_frag(wyn, sonda):
    s_frag.frag += wyn
    s_frag.num_frag += 1
    if abs(timezone.now() - sonda.data_ostatni_fragment) >= datetime.timedelta(
            minutes=10):
        # print("Fragment")
        f = Fragment(sonda=sonda, wynik=s_frag.frag / s_frag.num_frag)
        f.save()
        s_frag.frag = 0
        s_frag.num_frag = 0
        sonda.data_ostatni_fragment = timezone.now()
        sonda.save()


s_frag.frag = 0
s_frag.num_frag = 0


def s_dzn(wyn, sonda):
    s_dzn.dzn += wyn
    s_dzn.num_dzn += 1
    if timezone.now().day != sonda.data_ostatni_dzien.day:
        # print("Dzien")
        Fragment.objects.all().delete()
        d = Dzien(sonda=sonda, wynik=s_dzn.dzn / s_dzn.num_dzn)
        d.save()
        s_dzn.dzn = 0
        s_dzn.num_dzn = 0
        sonda.data_ostatni_dzien = timezone.now()
        sonda.save()


s_dzn.dzn = 0
s_dzn.num_dzn = 0


def s_mie(wyn, sonda):
    s_mie.mie += wyn
    s_mie.num_mie += 1
    if timezone.now().month != sonda.data_ostatni_miesiac.month:
        Dzien.objects.all().delete()
        m = Miesiac(sonda=sonda, wynik=s_mie.mie / s_mie.num_mie)
        m.save()
        s_mie.mie = 0
        s_mie.num_mie = 0
        sonda.data_ostatni_miesiac=timezone.now()
        sonda.save()


s_mie.mie = 0
s_mie.num_mie = 0


def dodaj(wyn, sonda):
    p = Pomiar(sonda=sonda, wynik=wyn)
    p.save()
    sonda.ostatni_pomiar_wynik = wyn
    sonda.ostatni_pomiar_data = timezone.now()
    sonda.save()
    s_frag(wyn, sonda)
    s_dzn(wyn, sonda)
    s_mie(wyn, sonda)

def main():
    while True:
        for i, sonda in enumerate(Sonda.objects.all()):
            dodaj(random.randint(20+10*i, 35+10*i), sonda)
        time.sleep(0.8)
