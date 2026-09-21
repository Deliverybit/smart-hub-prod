#!/usr/bin/env python3
"""
Step 7 — Build and smoke-test the Docker image locally.

Usage:
    python admin_tools/test_docker.py
    python admin_tools/test_docker.py --skip-build
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
import urllib.error
import urllib.request
from http.client import RemoteDisconnected
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMAGE = "scoop52:production"
CONTAINER = "scoop52-production-test"
HOST_PORT = 8502
SECRETS_PATH = ROOT / ".streamlit" / "secrets.toml"


def _run(cmd: list[str], *, check: bool = True, echo: bool = True) -> subprocess.CompletedProcess[str]:
    if echo:
        print(f"$ {' '.join(cmd)}")
    return subprocess.run(
        cmd, cwd=ROOT, text=True, check=check, capture_output=True, encoding="utf-8", errors="replace"
    )


def _load_secrets_env() -> dict[str, str]:
    if not SECRETS_PATH.is_file():
        raise FileNotFoundError(
            f"Missing {SECRETS_PATH}. Copy .streamlit/secrets.toml.example first."
        )

    env: dict[str, str] = {"APP_ENV": "production"}
    for line in SECRETS_PATH.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key in {"APP_ENV", "ALPHA_VANTAGE_API_KEY", "DATABASE_URL", "SCREENER_SYMBOL_LIMIT"}:
            env[key] = value
    return env


def _docker_available() -> tuple[bool, str]:
    try:
        result = _run(["docker", "version"], check=False)
        if result.returncode == 0:
            return True, ""
        combined = f"{result.stdout}\n{result.stderr}".lower()
        if "dockerdesktoplinuxengine" in combined or "cannot connect" in combined:
            return False, "Docker Desktop is installed but the daemon is not running. Start Docker Desktop and retry."
        if "not recognized" in combined or "not found" in combined:
            return False, "Docker CLI is not installed or not on PATH."
        return False, (result.stderr or result.stdout or "docker version failed").strip()
    except FileNotFoundError:
        return False, "Docker CLI is not installed or not on PATH."


def _stop_existing() -> None:
    _run(["docker", "rm", "-f", CONTAINER], check=False)


def _wait_for_health(url: str, timeout_sec: int = 120) -> bool:
    deadline = time.time() + timeout_sec
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=5) as response:
                if response.status == 200:
                    return True
        except (
            urllib.error.URLError,
            TimeoutError,
            ConnectionResetError,
            ConnectionAbortedError,
            RemoteDisconnected,
            OSError,
        ):
            pass
        time.sleep(2)
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Build and smoke-test Docker image.")
    parser.add_argument("--skip-build", action="store_true")
    args = parser.parse_args()

    print("Step 7 — Docker build and local container test")
    print("-" * 60)

    ok, reason = _docker_available()
    if not ok:
        print(f"FAIL: {reason}")
        return 1

    try:
        secrets = _load_secrets_env()
    except FileNotFoundError as exc:
        print(f"FAIL: {exc}")
        return 1

    if not args.skip_build:
        build = _run(["docker", "build", "-t", IMAGE, "."])
        if build.returncode != 0:
            print(build.stderr or build.stdout)
            print("FAIL: docker build")
            return 1
        print("PASS: docker build")

    _stop_existing()

    run_cmd = [
        "docker",
        "run",
        "-d",
        "--name",
        CONTAINER,
        "-p",
        f"{HOST_PORT}:8501",
    ]
    for key, value in secrets.items():
        run_cmd.extend(["-e", f"{key}={value}"])
    run_cmd.append(IMAGE)

    run = _run(run_cmd, echo=False)
    if run.returncode != 0:
        print(run.stderr or run.stdout)
        print("FAIL: docker run")
        return 1
    print(f"PASS: container started on http://localhost:{HOST_PORT} (secrets passed via env)")

    health_url = f"http://localhost:{HOST_PORT}/_stcore/health"
    home_url = f"http://localhost:{HOST_PORT}/"
    if _wait_for_health(health_url):
        print(f"PASS: health check {health_url}")
    else:
        logs = _run(["docker", "logs", CONTAINER], check=False)
        print(logs.stdout or logs.stderr)
        print(f"FAIL: health check timed out ({health_url})")
        _stop_existing()
        return 1

    try:
        with urllib.request.urlopen(home_url, timeout=10) as response:
            html = response.read(8000).decode("utf-8", errors="ignore")
            if "Streamlit" in html or "scoop" in html.lower():
                print(f"PASS: home page reachable ({home_url})")
            else:
                print(f"WARN: home page returned {response.status} but content unexpected")
    except urllib.error.URLError as exc:
        print(f"FAIL: home page request ({home_url}): {exc}")
        _stop_existing()
        return 1

    inspect = _run(
        ["docker", "inspect", "--format", "{{.State.Health.Status}}", CONTAINER],
        check=False,
    )
    if inspect.returncode == 0:
        print(f"Container health status: {(inspect.stdout or '').strip()}")

    print("-" * 60)
    print("Overall: PASS")
    print(f"Open: http://localhost:{HOST_PORT}")
    print(f"Stop: docker rm -f {CONTAINER}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
