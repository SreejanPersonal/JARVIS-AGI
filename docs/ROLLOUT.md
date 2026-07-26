# Owner Rollout Plan

## Purpose

This rollout sequence brings the Docker-hosted Jarvis Kiosk Agent online without placing an unconfigured cloud account, camera system, or home-control connector in the critical path. The Galaxy Book remains a lightweight kiosk client; all model inference, indexing, persistence, and integration work occurs on the server.

| Stage | Goal | Owner action | Success condition |
|---|---|---|---|
| 1. Private core | Start the local assistant on a trusted network. | Copy `.env.agent.example` to `.env.agent`, set `SEARXNG_SECRET`, select an Ollama model already installed on the Docker host, and start Compose. | The Galaxy Book opens the kiosk page and `/health` reports the expected service state. |
| 2. Profiles and memory | Establish separate household memories and saved folders. | Create one consenting profile at a time, confirm profile switching, save a note, and review the profile vault. | A note or conversation from one profile does not appear in another profile’s memory or vault. |
| 3. Voice and webcam | Enable explicitly initiated browser media. | Grant microphone or camera permission only while testing, use the talk button, and optionally capture one enrollment image for a consenting person. | The browser visibly indicates the active feature; the enrollment image is written only to the selected profile folder. |
| 4. Drive import | Use Google Drive as a selected document source and backup location. | Sync a dedicated Drive folder to the Docker host, mount it read-only, then import a supported document from the kiosk. | The selected document becomes profile-scoped memory while the original Drive mirror remains unchanged. |
| 5. Action connector | Connect a user-owned messaging, booking, or automation adapter. | Deploy a narrowly scoped connector endpoint, configure its URL and token in `.env.agent`, and create minimal allowlists/rules. | A task proposal is visible before delivery; messages and bookings require confirmation and named rule actions target only approved destinations. |
| 6. Expansion adapters | Add features that need vendor-specific APIs or hardware. | Implement and test one adapter at a time for contacts, Google Photos, Family Hub, security cameras, location, Bluetooth, USB, or local file transfer. | Each adapter reports configuration status, exposes a clear disable control, and obeys the core action/privacy policy. |

## Recommended first server profile

Use a small always-on Linux Docker host if possible, because it provides the simplest maintenance path for Docker, Ollama, local mounted folders, and firewall rules. Windows with Docker Desktop also works for the provided Compose topology. The Galaxy Book does **not** run Docker or Ollama; it only opens the kiosk in a Chromium-based browser.

Choose the first Ollama model by the server—not the tablet. Start with the `OLLAMA_MODEL` value in `.env.agent` only if that model is already installed and responds acceptably on the host. Change the setting without changing application code when you upgrade server hardware or test a different model.

## Implemented baseline versus adapters

> The delivered source is a usable private-assistant baseline, not a pre-authorized connection to every service named in the original brief.

The baseline implements local conversation streaming, cited search retrieval, profile-separated memory and saved folders, a Drive-mirror import path, action planning, confirmation/rule enforcement, an owner-configured connector contract, browser voice controls, an optional visible wake-word listener, explicit webcam enrollment storage, a skills registry, and an operating-system-neutral kiosk page.

Contacts, Google Photos, direct messaging providers, reservation providers, Family Hub, named Wi-Fi cameras, location sharing, Bluetooth, USB, and direct LAN transfer are deliberately adapter slots. Each depends on the user’s actual vendor, account connection, device model, permissions, and network topology. Configure them in isolated increments after the core kiosk works.

## Daily operating routine

Start by selecting the active person’s profile. Use normal chat or web search for information, save only information worth keeping, and use **Plan task** for an action goal. Confirm messages and bookings before a connector is contacted. Review and expire trusted action rules for device, location, or file tasks as household needs change. Use the browser’s visible controls to stop the camera, microphone, or wake-word listener whenever they are not needed.

## Recovery and upgrades

Back up the `agent_data` Docker volume before upgrading images or changing the host. Keep `.env.agent`, connector credentials, and backup keys out of source control. Upgrade the Docker image, SearXNG image, Ollama installation, and operating system independently, then run the regression command in the repository before returning the kiosk to regular use.

```bash
cd agent_server
PYTHONPATH=. python3 -m unittest discover -s tests -v
```
