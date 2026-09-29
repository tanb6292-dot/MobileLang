[app]
title = MobileLang Engine
package.name = mobilelang
package.domain = org.mobilelang
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,mbl
version = 1.0
requirements = python3,kivy
orientation = portrait
fullscreen = 0

# ⭐ ဒီ ၃ line ထည့်ပါ
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a

android.permissions = VIBRATE, INTERNET, POST_NOTIFICATIONS
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
