"""Verify the copyable server and a context edit through actual stdio MCP clients."""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import shutil
import sys
import tempfile
from datetime import UTC, datetime
from pathlib import Path

from mcp import Client, StdioServerParameters

ROOT = Path(__file__).resolve().parent


async def call(client: Client, name: str, arguments: dict) -> dict:
    result = await client.call_tool(name, arguments)
    if result.is_error or result.structured_content is None:
        raise AssertionError(f"{name} failed: {result.content}")
    return result.structured_content


async def verify() -> dict:
    with tempfile.TemporaryDirectory(prefix="my-product-guide-") as temporary:
        # Copy only the reusable implementation and context, outside the workshop repository.
        copied = Path(temporary) / "copied-template"
        copied.mkdir()
        for filename in ("server.py", "context_loader.py"):
            shutil.copy2(ROOT / filename, copied / filename)
        shutil.copytree(ROOT / "context", copied / "context")
        path = copied / "context/guide.json"
        raw = json.loads(path.read_text())
        task = raw["tasks"][0]
        task_id = task["id"]
        alternatives = [
            c for c in task["choices"] if not c["requires"] and c["id"] != task["default_choice"]
        ]
        if not alternatives:
            raise AssertionError(
                "The edit exercise needs two choices with no requirements in the first task"
            )
        changed_choice = alternatives[0]["id"]
        parameters = StdioServerParameters(command=sys.executable, args=["server.py"], cwd=copied)
        async with Client(parameters) as client:
            tools = await client.list_tools()
            assert {t.name for t in tools.tools} == {
                "list_tasks",
                "get_guidance",
                "recommend_next_step",
            }
            catalog = await call(client, "list_tasks", {})
            guidance = await call(client, "get_guidance", {"task_id": task_id})
            before = await call(client, "recommend_next_step", {"task_id": task_id})
            assert before["recommended_choice"] == task["default_choice"]
            assert before["decision_basis"] == "default"
            assert before["guidance_sources"][0]["revision"] == guidance["source"]["revision"]
            for reference in guidance["references"]:
                assert reference["content"]
            restricted = next((c for c in task["choices"] if c["requires"]), None)
            if restricted:
                blocked = await call(
                    client, "recommend_next_step", {"task_id": task_id, "choice": restricted["id"]}
                )
                assert blocked["decision_basis"] == "clarification_required"
                assert blocked["unmet_requirements"]
                assert blocked["recommended_choice"] == task["default_choice"]
                confirmed = await call(
                    client,
                    "recommend_next_step",
                    {
                        "task_id": task_id,
                        "choice": restricted["id"],
                        "facts": {key: True for key in restricted["requires"]},
                    },
                )
                assert confirmed["recommended_choice"] == restricted["id"]

        task["default_choice"] = changed_choice
        path.write_text(json.dumps(raw, indent=2) + "\n")
        async with Client(parameters) as client:
            after = await call(client, "recommend_next_step", {"task_id": task_id})
            assert after["recommended_choice"] == changed_choice
            assert (
                before["guidance_sources"][0]["revision"]
                != after["guidance_sources"][0]["revision"]
            )
            tools = await client.list_tools()
            assert f"Default: {changed_choice}" in next(
                t.description for t in tools.tools if t.name == "recommend_next_step"
            )

        # A second task is added in JSON; Python stays identical.
        new_id = "template-check"
        while any(item["id"] == new_id for item in raw["tasks"]):
            new_id += "-x"
        additional = json.loads(json.dumps(task))
        additional["id"] = new_id
        additional["title"] = "A task added in context only"
        raw["tasks"].append(additional)
        path.write_text(json.dumps(raw, indent=2) + "\n")
        async with Client(parameters) as client:
            extended = await call(client, "list_tasks", {})
            assert len(extended["tasks"]) == len(catalog["tasks"]) + 1
            added = await call(client, "recommend_next_step", {"task_id": new_id})
            assert added["recommended_choice"] == changed_choice

        return {
            "verified_at": datetime.now(UTC).isoformat(),
            "python_version": sys.version.split()[0],
            "scope": "Copied server outside workshop; real stdio clients; no editor/model tested",
            "implementation_revision": hashlib.sha256(
                b"".join(
                    (ROOT / filename).read_bytes()
                    for filename in ("server.py", "context_loader.py")
                )
            ).hexdigest(),
            "before": before,
            "after": after,
            "checks": [
                "standalone copy",
                "task discovery",
                "reference documents",
                "context-only default edit",
                "refreshed tool descriptions",
                "additional task without Python changes",
            ],
        }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = asyncio.run(verify())
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print("Template verified: standalone copy, context edit, source trace, and new task")


if __name__ == "__main__":
    main()
