#!/usr/bin/env python3
r"""
server.py  -  Tiny local HTTP listener for Stage D of the Minesweeper assignment
================================================================================
Run this BEFORE launching winmine_stageD.exe.  Every request the patched game
sends (a GET whose query string carries your message) is printed here and
appended to  beacon_log.txt .

    python server.py            # listens on 127.0.0.1:80   (matches the brief)
    python server.py 8080       # use another port if 80 is taken / needs admin

On Windows, port 80 is sometimes reserved by IIS / http.sys.  If you get
"Permission denied" or "address in use", either free the port or pass another
one (and point the patched URL at it).
"""
import sys, datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 80
LOGFILE = "beacon_log.txt"

def log(line):
    stamp = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{stamp}] {line}", flush=True)
    with open(LOGFILE, "a", encoding="utf-8") as f:
        f.write(f"[{stamp}] {line}\n")

class Handler(BaseHTTPRequestHandler):
    def _handle(self):
        parsed = urlparse(self.path)
        msg = parse_qs(parsed.query).get("msg", ["<none>"])[0]
        log(f"{self.command} {self.path}  from {self.client_address[0]}")
        log(f"        --> message = {msg!r}")
        body = b"OK - beacon received\n"
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    do_GET = do_POST = do_HEAD = _handle

    def log_message(self, *a):           # silence the default noisy logger
        pass

if __name__ == "__main__":
    log(f"==== listening on http://127.0.0.1:{PORT}/  (Ctrl+C to stop) ====")
    try:
        HTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
    except KeyboardInterrupt:
        log("==== stopped ====")
    except PermissionError:
        sys.exit(f"Permission denied binding port {PORT}. Try:  python server.py 8080")
    except OSError as e:
        sys.exit(f"Could not bind port {PORT}: {e}")
