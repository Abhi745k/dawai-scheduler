[app]

# App title
title = Medicine Reminder

# Package name
package.name = medicinereminder

# Package domain (needed for android/ios package)
package.domain = org.medicinereminder

# Source code directory
source.dir = .

# Source files to include
source.include_exts = py,png,jpg,kv,atlas,json

# Application versioning
version = 1.0

# Application requirements (removed pandas due to numpy build issues on Android)
requirements = python3,kivy,kivymd,gtts,requests

# Main file
android.entrypoint = org.kivy.android.PythonActivity

# Presplash background color
presplash.color = #FFFFFF

# Icon of the application
#icon.filename = %(source.dir)s/icon.png

# Supported orientation
orientation = portrait

# Android specific
fullscreen = 0

# Auto-accept Android SDK licenses
android.accept_sdk_license = True

# Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,VIBRATE

# Android API to use
android.api = 31

# Minimum API
android.minapi = 21

# Android NDK version to use
android.ndk = 25b

# Android SDK version to use
android.sdk = 31

# Arch
android.archs = arm64-v8a,armeabi-v7a

[buildozer]

# Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# Display warning if buildozer is run as root
warn_on_root = 1
