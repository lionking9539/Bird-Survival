[app]

# (str) Title of your application
title = Bird Survival

# (str) Package name
package.name = flappybird

# (str) Package domain (needed for android/ios packaging)
package.domain = org.test

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (leave empty to include all the files)
source.include_exts = py,png,jpg,jpeg,wav,ogg

# (list) List of inclusions using pattern matching
source.include_patterns = *.png,*.jpg,*.jpeg,*.wav,*.ogg

# (list) Application requirements
requirements = python3,pygame

# (str) Presplash of the application
presplash.filename = %(source.dir)s/presplash.png

# (str) Icon of the application
icon.filename = %(source.dir)s/icon.png

# (str) Supported orientation (one of landscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (int) Target Android API, should be as high as possible
android.api = 35

# (int) Minimum API your APK will support
android.minapi = 21

# (bool) If True, then automatically accept SDK license
android.accept_sdk_license = True

# (str) Android logcat filters to use
android.logcat_filters = *:S python:D

# (str) Android permissions
android.permissions = INTERNET

# (str) Android entry point, default is ok for Kivy-based app
android.entrypoint = org.kivy.android.PythonActivity

# (str) The Android arch to build for
android.archs = arm64-v8a

# (bool) If True, can use 64-bit architectures
android.allow_backup = True

# (int) Android version code
android.numeric_version = 1

# (str) The AAPT version to use
# android.aapt_version = 0.2
