#!/usr/bin/env python3

import sys
import time
import getopt
import alsaaudio
import math
import struct

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
            print(suma/test)
            suma = 0

        time.sleep(.001)

if __name__ == '__main__':
    main()

