# Galaxy Book Kiosk Deployment

The Galaxy Book is a **thin kiosk client**, not the assistant server. It opens the locally hosted web interface, supplies touchscreen, microphone, speakers, and an optional webcam, while Docker, Ollama, search, profiles, long-term memory, Google Drive imports, and integrations run on a separate always-on server.

> **Do not install Ollama, Docker, a Google Drive mirror, or a local vector database on the Galaxy Book.** Keeping all computation on the server is the intended low-memory design.

## Operating-system choices

| Client path | When to use it | Included launcher |
|---|---|---|
| Lightweight Linux desktop | Recommended for a dedicated single-purpose kiosk. Install a current lightweight Linux desktop with a supported Chromium-based browser, verify Wi-Fi/audio/camera first, and use the Linux launcher. | `deployment/kiosk/linux/jarvis-kiosk.sh` |
| Existing Windows installation | Use when the touchscreen, LTE, camera, or drivers already work reliably and you prefer not to reinstall the tablet. | `deployment/kiosk/windows/start-jarvis-kiosk.cmd` |

The SM-W627Y support page confirms the Galaxy Book 10.6'' (128 GB, 4G) family, while a closely related LTE configuration is documented with a low-power Core m3 processor, integrated graphics, Wi-Fi, Bluetooth, USB-C, and a 5 MP camera. Because regional configurations can vary, confirm the actual installed memory and test the webcam, microphone, Wi-Fi, sleep/wake behavior, and touchscreen before committing to an OS change. [1] [2]

## Server address

Give the Docker server a stable local-network address, for example `http://192.168.1.20:8080`. The tablet needs only that address. For remote access, add a VPN or reverse proxy separately; do not publish the kiosk directly to the public internet.

## Linux profile

Copy `deployment/kiosk/linux/jarvis-kiosk.sh` to the kiosk user’s home directory, make it executable, and set the server address:

```bash
chmod +x ~/jarvis-kiosk.sh
JARVIS_AGENT_URL=http://192.168.1.20:8080 ~/jarvis-kiosk.sh
```

Configure the selected desktop environment to start that command after login. The launcher opens Chromium in kiosk mode. Browser-level microphone and camera permissions remain visible and must be granted by the person using the tablet.

## Windows profile

Edit `deployment/kiosk/windows/start-jarvis-kiosk.cmd` and set `JARVIS_AGENT_URL` to the server address. Double-click the file once to verify the kiosk opens. After testing, place a shortcut in the kiosk user’s Startup folder if automatic startup is desired.

## Browser privacy settings

Use the browser’s site settings for the server address to allow microphone and camera only when the household wants those inputs. The kiosk UI exposes its own microphone/camera controls; stopping the camera stops the browser capture stream. The first release records permission/audit state only and does not upload raw browser camera or microphone data without a dedicated, opt-in adapter.

## Recovery access

Retain a normal administrator account and a keyboard path to leave kiosk mode before enabling automatic launch. Do not use a kiosk launcher as the only method of administration.

## References

[1] [Samsung Australia — Galaxy Book 10.6'' (128GB, 4G), SM-W627Y](https://www.samsung.com/au/support/model/SM-W627YZKAXSA/)

[2] [Notebookcheck — Samsung Galaxy Book 10.6 W627N LTE specifications](https://www.notebookcheck.net/Samsung-Galaxy-Book-10-6-W627N-LTE.231714.0.html)
