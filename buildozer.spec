[app]
title = Object Tracker
package.name = objecttracker
package.domain = org.test

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,tflite
source.exclude_dirs = .git, __pycache__

version = 0.1

requirements = python3,kivy,opencv,numpy,android

android.permissions = CAMERA, INTERNET, ACCESS_NETWORK_STATE, ACCESS_WIFI_STATE

orientation = portrait
fullscreen = 0

android.add_src = ./
