# Security Notes

## Summary
This project is a small Pygame game intended for desktop and Android deployment. The code now uses safer asset resolution, validated high-score persistence, and guarded audio playback so missing or malformed files do not crash the game.

## Hardening Measures
- Asset paths are restricted to the project folder and only allow known safe file extensions.
- High scores are sanitized and written atomically to reduce corruption.
- Audio playback is wrapped so missing or broken sound files fail gracefully.
- The game can still run in headless or CI environments with a fallback surface.

## Reporting a Vulnerability
If you discover a security issue, please report it privately by opening a GitHub Security Advisory or contacting the repository maintainer.
