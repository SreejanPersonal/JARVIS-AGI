# Local Smoke Test Findings

## 2026-07-26 — Kiosk render

The FastAPI service started successfully on local port `8008`. The kiosk page rendered the compact JARVIS header, active Owner profile selector, live-web toggle, browser-voice control, camera control, save-response control, and the new **Plan task** control. The skills panel populated from the local skill registry and showed configuration-required labels where appropriate.

The health indicator correctly reported that no Ollama service was reachable in the sandbox. This is expected because the smoke-test environment did not start Ollama. A sample task request, `Send a message to Ava about dinner at 7.`, was entered successfully and is ready for the action-planning interaction test.

## Task-planning interaction

The sample message task produced a three-step plan and an **EXTERNAL ACTION** card. The card correctly stated that the proposal would not be delivered until confirmation and rendered separate **Type confirmation** and **Confirm by voice** controls. This verifies that the kiosk distinguishes task planning from action delivery.

The automated click on the browser-native typed-confirmation prompt timed out, likely because the modal JavaScript prompt blocks the automation channel. This does not indicate a server error; the next test will use a non-modal confirmation path or inspect the current browser state without repeating the same interaction.


## Updated kiosk and Drive-mirror smoke test

The current service was started locally with a writable temporary data directory and viewed at `http://127.0.0.1:8009/`. The kiosk rendered its touch-friendly composer, profile selector, microphone/camera controls, task-planning button, skill drawer, and newly added Google Drive mirror panel. With no `GOOGLE_DRIVE_SYNC_DIR` configured, the panel correctly showed **“No Google Drive mirror directory is configured.”** rather than exposing any host files. The health indicator correctly reported that the local model was unavailable because no Ollama server was attached to the sandbox smoke-test process.


## Consented enrollment-control smoke test

The refreshed kiosk at `http://127.0.0.1:8009/` displayed the camera dialog with distinct **Capture audit** and **Save enrollment photo** actions. The enrollment action is paired with a visible statement that the active person has agreed to local profile-image storage and is disabled until the camera is running and the consent checkbox is selected. This confirms that enrollment capture is separated from ordinary camera permission and does not imply background recognition.


## Wake-word visibility smoke test

The refreshed kiosk displayed a dedicated **Wake word: Off** control with an explicit tooltip stating that it is a visible browser microphone listener using the default phrase “Jarvis.” The control starts in the off state before any microphone permission is requested. The test did not activate microphone access.
