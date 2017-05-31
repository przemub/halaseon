#!/bin/bash

pulseaudio --daemon || true
pacmd set-source-volume 0 1400
python3 `dirname $0`/pomiary/utils/mierz.py

