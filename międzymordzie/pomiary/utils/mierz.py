#!/usr/bin/env python3

import sys
import time
import getopt
import alsaaudio
import math
import struct
import datetime

import django
django.setup()

from ..models import Pomiar, Sonda,Fragment, Dzien, Miesiac
from django.utils import timezone

DEBUG = False
now = timezone.now()
nazwa_sondy = 'W szafce'

def s_frag(wyn):
    s_frag.frag += wyn
    s_frag.num_frag += 1
    if abs(now - Sonda.objects.get(położenie=nazwa_sondy).data_ostatni_fragment) >= datetime.timedelta(minutes=10):
        #print("Fragment")
        f = Fragment(sonda=Sonda.objects.get(położenie=nazwa_sondy), wynik=s_frag.frag/s_frag.num_frag)
        f.save()
        s_frag.frag = 0
        s_frag.num_frag = 0
        Sonda.objects.filter(położenie=nazwa_sondy).update(data_ostatni_fragment = now)
s_frag.frag = 0
s_frag.num_frag = 0

def s_dzn(wyn):
    s_dzn.dzn += wyn
    s_dzn.num_dzn += 1
    if now.day != Sonda.objects.get(położenie=nazwa_sondy).data_ostatni_dzien.day:
        #print("Dzien")
        Fragment.objects.all().delete()
        d = Dzien(sonda=Sonda.objects.get(położenie=nazwa_sondy), wynik=s_dzn.dzn/s_dzn.num_dzn)
        d.save()
        s_dzn.dzn = 0
        s_dzn.num_dzn = 0
        Sonda.objects.filter(położenie=nazwa_sondy).update(data_ostatni_dzien = now)
s_dzn.dzn = 0
s_dzn.num_dzn = 0

def s_mie(wyn):
    s_mie.mie += wyn
    s_mie.num_mie += 1
    if now.month != Sonda.objects.get(położenie=nazwa_sondy).data_ostatni_miesiac.month:
        Dzien.objects.all().delete()
        m = Miesiac(sonda=Sonda.objects.get(położenie=nazwa_sondy), wynik=s_mie.mie/s_mie.num_mie)
        m.save()
        s_mie.mie = 0
        s_mie.num_mie = 0
        Sonda.objects.filter(położenie=nazwa_sondy).update(data_ostatni_miesiac = now)
s_mie.mie = 0
s_mie.num_mie = 0

def dodaj(wyn):
    p = Pomiar(sonda=Sonda.objects.get(położenie=nazwa_sondy), wynik=wyn)
    p.save()
    Sonda.objects.get(położenie=nazwa_sondy).ostatni_pomiar_wynik = p.wynik
    Sonda.objects.get(położenie=nazwa_sondy).ostatni_pomiar_data = p.data
    s_frag(wyn)
    s_dzn(wyn)
    s_mie(wyn)

def main():
    #device = 'default'
    device = 'pulse'

    opts, args = getopt.getopt(sys.argv[1:], 'd:')
    for o, a in opts:
        if o == '-d':
            device = a

    inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL, device=device)

    inp.setchannels(1)
    inp.setrate(44100)
    inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
    inp.setperiodsize(160)

    stest = 300
    test = stest
    suma = 0
    while True:
        l, data = inp.read()

        test -= 1
        try:
            st = struct.unpack('H'*160, data)
        except struct.error as se:
            print(len(data))
            continue
        try:
            suma += 20*math.log10(max(st)-min(st))
        except ValueError as ve:
            #print("ve")
            pass
        if test == 0:
            test = stest
            if DEBUG:
                print(suma/test)
            else:
                dodaj(suma/test)
            suma = 0

        time.sleep(.001)

if __name__ == '__main__':
    main()
