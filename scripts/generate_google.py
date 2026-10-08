#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 google-raffle contributors
"""Generate Nano Banana artwork via Google Cloud, using existing gcloud login."""
import argparse
import base64
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import urllib.error
import urllib.request


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True)
    parser.add_argument("--model", default="gemini-nano-banana-2.1")
    parser.add_argument("--prompt", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("Output exists; choose a new filename to preserve the generation.")
    prompt = args.prompt.read_text()
    token = subprocess.run(["gcloud", "auth", "print-access-token"], check=True,
                           capture_output=True, text=True).stdout.strip()
    endpoint = (f"https://aiplatform.googleapis.com/v1/projects/{args.project}/locations/global/"
                f"publishers/google/models/{args.model}:generateContent")
    body = {"contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {"responseModalities": ["TEXT", "IMAGE"],
                                 "imageConfig": {"aspectRatio": "1:1"}}}
    request = urllib.request.Request(endpoint, data=json.dumps(body).encode(),
                                     headers={"Authorization": "Bearer " + token,
                                              "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            result = json.load(response)
    except urllib.error.HTTPError as exc:
        error = json.loads(exc.read())
        raise SystemExit(f"Google API {exc.code}: {error.get('error', {}).get('message', 'Request failed')}")
    parts = [part for candidate in result.get("candidates", [])
             for part in candidate.get("content", {}).get("parts", [])]
    images = [p["inlineData"] for p in parts if p.get("inlineData", {}).get("mimeType", "").startswith("image/")]
    if not images:
        raise SystemExit("No image returned. " + json.dumps({"feedback": result.get("promptFeedback"),
                                                            "text": [p["text"] for p in parts if "text" in p]}))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(base64.b64decode(images[0]["data"]))
    record = {"provider": "Google Cloud", "model": args.model,
              "created_at": datetime.now(timezone.utc).isoformat(), "prompt": prompt,
              "mime_type": images[0]["mimeType"], "output": args.output.name,
              "response_id": result.get("responseId"), "usage": result.get("usageMetadata"),
              "text": [p["text"] for p in parts if "text" in p]}
    records = Path(__file__).resolve().parents[1] / "generation"
    records.mkdir(exist_ok=True)
    (records / (args.output.stem + ".json")).write_text(json.dumps(record, indent=2) + "\n")
    print(f"Generated {args.output} with {args.model}; saved generation record.")


if __name__ == "__main__":
    main()
