#!/bin/bash

pulseaudio --daemon || true
pacmd set-default-source alsa_input.usb-Creative_Labs_VF0420_Live__Cam_Vista_IM-01-IM.analog-mono
pacmd set-source-volume alsa_input.usb-Creative_Labs_VF0420_Live__Cam_Vista_IM-01-IM.analog-mono 1400

export DJANGO_SETTINGS_MODULE="halaseon.settings"
cd `dirname $0`
python3 -m pomiary.utils

