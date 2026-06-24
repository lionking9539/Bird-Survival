# Bird Survival

Bird Survival is a small Pygame game that is now prepared for safe local use and GitHub publication.

## What changed for GitHub publishing
- Added a repository-safe ignore file so build artifacts and temporary files stay out of version control.
- Added a GitHub Actions workflow to automatically run tests on push and pull requests.
- Added a license and security policy for a more professional repository.
- Hardened the game code so it handles missing assets, bad input, and unsafe file paths more safely.

## Files
- `Flappybird.py` — main gameplay loop and security hardening
- `main.py` — entry point used for packaging
- `buildozer.spec` — Android packaging configuration
- `android_build.sh` — helper script for installing build tools
- `tests/test_security.py` — regression tests for safe asset and score handling

## Run locally
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the game:
   ```bash
   python main.py
   ```

## Required assets
Place these files in the project root:
- `background.png`
- `player.png`
- `pipe.png`
- `jump.wav`
- `point.wav`
- `die.wav`

## Security improvements
- Asset loading is restricted to the project folder.
- High scores are sanitized before being saved.
- Audio playback is guarded so missing files do not crash the game.
- The game can run in headless or CI environments without failing completely.

## Android packaging
1. Install the Android SDK and NDK.
2. Install Buildozer:
   ```bash
   pip install buildozer
   ```
3. Build an APK for testing:
   ```bash
   buildozer -v android debug
   ```
4. Build a release bundle for the Play Store:
   ```bash
   buildozer -v android release
   ```
5. Upload the generated signed `.aab` to the Google Play Console.

## GitHub publish checklist
1. Create a new repository on GitHub.
2. Commit these changes.
3. Push the repository to GitHub.
4. Enable GitHub Actions if it does not run automatically.
5. Add screenshots and a description to the repository page.
