# Connector and Google Drive Setup

The agent server does **not** contain account passwords, browser cookies, Google OAuth client secrets, or smart-device credentials. It creates a reviewable action proposal, enforces its confirmation or trusted-rule policy, and only then calls a connector that the owner configures.

## Action connector contract

Set `ACTION_WEBHOOK_URL` to a service you own on the same private network or a secured HTTPS endpoint. The agent sends a JSON `POST` request only after an action reaches an executable state.

```json
{
  "action_id": "opaque action identifier",
  "profile_id": "owner",
  "action_type": "message | booking | file_transfer | location_share | device_control",
  "summary": "human-readable description",
  "payload": {},
  "rule_id": "optional trusted-rule identifier"
}
```

If configured, `ACTION_WEBHOOK_TOKEN` is delivered as a bearer token. A connector should validate that token, restrict its accepted action types and targets, write an audit record, and return a JSON result with a short status message. The first-release agent defaults to **not delivered** whenever no connector is configured.

| Action type | Default approval path | Connector expectation |
|---|---|---|
| Message or booking | Kiosk typed or voice confirmation, then a separate delivery tap | Draft/send or reservation adapter owned by the household |
| File transfer | Named target must match an enabled owner-managed rule | Local share, USB, Bluetooth, or other allowlisted transfer adapter |
| Location share | Named recipient must match an enabled owner-managed rule | Family-location provider adapter with explicit recipient restriction |
| Device control | Named device must match an enabled owner-managed rule | Smart-home bridge constrained to configured device IDs |

## Google Drive mirror

Google Drive is storage and import/export space; it does not host the running Docker agent. For a private Drive-backed document brain:

1. Create a dedicated folder in the owner’s Google Drive, such as `Jarvis/Import`.
2. Sync or mount that folder on the Docker host with a tool you control, such as the Google Drive desktop client on Windows or an `rclone` mount on Linux.
3. Mount that host folder **read-only** into the agent container and set `GOOGLE_DRIVE_SYNC_DIR` to its container path.
4. From the agent UI or API, explicitly choose a supported text document to import into a selected profile’s local vault. An optional checkbox decides whether a short excerpt becomes recallable profile memory.

The import service permits only `.txt`, `.md`, `.csv`, `.json`, and `.log` documents under the configured mirror root. It rejects path traversal, follows no out-of-root files, imposes a 2 MB per-file limit, and keeps imports profile-scoped.

> **Recommendation:** Use a separate Drive folder for imports, and keep the database and profile vault on the Docker host. Back up the host’s encrypted data volume to Google Drive only after enabling disk or backup encryption appropriate for the household.
