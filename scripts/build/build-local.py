#!/usr/bin/env python3

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "package"))
from artifact_contract import BUILD_RECORD, build_record, load_map, plugin_paths, source_digests


def run_spcomp(spcomp: Path, source_file: Path, include_dirs: list[Path], output_file: Path, compile_log: Path) -> None:
    cmd = [str(spcomp), str(source_file)]
    for include_dir in include_dirs:
        cmd.append(f"-i{include_dir}")
    cmd.append(f"-o{output_file}")

    rel_output = output_file.as_posix().split("/addons/", 1)[-1]
    print(f"Compiling {source_file.name} -> addons/{rel_output}", flush=True)
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)

    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)

    with compile_log.open("a", encoding="utf-8", newline="") as fh:
        if result.stdout:
            fh.write(result.stdout)
        if result.stderr:
            fh.write(result.stderr)

    if result.returncode != 0:
        raise RuntimeError(f"spcomp failed for {source_file.name}")
    with output_file.open("rb") as binary:
        if binary.read(4) != b"FFPS":
            raise RuntimeError(f"Expected a valid SMX header: {output_file}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile the game mode plugins listed in the package map.")
    parser.add_argument("--root", default=".")
    parser.add_argument("--spcomp", required=True)
    parser.add_argument("--output-root", default=".build/smx")
    parser.add_argument("--compile-log", required=True)
    args = parser.parse_args()

    root = Path(args.root).resolve()
    spcomp = Path(args.spcomp).resolve()
    output_root = (root / args.output_root).resolve()
    compile_log = (root / args.compile_log).resolve()

    if not spcomp.exists():
        raise FileNotFoundError(f"spcomp not found: {spcomp}")

    source_mod_include_dir = spcomp.parent / "include"
    if not source_mod_include_dir.exists():
        raise FileNotFoundError(f"SourceMod include dir not found: {source_mod_include_dir}")

    manifest = load_map(root)
    plugins = plugin_paths(manifest)
    source_root = root / "addons" / "sourcemod"
    build_root = root / ".build"
    if not output_root.is_relative_to(build_root) or output_root == build_root:
        raise ValueError(f"Build output must be a subdirectory of {build_root}: {output_root}")
    if not compile_log.is_relative_to(build_root) or compile_log.is_relative_to(output_root):
        raise ValueError(f"Compile log must be within {build_root} and outside {output_root}: {compile_log}")

    scripting_dir = source_root / "scripting"
    include_dir = scripting_dir / "include"
    compile_log.parent.mkdir(parents=True, exist_ok=True)
    compile_log.write_text("", encoding="utf-8")

    include_dirs = [include_dir, scripting_dir, source_mod_include_dir]
    output_root.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(dir=output_root.parent) as temporary:
        candidate = Path(temporary) / "smx"
        inputs = source_digests(root, manifest)
        for binary, source in plugins.items():
            output_file = candidate / binary
            output_file.parent.mkdir(parents=True, exist_ok=True)
            run_spcomp(spcomp, root / source, include_dirs, output_file, compile_log)
        record = build_record(root, manifest, candidate)
        if record["sources"] != inputs:
            raise RuntimeError("Source inputs changed during compilation. Run make build-smx.")
        (candidate / BUILD_RECORD).write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
        if output_root.exists():
            shutil.rmtree(output_root)
        candidate.rename(output_root)

    print()
    print(f"Build local completed in: {output_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
