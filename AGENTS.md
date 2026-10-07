# Base44 Dev Environment

## What this repo is

This repository is **not** a fullstack application with source code. It contains a
single saved HTML snapshot of a Base44 app called "The VJ Pulse"
(`The VJ Pulse _ Base44.html`), captured via a browser "Save Page As" from the
Base44 editor preview. There is no `package.json`, backend, database, or build step.

The saved assets folder (`The VJ Pulse _ Base44_files/`) referenced by the HTML is
absent, so external images/scripts in the snapshot will 404. The page's rendered
DOM is inlined in the HTML, so the frozen UI still displays.

## Running it

The app is served as a static page with nginx on host port 3000:

```
docker compose -f docker-compose.base44.yml up -d --build
```

- nginx copies the HTML snapshot to `index.html` at startup and serves it at `/`.
- No credentials or external services are required.
- This is a static snapshot — it is not interactive and will not reflect edits to
  the HTML without a container restart (call `reload_preview` after changes).

## Verification

- `curl http://localhost:3000/` returns the HTML page (HTTP 200).
- `docker compose ps` shows the `web` service healthy.
