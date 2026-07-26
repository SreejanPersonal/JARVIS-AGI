# Foundation Assessment

## Repository Sources

| Item | Reference | Assessment date |
|---|---|---|
| User repository | `https://github.com/whoami22888/JARVIS-AGI` | 2026-07-26 |
| Upstream repository | `https://github.com/SreejanPersonal/JARVIS-AGI` | 2026-07-26 |
| Reviewed branch and revision | `main` at `9aa7e54` | 2026-07-26 |

## Findings

The original project is a Python console loop with local microphone/camera assumptions, hosted-provider wrappers, file-based chat history, and experimental utilities. Its documented feature areas include speech recognition, text processing, image analysis, hotword detection, and audio playback. The reviewed runtime does not provide a Docker deployment, FastAPI/HTTP service boundary, Ollama adapter, profile-scoped memory, persistent action authorization, secure Google Drive synchronization, or tablet kiosk interface.

Its dependency manifest includes interactive/local-media packages such as PyAudio, Vosk, OpenCV, Porcupine, pygame, and hosted-provider clients. Its main entry point directly coordinates speech input, remote text classification/generation, local Windows system customization, camera capture, and speech output in an infinite loop. This is not suitable as the server runtime for a resource-constrained kiosk client.

## Decision

The project is retained for attribution and reference, with potentially useful user-experience ideas documented under `legacy/`. The new `agent_server` implementation is a separate, Docker-first FastAPI service using a configurable Ollama endpoint, internal SearXNG retrieval, SQLite persistence, an OS-neutral browser kiosk, and typed action-policy boundaries.

## Google Storage Note

Google Drive is supported as a future authorized storage, document-import, and backup integration. It is not a Docker or Ollama compute host. The current task configuration contains an enabled Google Workspace integration, but the source platform will not depend on it; production Google Drive synchronization will use explicit user-owned OAuth credentials or another approved deployment mechanism.
