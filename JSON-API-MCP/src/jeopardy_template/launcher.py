"""Start a workspace MCP server with its own local API and clean shutdown."""

from __future__ import annotations

import argparse
import os
import socket
import sys
import threading
import time

import uvicorn

from .api import create_app
from .guidance import PROJECT_ROOT


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--server", choices=("guide", "wrapper", "deployment"), default="guide")
    args = parser.parse_args()
    if args.server == "deployment":
        from .guide_server import create_guide

        create_guide(tasks=("deployment",)).run()
        return

    # A private ephemeral port avoids collisions between the two editor windows.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
        listener.bind(("127.0.0.1", 0))
        listener.listen(128)
        port = listener.getsockname()[1]
        app = create_app(PROJECT_ROOT / "data/clues.json", PROJECT_ROOT / "data/manifest.json")
        server = uvicorn.Server(uvicorn.Config(app, log_level="warning", access_log=False))
        thread = threading.Thread(target=server.run, kwargs={"sockets": [listener]}, daemon=True)
        thread.start()
        try:
            deadline = time.monotonic() + 10
            while not server.started:
                if not thread.is_alive() or time.monotonic() >= deadline:
                    raise RuntimeError("The local clue API did not become ready")
                time.sleep(0.05)
            os.environ["JEOPARDY_API_BASE_URL"] = f"http://127.0.0.1:{port}"
            if args.server == "wrapper":
                from .mcp_server import mcp

                mcp.run()
            else:
                from .guide_server import create_guide

                create_guide().run()
        finally:
            server.should_exit = True
            thread.join(timeout=5)
            if thread.is_alive():
                print("Local API shutdown exceeded five seconds", file=sys.stderr)


if __name__ == "__main__":
    main()
