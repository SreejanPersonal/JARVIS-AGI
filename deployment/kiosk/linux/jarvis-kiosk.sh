#!/usr/bin/env bash
# Lightweight kiosk launcher. Configure the agent URL below before use.
set -euo pipefail

AGENT_URL="${JARVIS_AGENT_URL:-http://127.0.0.1:8080}"
BROWSER="${JARVIS_BROWSER:-chromium}"

if ! command -v "$BROWSER" >/dev/null 2>&1; then
  echo "Browser not found: $BROWSER" >&2
  echo "Install Chromium or set JARVIS_BROWSER to your supported browser binary." >&2
  exit 1
fi

exec "$BROWSER" \
  --kiosk "$AGENT_URL" \
  --no-first-run \
  --no-default-browser-check \
  --disable-session-crashed-bubble \
  --disable-features=TranslateUI \
  --start-maximized
