"""A tiny json-server replacement for chapter 2.

Serves every top-level list in a JSON file as a REST collection:

    GET    /<collection>          all items
    GET    /<collection>/<id>     one item
    POST   /<collection>          create an item (the server picks the id)
    PUT    /<collection>/<id>     replace an item
    PATCH  /<collection>/<id>     change some fields of an item
    DELETE /<collection>/<id>     delete an item

Every change is written back to the JSON file.

Usage: python mock_server.py db.json --port 3001
"""

import argparse
import json
import secrets
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Lock

lock = Lock()


def make_handler(db_path: Path) -> type[BaseHTTPRequestHandler]:
    def load() -> dict:
        return json.loads(db_path.read_text(encoding="utf-8"))

    def save(db: dict) -> None:
        db_path.write_text(json.dumps(db, indent=2) + "\n", encoding="utf-8")

    class Handler(BaseHTTPRequestHandler):
        def _send(self, status: HTTPStatus, body: object = None) -> None:
            data = b"" if body is None else json.dumps(body).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            print(f"  -> {status.value} {status.phrase}", flush=True)

        def _route(self) -> tuple[str, str | None]:
            parts = [p for p in self.path.split("?")[0].split("/") if p]
            if len(parts) == 1:
                return parts[0], None
            if len(parts) == 2:
                return parts[0], parts[1]
            return "", None

        def _body(self) -> dict | None:
            length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(length) if length else b""
            print(f"{self.command} {self.path} {raw.decode() if raw else ''}", flush=True)
            if not raw:
                return None
            try:
                body = json.loads(raw)
            except json.JSONDecodeError:
                return None
            return body if isinstance(body, dict) else None

        def _handle(self) -> None:
            body = self._body()
            name, item_id = self._route()
            with lock:
                db = load()
                items = db.get(name)
                if not isinstance(items, list):
                    return self._send(HTTPStatus.NOT_FOUND, {})
                index = next(
                    (i for i, it in enumerate(items) if str(it.get("id")) == item_id),
                    None,
                )

                if self.command == "GET":
                    if item_id is None:
                        return self._send(HTTPStatus.OK, items)
                    if index is None:
                        return self._send(HTTPStatus.NOT_FOUND, {})
                    return self._send(HTTPStatus.OK, items[index])

                if self.command == "POST" and item_id is None:
                    if body is None:
                        return self._send(HTTPStatus.BAD_REQUEST, {"error": "JSON object body required"})
                    new = {**body, "id": secrets.token_hex(2)}
                    items.append(new)
                    save(db)
                    return self._send(HTTPStatus.CREATED, new)

                if item_id is None or index is None:
                    return self._send(HTTPStatus.NOT_FOUND, {})

                if self.command in ("PUT", "PATCH"):
                    if body is None:
                        return self._send(HTTPStatus.BAD_REQUEST, {"error": "JSON object body required"})
                    base = items[index] if self.command == "PATCH" else {}
                    items[index] = {**base, **body, "id": items[index]["id"]}
                    save(db)
                    return self._send(HTTPStatus.OK, items[index])

                if self.command == "DELETE":
                    removed = items.pop(index)
                    save(db)
                    return self._send(HTTPStatus.OK, removed)

                return self._send(HTTPStatus.METHOD_NOT_ALLOWED, {})

        do_GET = do_POST = do_PUT = do_PATCH = do_DELETE = _handle

        def log_message(self, format: str, *args: object) -> None:
            pass  # our own prints are enough

    return Handler


def main() -> None:
    parser = argparse.ArgumentParser(description="Tiny json-server replacement")
    parser.add_argument("db", type=Path, help="path to the JSON file")
    parser.add_argument("--port", type=int, default=3001)
    args = parser.parse_args()

    if not args.db.exists():
        parser.error(f"{args.db} does not exist")

    server = ThreadingHTTPServer(("localhost", args.port), make_handler(args.db))
    print(f"Serving {args.db} on http://localhost:{args.port}", flush=True)
    for name, value in json.loads(args.db.read_text(encoding="utf-8")).items():
        if isinstance(value, list):
            print(f"  http://localhost:{args.port}/{name}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped")


if __name__ == "__main__":
    main()