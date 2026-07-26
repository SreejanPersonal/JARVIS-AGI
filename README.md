# Jarvis Kiosk Agent

This repository now contains a **new, Docker-hosted local-agent service** designed for a low-resource tablet kiosk. It preserves the original JARVIS-AGI material under `legacy/` but does not run the legacy monolithic entry point. The new service keeps AI work, search, memory, and integrations on a separate server; the Samsung Galaxy Book is only a browser, microphone, speaker, touchscreen, and optional webcam client.

> **Google Drive is storage, not a Docker server.** Run this stack on an always-on home PC/server or cloud VM, and use a dedicated Google Drive folder only for explicit document imports and encrypted backups.

## First-release capability map

| Capability | Current implementation | Configuration needed |
|---|---|---|
| Local conversations | Streamed Ollama responses with per-profile conversation context | An Ollama server and a model selected in `.env.agent` |
| Perplexity-style search | Query rewrite, SearXNG retrieval, cited answer stream | Internet access from SearXNG |
| Persistent household memory | Separate SQLite conversations/memories and per-profile content folders | None after first start |
| Google Drive document brain | Explicit import from a read-only, locally mounted Drive mirror | A user-managed Drive sync/mount on the Docker host |
| Skills | Enable/disable registry with setup requirements | Configure each provider/device adapter separately |
| Tasks and external actions | Reviewable plans, message/booking confirmation, named trusted rules, bounded webhook delivery | An owner-controlled connector service |
| Tablet voice and camera | Browser talk control, optional visible wake-word listener, consent audit, and explicit per-profile enrollment-photo storage | Browser microphone/camera permissions; wake-word support varies by browser |
| Per-person identity features | Consenting profiles, private memory/vault folders, and local enrollment-image storage | Recognition and background matching are intentionally not enabled in the first release |
| Security cameras, contacts, Photos, Family Hub, location, Bluetooth/USB | Staged skills only; no account, device, or raw media connector is preconfigured | Add an explicit adapter and owner credentials/settings |

## Quick start

Install Docker Compose and Ollama on the **server**, not on the Galaxy Book. Start a local model on the server, then configure the project:

```bash
cp .env.agent.example .env.agent
# Edit .env.agent: set SEARXNG_SECRET and choose OLLAMA_MODEL.
docker compose --env-file .env.agent up --build -d
```

Open `http://SERVER_LAN_IP:8080` on the Galaxy Book. The Compose stack exposes only the agent kiosk; SearXNG remains on its internal Docker network. This follows SearXNG’s documented container setup pattern of mounting configuration and cache volumes while retaining its server configuration as a service concern. [1] [2]

The default model setting is `llama3.2:3b`, but it is only a placeholder. Change `OLLAMA_MODEL` to a model already pulled on the Docker host. The server hardware—not the tablet—determines the suitable model.

## Use Google Drive safely

Create a dedicated Drive folder such as `Jarvis/Import`, sync or mount it locally on the Docker host, and point `GOOGLE_DRIVE_HOST_DIR` at that host folder. Then set `GOOGLE_DRIVE_SYNC_DIR=/mnt/google-drive` in `.env.agent`. The container sees the directory read-only and the kiosk can explicitly import supported text documents into the selected person’s vault. See [Connector and Google Drive setup](docs/CONNECTORS.md).

## Use the Galaxy Book as a kiosk

The client is operating-system neutral. You may keep Windows or install a lightweight Linux desktop, then launch a supported Chromium-based browser in kiosk mode. Scripts for both paths are in `deployment/kiosk/`; see [Galaxy Book kiosk deployment](docs/KIOSK_DEPLOYMENT.md). The device family is documented by Samsung as the 10.6-inch, 128 GB, 4G SM-W627Y model; a related LTE configuration includes low-power mobile hardware and a camera, which is why this project performs no local AI inference. [3] [4]

## Action and privacy model

Messages and bookings produce a plan first and require typed or voice confirmation before the delivery endpoint is contacted. File transfers, location sharing, and device control may use only owner-created rules with named targets, an expiry time, a visible state, and a revocation path. The camera dialog now allows one explicit enrollment photo only for a consenting selected profile; the first release does not perform background recognition or raw media streaming. The optional wake-word listener is visibly off by default and cannot send messages or trigger device actions on its own.

The Compose stack uses a non-root application image, a read-only application filesystem, dropped capabilities, `no-new-privileges`, a PID limit, and an internal-only search service. See [deployment security](docs/SECURITY.md), the [staged rollout plan](docs/ROLLOUT.md), [architecture](docs/ARCHITECTURE.md), [connectors](docs/CONNECTORS.md), [smoke-test findings](docs/SMOKE_TEST.md), and the [legacy-foundation assessment](docs/FOUNDATION_ASSESSMENT.md) for detailed implementation notes.

## Verification

Run the regression suite without requiring Ollama or external accounts:

```bash
cd agent_server
PYTHONPATH=. python3 -m unittest discover -s tests -v
```

## References

[1] [SearXNG — Installation in a container](https://docs.searxng.org/admin/installation-docker.html)

[2] [SearXNG — Server settings](https://docs.searxng.org/admin/settings/settings_server.html)

[3] [Samsung Australia — Galaxy Book 10.6'' (128GB, 4G), SM-W627Y](https://www.samsung.com/au/support/model/SM-W627YZKAXSA/)

[4] [Notebookcheck — Samsung Galaxy Book 10.6 W627N LTE specifications](https://www.notebookcheck.net/Samsung-Galaxy-Book-10-6-W627N-LTE.231714.0.html)
