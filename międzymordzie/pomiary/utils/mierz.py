#!/usr/bin/env python3

import sys
import time
import getopt
import alsaaudio
import math
import struct
import datetime

from ..models import Pomiar, Sonda, newValue

now = datetime.datetime.now()

frag = 0
num_frag = 0

dzn = 0
num_dzn = 0

mie = 0
num_mie = 0

def s_frag(wyn):
    frag += wyn
    num_frag++
    if now.min - Sonda.objects.all().first().min >= 10:
        f = Fragment(sonda=Sonda.objects.all().first(), wynik=frag/num_frag)
        f.save()
        frag = 0
        num_frag = 0
        Sonda.objects.all().first().data_ostatni_fragment = now
        Sonda.objects.all().first().save()

def s_dzn(wyn):
    dzn += wyn
    num_dzn++
    if now.day != Sonda.objects.all().first().day:
        #Wypieprzyc frag

        d = Dzien(sonda=Sonda.objects.all().first(), wynik=dzn/num_dzn)
        d.save()
        dzn = 0
        num_dzn = 0
        Sonda.objects.all().first().data_ostatni_dzien = now
        Sonda.objects.all().first().save()

def s_mie(wyn):
    mie += wyn
    num_mie++
    if now.month != Sonda.objects.all().first().month:
        #Wypieprzyc dzn

        m = Miesiac(sonda=Sonda.objects.all().first(), wynik=mie/num_mie)
        m.save()
        mie = 0
        num_mie = 0
        Sonda.objects.all().first().data_ostatni_miesiac = now
        Sonda.objects.all().first().save()

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
