#!/bin/bash

pulseaudio --daemon || true
pacmd set-source-volume 0 1400

export DJANGO_SETTINGS_MODULE="halaseon.settings"
cd `dirname $0`
python3 -m pomiary.utils

