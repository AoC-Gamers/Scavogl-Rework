#!/usr/bin/env python3

import argparse
import platform as py_platform
import shutil
import tarfile
import urllib.request
import zipfile
from pathlib import Path


def build_url(platform: str, version: str) -> str:
    if platform == "windows":
        return f"https://www.sourcemod.net/latest.php?os=windows&version={version}"
    if platform == "linux":
        return f"https://www.sourcemod.net/latest.php?os=linux&version={version}"
    raise ValueError(f"Unsupported platform: {platform}")


def detect_platform() -> str:
    system = py_platform.system().lower()
    if system.startswith("win"):
        return "windows"
    if system == "linux":
        return "linux"
    raise RuntimeError(f"Unsupported platform: {py_platform.system()}")


def download(url: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "*/*"})
    with urllib.request.urlopen(request, timeout=60) as response, destination.open("wb") as fh:
        shutil.copyfileobj(response, fh)


def extract_archive(archive_path: Path, output_dir: Path, platform: str) -> None:
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    if platform == "windows":
        with zipfile.ZipFile(archive_path, "r") as zf:
            zf.extractall(output_dir)
        return
    with tarfile.open(archive_path, "r:gz") as tf:
        tf.extractall(output_dir)


def main() -> int:
    parser = argparse.ArgumentParser(description="Download and extract SourceMod compiler dependencies.")
    parser.add_argument("--root", default=".")
    parser.add_argument("--platform", choices=("windows", "linux"))
    parser.add_argument("--version", default="1.12")
    parser.add_argument("--archive-url", default="")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    deps_dir = root / ".deps" / "smx"
    platform = args.platform or detect_platform()
    archive_name = "sourcemod-windows.zip" if platform == "windows" else "sourcemod-linux.tar.gz"
    extract_dir = deps_dir / f"sourcemod-{platform}"
    archive_path = deps_dir / archive_name
    download(args.archive_url or build_url(platform, args.version), archive_path)
    extract_archive(archive_path, extract_dir, platform)
    print(f"SourceMod {platform} extracted to: {extract_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
