# Implementation References

The Docker stack uses SearXNG's supported container image and mounts persistent configuration at `/etc/searxng` and cache data at `/var/cache/searxng`. The application points to SearXNG over the internal Compose network; its search endpoint is not published separately to the LAN.

| Reference | Applied decision |
|---|---|
| [SearXNG — Installation container](https://docs.searxng.org/admin/installation-docker.html) | Use Compose, mount configuration/cache directories, and maintain SearXNG as an internal service. |
| [SearXNG — `settings.yml`](https://docs.searxng.org/admin/settings/settings.html) | Set a non-default server secret and use a compact override configuration based on default settings. |
| [Official Compose template](https://raw.githubusercontent.com/searxng/searxng/master/container/docker-compose.yml) | Keep SearXNG's configuration and cache as separate mounted volumes; do not expose its port in this project. |
| [Official environment template](https://raw.githubusercontent.com/searxng/searxng/master/container/.env.example) | Use explicit version/host/port values only where required; project-specific variables stay in the top-level `.env`. |
| [SearXNG — `server:` settings](https://docs.searxng.org/admin/settings/settings_server.html) | Pass the required non-default server secret through the documented `SEARXNG_SECRET` environment variable. |

The first deployment creates a random SearXNG secret in `.env`; it must not be committed to Git.

## Galaxy Book kiosk client references

The Samsung Australia support page identifies the relevant device family as **Galaxy Book 10.6'' (128GB, 4G), SM-W627Y** and provides Windows-era manuals, drivers, and support material. It is used here only to confirm the model family, not to recommend retaining Windows.

Notebookcheck’s technical listing for the related Galaxy Book 10.6 W627N LTE configuration reports an Intel Core m3-7Y30, integrated Intel HD 615 graphics, a 10.6-inch 1920×1080 display, Wi-Fi ac, Bluetooth 4.1, USB-C, and a 5 MP camera. The user-reported installed RAM should take priority because regional configurations can differ; the kiosk design therefore performs no local AI inference and uses only a browser client.

Sources:

1. Samsung Australia, [Galaxy Book 10.6'' (128GB, 4G) — SM-W627Y](https://www.samsung.com/au/support/model/SM-W627YZKAXSA/).
2. Notebookcheck, [Samsung Galaxy Book 10.6 W627N LTE specifications](https://www.notebookcheck.net/Samsung-Galaxy-Book-10-6-W627N-LTE.231714.0.html).
