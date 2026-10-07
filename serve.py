import http.server
import os
import re
import socketserver
import sys

SRC = "/repo/The VJ Pulse _ Base44.html"
OUT = "/srv/index.html"

# This repo is a single saved HTML snapshot of a Base44 app. Its inline
# analytics/tracking scripts stall the preview iframe, so strip every
# <script> tag (non-greedy, keeps the rendered HTML/CSS). Also blank out
# references to the missing saved-assets folder so they don't 404.
html = open(SRC, encoding="utf-8").read()
html = re.sub(r"<script.*?</script>", "", html, flags=re.S)
html = re.sub(r'src="\./The VJ Pulse _ Base44_files/[^"]*"', 'src=""', html)
os.makedirs("/srv", exist_ok=True)
open(OUT, "w", encoding="utf-8").write(html)


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="/srv", **kwargs)


class Server(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True

    def handle_error(self, request, client_address):
        # Swallow benign errors from clients disconnecting mid-transfer
        # (ConnectionResetError/BrokenPipeError); these are not real failures.
        exc = sys.exc_info()[1]
        if isinstance(exc, (ConnectionResetError, BrokenPipeError)):
            return
        super().handle_error(request, client_address)


if __name__ == "__main__":
    Server(("0.0.0.0", 3000), Handler).serve_forever()
