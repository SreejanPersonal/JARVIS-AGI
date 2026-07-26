# Legacy JARVIS-AGI Material

The original repository remains intact at the project root for attribution and reference. It is not invoked by the new `agent_server` runtime.

The following legacy ideas may be reimplemented behind controlled adapters when they fit the new platform:

| Legacy area | New-platform treatment |
|---|---|
| Voice interaction | Browser-native microphone/speech functions on the kiosk, with explicit permissions. |
| Conversation history | Replaced by profile-scoped SQLite conversations and retrievable long-term memory. |
| Web retrieval | Replaced by a Docker-contained SearXNG adapter and bounded page extraction. |
| Local model support | Replaced by a configurable Ollama adapter. |
| Camera input | Replaced by an opt-in browser capture pipeline; no implicit device access. |

The new platform intentionally does not execute the legacy remote-provider wrappers, browser automation for speech recognition, cookie-related code, or script-execution path.
