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

The app is served as a static page by `serve.py` (python:3.12-slim) on port 3000:

```
docker compose -f docker-compose.base44.yml up -d --build
```

- `serve.py` reads the snapshot, strips every `<script>` tag (the inline
  analytics/tracking scripts stall the preview iframe), blanks references to the
  missing saved-assets folder, and serves the cleaned rendered HTML/CSS.
- `handle_error` swallows benign `ConnectionResetError`/`BrokenPipeError` from
  clients disconnecting mid-transfer so the logs stay clean.
- No credentials or external services are required.
- This is a static snapshot — it is not interactive. Edits to `serve.py` or the
  snapshot require a container restart (call `reload_preview` after changes).

## Verification

- `curl http://localhost:3000/` returns the cleaned page (HTTP 200, 0 `<script>`
  tags, `id="root"` present, title `The VJ Pulse |`).
- `docker compose ps` shows the `web` service healthy.
- `docker compose logs web` shows only 200 access lines, no tracebacks.
