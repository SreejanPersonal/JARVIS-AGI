# Deployment Security and Privacy Controls

## Scope

This document describes the controls built into the first-release Jarvis Kiosk Agent deployment. It is intended for an owner-operated home server or private cloud VM. It does not turn the project into a publicly exposed, multi-tenant service.

## Container boundaries

| Component | Network exposure | Container controls | Persistent data |
|---|---|---|---|
| `agent-server` | The only published service; bind it to a trusted LAN address or loopback interface. | Runs as the non-root `app` user with a read-only root filesystem, a small writable `/tmp`, dropped Linux capabilities, `no-new-privileges`, an init process, and a PID limit. | The writable `agent_data` volume holds SQLite state, profile vault files, and explicit enrollment images. |
| `searxng` | Internal Compose network only; no host port is published. | Uses `no-new-privileges`, dropped capabilities, an init process, and a PID limit. | Its settings and cache volumes are separate from personal assistant data. |
| Google Drive mirror | Never published as a service. | Mounted into the agent container as read-only. | Import is explicit and profile-scoped; the running service cannot modify the mounted source folder. |

The application image runs as a non-root service account. Container hardening reduces the impact of a process compromise, but it does not replace host patching, firewall rules, backups, or physical control of the Docker server.

## Network deployment

Keep the kiosk service on a trusted home or office network. If the Galaxy Book is the only client, restrict inbound access to that device or subnet with the host firewall. For remote use, place the service behind an authenticated HTTPS reverse proxy or private VPN rather than exposing port `8080` directly to the public internet.

The default Compose topology does not publish SearXNG. Search requests flow from the internal agent service to the internal search service, while the kiosk communicates only with the agent service.

## Data and media boundaries

Conversation history, long-term memories, explicit saved notes, and profile vault content are stored under the agent data volume. An enrollment image can be saved only when the selected profile exists, is marked as consenting, and the user makes a visible confirmation in the camera dialog. The browser captures a reduced-size JPEG, sends it to the local server endpoint, and the server stores it in that profile’s local enrollment folder.

> Enrollment storage is not facial recognition. The first release does not perform background matching, identification, continuous camera recording, or remote camera ingestion.

Protect the host volume with normal operating-system account permissions and encrypted storage when available. Back up only data that the owner has chosen to retain, and ensure the backup destination has an access policy appropriate for household information.

## Action boundaries

| Action category | First-release policy |
|---|---|
| Messages and reservations | The assistant creates a proposal, then requires visible typed or voice confirmation before an owner-configured connector can receive it. |
| File transfer, location sharing, and device control | Only an owner-created, named-target rule with an expiry can authorize delivery. If no connector exists, the server records `connector_unavailable` rather than attempting delivery. |
| Google Drive import | The kiosk lists and imports supported text files only from a locally mounted, read-only mirror. |
| Camera and microphone | Browser permission is required. The wake-word listener begins off, is visibly labelled, and cannot itself send messages, operate devices, or activate the camera. |

The fixed agent policy may adapt tone and response style to profile preferences, but profile preferences cannot disable consent checks, action rules, privacy boundaries, or the requirement to accurately report whether an action was completed.

## Owner checklist

Before enabling the stack for regular household use, set a strong `SEARXNG_SECRET`, select an Ollama model that is already installed on the server, restrict the published port to the intended network, and keep `.env.agent` outside version control. Configure third-party services only through user-owned adapters and credentials. Review the action-rule list regularly, set short expiry times for sensitive rules, and remove profiles or enrollment images when consent is withdrawn.
