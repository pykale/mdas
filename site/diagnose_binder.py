"""Compare local/public Binder inputs; optionally observe one launch event stream."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import time
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent.parent
REPO = "pykale/mdas"
REQUIRED = [".binder/runtime.txt", ".binder/requirements.txt",
            "notebooks/MDAS/cancer/survival.ipynb",
            "notebooks/MDAS/cancer/synthetic_data_generation.py"]


def request(url, accept="application/vnd.github+json", timeout=15):
    return urlopen(Request(url, headers={"Accept": accept, "User-Agent": "MDAS-Binder-diagnostic"}), timeout=timeout)


def redact(message):
    # Ready events contain server tokens. Only log phase/message, never URL/token.
    return re.sub(r"(token[=:\s]+)[^\s&]+", r"\1[redacted]", str(message), flags=re.I)


def observe_launch(url, timeout=600):
    events = []
    started = time.monotonic()
    try:
        # Binder can send only a heartbeat between build steps. Allow longer
        # socket reads while keeping a separate overall observation deadline.
        with request(url, "text/event-stream", timeout=min(60, timeout)) as response:
            events.append({"http_status": response.status, "endpoint": response.geturl()})
            for raw in response:
                if time.monotonic() - started > timeout:
                    events.append({"result": f"Observation stopped after {timeout} seconds; build/launch outcome is still unknown."})
                    print(json.dumps(events[-1]), flush=True)
                    break
                line = raw.decode("utf-8", errors="replace").strip()
                if not line.startswith("data:"):
                    continue
                try:
                    event = json.loads(line[5:])
                except ValueError:
                    continue
                message = redact(event.get("message", ""))[:5000]
                events.append({"phase": event.get("phase"), "message": message})
                print(json.dumps(events[-1]), flush=True)
                if event.get("phase") in {"failed", "ready"}:
                    break
    except (HTTPError, URLError, TimeoutError) as error:
        events.append({"network_error": type(error).__name__, "detail": redact(str(error))})
        print(json.dumps(events[-1]), flush=True)
    return events


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ref", default=os.environ.get("MDAS_BINDER_REF", "main"))
    parser.add_argument("--launch", action="store_true", help="Explicitly request and observe one public Binder launch")
    parser.add_argument("--timeout", type=int, default=600, metavar="SECONDS",
                        help="Overall launch observation window (default: 600 seconds)")
    args = parser.parse_args()
    if args.timeout <= 0:
        parser.error("--timeout must be greater than zero")
    with request(f"https://api.github.com/repos/{REPO}") as response:
        metadata = json.load(response)
    with request(f"https://api.github.com/repos/{REPO}/git/trees/{quote(args.ref, safe='')}?recursive=1") as response:
        tree = json.load(response)
    blobs = {entry["path"]: entry["sha"] for entry in tree["tree"] if entry["type"] == "blob"}
    files = []
    for name in REQUIRED:
        path = ROOT / name
        contents = path.read_bytes() if path.is_file() else None
        def blob_sha(data):
            return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

        local_sha = blob_sha(contents) if contents is not None else None
        # Windows Git checkouts can use CRLF although GitHub stores LF text.
        normalized_sha = blob_sha(contents.replace(b"\r\n", b"\n")) if contents is not None else None
        files.append({"path": name, "local_exists": contents is not None,
                      "remote_exists": name in blobs,
                      "byte_identical_remote": local_sha == blobs.get(name) if name in blobs else False,
                      "matches_remote_after_lf_normalisation": normalized_sha == blobs.get(name) if name in blobs else False})
    missing = [file["path"] for file in files if not file["remote_exists"]]
    report = {"repository": REPO, "public": not metadata["private"], "ref": args.ref,
              "commit": tree["sha"], "tree_truncated": tree.get("truncated", False), "files": files}
    if missing:
        report["readiness"] = "Cannot verify incomplete GitHub tree" if tree.get("truncated") else "Blocked: required files absent from public revision"
    else:
        report["readiness"] = "Files available; build, dependencies and kernel still require runtime testing"
    print(json.dumps(report, indent=2), flush=True)
    if args.launch:
        binder = os.environ.get("MDAS_BINDER_URL", "https://mybinder.org").rstrip("/")
        report["launch_events"] = observe_launch(f"{binder}/build/gh/{REPO}/{quote(args.ref, safe='')}", args.timeout)
        terminal = [event["phase"] for event in report["launch_events"] if event.get("phase") in {"ready", "failed"}]
        report["launch_result"] = terminal[-1] if terminal else "incomplete: no ready/failed event observed"
        print(f"Launch result: {report['launch_result']}", flush=True)
        messages = "\n".join(event.get("message", "") for event in report["launch_events"])
        if "No environment specification found" in messages:
            report["failure_phase"] = "environment discovery, before package installation or kernel startup"
    output = ROOT / "site/_build/binder-diagnostic.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Diagnostic report: {output}")


if __name__ == "__main__":
    try:
        main()
    except (HTTPError, URLError, TimeoutError) as error:
        raise SystemExit(f"Diagnostic request failed: {redact(str(error))}")
