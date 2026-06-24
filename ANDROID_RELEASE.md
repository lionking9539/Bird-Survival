# Android release guide for Bird Survival

## Important note
The current game is a desktop Python/Pygame script. To publish on Google Play, you should first package it for Android using a mobile-friendly setup.

## Recommended setup
Use one of these options:

1. **Kivy + Buildozer** (recommended for Android release)
2. **pygame + python-for-android** (possible, but more setup)

## Minimum release checklist
- Create a unique app package name (for example `com.yourname.flappygame`)
- Add app icon (`icon.png`)
- Add a splash screen / loading screen
- Create a privacy policy URL
- Prepare screenshots and store description
- Create a signing key for release builds
- Build an `.aab` file for Google Play

## Build workflow
### 1) Install tools
- Python
- Android SDK
- Android NDK
- Buildozer

### 2) Create a mobile project
If using Kivy:
```bash
pip install buildozer kivy
buildozer init
```

### 3) Configure the build file
Update `buildozer.spec` with:
- package name
- app version
- permissions
- icon and splash assets
- requirements (`kivy`, `pygame` if needed)

### 4) Build for Android
```bash
buildozer -v android debug
```
For release:
```bash
buildozer -v android release
```

### 5) Generate a signed AAB
Google Play requires an Android App Bundle (`.aab`), not just an APK.

## Play Store submission
- Upload the signed `.aab`
- Fill in store listing details
- Add content rating
- Set up ads / in-app purchases if needed
- Test on multiple devices before publishing

## Next step I recommend
Convert the game logic from the current desktop script into a mobile-friendly Android project first, then build the release bundle.
