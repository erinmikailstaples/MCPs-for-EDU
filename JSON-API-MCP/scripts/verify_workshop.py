#!/usr/bin/env python3
"""Exercise real stdio servers and content-only edits without an editor or external API."""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import os
import shutil
import sys
import tempfile
from datetime import UTC, datetime
from pathlib import Path

from mcp import Client, StdioServerParameters

from jeopardy_template.guidance import CONTENT_DIR, PROJECT_ROOT


def parameters(server: str, content_dir: Path) -> StdioServerParameters:
    return StdioServerParameters(
        command=sys.executable,
        args=["-m", "jeopardy_template.launcher", "--server", server],
        cwd=PROJECT_ROOT,
        env={**os.environ, "GUIDANCE_CONTENT_DIR": str(content_dir)},
    )


async def call(client: Client, name: str, arguments: dict) -> dict:
    result = await client.call_tool(name, arguments)
    if result.is_error or result.structured_content is None:
        raise AssertionError(f"{name} failed: {result.content}")
    return result.structured_content


async def verify() -> dict:
    with tempfile.TemporaryDirectory(prefix="education-guide-") as temp:
        content = Path(temp) / "content"
        shutil.copytree(CONTENT_DIR, content)
        # Normalize only the temporary copy so reruns work even after attendee edits.
        practice_path = content / "practice.json"
        practice = json.loads(practice_path.read_text())
        next(r for r in practice["rules"] if r["id"] == "practice.default_count")["value"] = 2
        practice_path.write_text(json.dumps(practice, indent=2) + "\n")
        deployment_path = content / "deployment.json"
        deployment = json.loads(deployment_path.read_text())
        next(r for r in deployment["rules"] if r["id"] == "deployment.default_environment")[
            "value"
        ] = "preview"
        deployment_path.write_text(json.dumps(deployment, indent=2) + "\n")

        async with Client(parameters("guide", content)) as client:
            tools = await client.list_tools()
            assert {t.name for t in tools.tools} == {
                "get_guidance",
                "build_practice_set",
                "reveal_answer",
                "recommend_deployment",
            }
            guidance = await call(client, "get_guidance", {"task": "practice"})
            before = await call(client, "build_practice_set", {"category": "Developer Tools"})
            assert before["returned_count"] == 2
            assert all("answer" not in clue for clue in before["items"])
            assert guidance["content_revision"] == before["guidance"][0]["content_revision"]
            reveal = await call(client, "reveal_answer", {"clue_id": before["items"][0]["id"]})
            assert reveal["answer"]
            override = await call(
                client, "build_practice_set", {"category": "Developer Tools", "clue_count": 1}
            )
            assert override["returned_count"] == 1
            assert override["guidance"][0]["decision_basis"] == "explicit_user_choice"
            shortage = await call(
                client, "build_practice_set", {"category": "Developer Tools", "clue_count": 10}
            )
            assert shortage["shortage"] and shortage["returned_count"] == 3
            trap = await call(client, "recommend_deployment", {"target": "production"})
            assert trap["recommended_target"] == "preview" and trap["question"]

        next(r for r in practice["rules"] if r["id"] == "practice.default_count")["value"] = 3
        practice_path.write_text(json.dumps(practice, indent=2) + "\n")
        async with Client(parameters("guide", content)) as client:
            after = await call(client, "build_practice_set", {"category": "Developer Tools"})
            assert after["returned_count"] == 3
            assert (
                after["guidance"][0]["content_revision"]
                != before["guidance"][0]["content_revision"]
            )
            tools = await client.list_tools()
            description = next(t.description for t in tools.tools if t.name == "build_practice_set")
            assert "Start with 3 clues" in description

        async with Client(parameters("wrapper", content)) as client:
            tools = await client.list_tools()
            assert {t.name for t in tools.tools} == {"search_clues", "get_clue", "list_categories"}
            raw = await call(client, "search_clues", {"category": "Developer Tools", "limit": 2})
            assert len(raw["items"]) == 2 and "answer" in raw["items"][0]
            numeric = await call(client, "get_clue", {"clue_id": 0})
            final = await call(client, "get_clue", {"clue_id": 4})
            assert numeric["item"]["value"] == 200
            assert final["item"]["value"] is None
            await call(client, "list_categories", {})

        async with Client(parameters("deployment", content)) as client:
            before_deploy = await call(client, "recommend_deployment", {})
            assert before_deploy["recommended_target"] == "preview"
        next(r for r in deployment["rules"] if r["id"] == "deployment.default_environment")[
            "value"
        ] = "staging"
        deployment_path.write_text(json.dumps(deployment, indent=2) + "\n")
        async with Client(parameters("deployment", content)) as client:
            tools = await client.list_tools()
            assert {t.name for t in tools.tools} == {"get_guidance", "recommend_deployment"}
            after_deploy = await call(client, "recommend_deployment", {})
            assert after_deploy["recommended_target"] == "staging"
            trap = await call(client, "recommend_deployment", {"target": "production"})
            assert trap["recommended_target"] == "staging" and trap["question"]
            confirmed = await call(
                client,
                "recommend_deployment",
                {"target": "production", "verified_nonproduction": True},
            )
            assert confirmed["recommended_target"] == "production"
            assert not confirmed["executes_deployment"]

        return {
            "verified_at": datetime.now(UTC).isoformat(),
            "python_version": sys.version.split()[0],
            "implementation_revision": hashlib.sha256(
                b"".join(
                    path.name.encode() + path.read_bytes()
                    for path in sorted((PROJECT_ROOT / "src/jeopardy_template").glob("*.py"))
                )
            ).hexdigest(),
            "scope": "Real stdio MCP clients and local HTTP API; no editor or model evaluated",
            "practice_before": before,
            "practice_after": after,
            "deployment_before": before_deploy,
            "deployment_after": after_deploy,
            "production_question": trap,
            "checks": [
                "guide discovery",
                "content-only practice edit and fresh descriptions",
                "hidden answers and explicit reveal",
                "explicit count override",
                "shortage",
                "wrapper fidelity including numeric and null values",
                "standalone deployment edit",
                "production readiness question",
            ],
        }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    evidence = asyncio.run(verify())
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(evidence, indent=2) + "\n")
    print("Workshop protocol checks passed: practice 2 -> 3; deployment preview -> staging")
    print("Protocol checks only; see evidence/README.md for editor and attendee rehearsal status.")


if __name__ == "__main__":
    main()
