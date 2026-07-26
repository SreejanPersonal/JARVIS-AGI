# Kiosk Agent Platform Architecture

## Purpose

This platform replaces the legacy console-loop runtime with a lightweight, Docker-hosted service. A Galaxy Book running Windows 10 remains a kiosk client: it renders the interface, captures explicit microphone/webcam input, plays speech, and presents approvals. All model calls, search retrieval, memory, integration logic, and optional image analysis run on the server.

## Deployment Shape

| Component | Location | Responsibility |
|---|---|---|
| `agent-server` | Docker host | FastAPI API, Ollama provider adapter, bounded task planner, SQLite memory, action rules, streamed answers, static kiosk assets. |
| `searxng` | Docker host | Aggregated web-search JSON endpoint. |
| Ollama | Docker host or host machine | Configurable local text/vision model endpoint. |
| Google Drive | Google account | Optional OAuth-authorized backup, selected per-person files, and document import source; it is never the compute host. |
| Galaxy Book kiosk | Windows 10 tablet | Browser-only display, microphone, webcam, speakers, and owner approval surface. |

The production path is a private LAN Docker server. A reverse proxy/TLS profile may be enabled when the kiosk connects across untrusted networks.

## Agent Boundaries

The planner is deliberately bounded: it receives a compact task context, chooses at most one tool or action proposal per cycle, observes the result, and stops at a configurable step limit. A model response is never authorization to perform an external action.

| Action category | Default policy |
|---|---|
| Search, recall, document retrieval, local memory | Allowed within the active profile and configured sources. |
| Compose message or booking | Produce draft, then require spoken or on-screen confirmation before submission. |
| File transfer, location share, smart-device control | Available only through named owner-managed rules with destination/device allowlists, expiry, status history, and a global stop switch. |
| Webcam, microphone, face/profile enrollment | Explicit browser permission, visible in-app state, opt-in per feature, and owner-managed deletion. |
| Credentials, payments, passwords, destructive operations, security settings | Not automated by the agent. |

## Persistent Data

SQLite is the primary local system of record. It stores profiles, consent records, conversation summaries, memories, task events, approval requests, action rules, and integration metadata. Sensitive provider tokens remain environment-managed or encrypted at rest in the eventual deployment. Google Drive synchronization is intentionally optional and operates on approved exports and selected source folders only.

## Service Layout

```text
agent_server/
  app/
    main.py                 FastAPI application and static kiosk delivery
    config.py               Environment-driven configuration
    db.py                   SQLite schema and data access
    models.py               API request/response types
    adapters/               Ollama, SearXNG, Google Drive, device adapters
    services/               Agent, memory, search, actions, profiles, policy
    static/                 Zero-build HTML/CSS/JavaScript kiosk client
  tests/                    Unit and API smoke tests
```

Legacy JARVIS-AGI code remains in the repository for attribution and reference. The new platform does not execute its remote-provider wrappers, browser-driving speech-recognition flow, or unrestricted script-execution path.

## Model Routing

`OLLAMA_MODEL` is an environment setting rather than a hard-coded choice. The platform starts with a small model default appropriate for CPU-first servers and exposes a health endpoint that reports model reachability. A larger or vision-capable model can be substituted without changing the kiosk client.

## Kiosk Interaction

The browser uses fetch streaming for answer delivery and browser-native speech synthesis. Speech recognition and webcam capture are browser-permission controlled. A low-resource mode avoids client-side models, heavy frameworks, persistent video streams, and background processing on the Galaxy Book.

## Initial APIs

| Endpoint | Role |
|---|---|
| `GET /health` | Service, database, Ollama, and search readiness. |
| `POST /api/chat/stream` | Stream a retrieved and synthesized response. |
| `GET /api/conversations/{profile_id}` | Load the active profile's recalled conversation context. |
| `POST /api/profiles` | Create an owner-managed profile. |
| `POST /api/actions/propose` | Create a typed action proposal or validate an existing pre-authorized rule. |
| `POST /api/actions/{id}/confirm` | Confirm a message or booking action. |
| `POST /api/media/capture` | Receive explicitly captured browser media metadata or approved image upload. |
```

The first implementation delivers the core server, memory model, Perplexity-style search/chat stream, kiosk interface, and action-proposal policy. Google OAuth, camera-provider adapters, device protocols, and external booking/messaging connectors are implemented as explicit adapters rather than embedded into the agent core.
