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

from ..models import Pomiar, Sonda, newValue

now = datetime.datetime.now()

def s_frag(wyn):
    s_frag.frag += wyn
    s_frag.num_frag += 1
    if now.min - Sonda.objects.all().first().min >= 10:
        f = Fragment(sonda=Sonda.objects.all().first(), wynik=s_frag.frag/s_frag.num_frag)
        f.save()
        s_frag.frag = 0
        s_frag.num_frag = 0
        Sonda.objects.all().first().data_ostatni_fragment = now
        Sonda.objects.all().first().save()
s_frag.frag = 0
s_frag.num_frag = 0

def s_dzn(wyn):
    s_dzn.dzn += wyn
    s_dzn.num_dzn += 1
    if now.day != Sonda.objects.all().first().day:
        #Wypieprzyc frag

        d = Dzien(sonda=Sonda.objects.all().first(), wynik=s_dzn.dzn/s_dzn.num_dzn)
        d.save()
        s_dzn.dzn = 0
        s_dzn.num_dzn = 0
        Sonda.objects.all().first().data_ostatni_dzien = now
        Sonda.objects.all().first().save()
s_dzn.dzn = 0
s_dzn.num_dzn = 0

def s_mie(wyn):
    s_mie.mie += wyn
    s_mie.num_mie += 1
    if now.month != Sonda.objects.all().first().month:
        #Wypieprzyc dzn

        m = Miesiac(sonda=Sonda.objects.all().first(), wynik=s_mie.mie/s_mie.num_mie)
        m.save()
        s_mie.mie = 0
        s_mie.num_mie = 0
        Sonda.objects.all().first().data_ostatni_miesiac = now
        Sonda.objects.all().first().save()
s_mie.mie = 0
s_mie.num_mie = 0

def dodaj(wyn):
    p = Pomiar(sonda=Sonda.objects.all().first(), wynik=wyn)
    p.save()
    newValue['pomiar'] = p
    newValue['sonda'] = Sonda.objects.all().first()
    s_frag(wyn)
    s_dzn(wyn)
    s_frag(wyn)

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

    stest = 100
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
            pass
        if test == 0:
            test = stest
            #print(suma/test)
            dodaj(suma/test)
            suma = 0

        time.sleep(.001)

if __name__ == '__main__':
    main()
