"""Tiny dependency-free service used to demonstrate the platform deployment."""

from __future__ import annotations

import json
import os
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

STARTED_AT = time.monotonic()
REQUEST_COUNT = 0


def payload(path: str) -> tuple[int, str, bytes]:
    global REQUEST_COUNT
    REQUEST_COUNT += 1

    if path == "/health":
        return 200, "application/json", _json({"status": "healthy"})
    if path == "/ready":
        return 200, "application/json", _json({"status": "ready"})
    if path == "/metrics":
        uptime = time.monotonic() - STARTED_AT
        metrics = (
            "# HELP platform_app_requests_total HTTP requests handled.\n"
            "# TYPE platform_app_requests_total counter\n"
            f"platform_app_requests_total {REQUEST_COUNT}\n"
            "# HELP platform_app_uptime_seconds Process uptime.\n"
            "# TYPE platform_app_uptime_seconds gauge\n"
            f"platform_app_uptime_seconds {uptime:.3f}\n"
        )
        return 200, "text/plain; version=0.0.4", metrics.encode()
    if path == "/":
        return 200, "application/json", _json(
            {
                "service": "platform-app",
                "environment": os.getenv("APP_ENV", "development"),
                "version": os.getenv("APP_VERSION", "local"),
            }
        )
    return 404, "application/json", _json({"error": "not_found"})


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        status, content_type, body = payload(self.path.split("?", 1)[0])
        self.send_response(status)
        self.send_header("content-type", content_type)
        self.send_header("content-length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: Any) -> None:
        print(json.dumps({"message": format % args, "client": self.client_address[0]}), flush=True)


def _json(value: dict[str, str]) -> bytes:
    return json.dumps(value, separators=(",", ":")).encode()


def main() -> None:
    port = int(os.getenv("PORT", "8080"))
    server = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    print(json.dumps({"message": "server_started", "port": port}), flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
