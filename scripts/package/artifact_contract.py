#!/usr/bin/env python3
"""Stage and validate a combined Confogl and SourceMod package."""

import argparse
import hashlib
import json
import os
import re
import shutil
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZIP_DEFLATED, BadZipFile, ZipFile

MAP_PATH = Path("scripts/package/package-map.json")
STAGE = Path(".build/package-modes")
RELEASE_DIR = Path("dist/release")
PROJECT_FILES = (Path("README.md"), Path("LICENSE"), Path("NOTICES.md"))
SOURCE_ROOT = Path("addons/sourcemod")
SCRIPTING = SOURCE_ROOT / "scripting"
PLUGINS = SOURCE_ROOT / "plugins"
BUILD_RECORD = "build-record.json"
EXEC = re.compile(r'^\s*exec\s+(?:"([^"]+)"|([^\s;"]+))', re.IGNORECASE)
PLUGIN_LOAD = re.compile(r'^\s*sm\s+plugins\s+load\s+(?:"([^"]+)"|([^\s;"]+))', re.IGNORECASE)
STRIPPER = re.compile(r'^\s*(?:confogl_addcvar\s+)?stripper_cfg_path\s+"?([^\s;"]+)', re.IGNORECASE)


def load_map(root: Path) -> dict:
    return json.loads((root / MAP_PATH).read_text(encoding="utf-8"))


def relative_path(value: str) -> Path:
    path = Path(value)
    if not path.parts or path.is_absolute() or any(
        not re.fullmatch(r"[A-Za-z0-9_][A-Za-z0-9_.-]*", part) for part in path.parts
    ):
        raise ValueError(f"Invalid path in {MAP_PATH}: {value}")
    return path


def unique_paths(paths: list[Path]) -> set[Path]:
    if len({path.as_posix().casefold() for path in paths}) != len(paths):
        raise ValueError("Package paths must be unique across platforms")
    return set(paths)


def plugin_paths(manifest: dict) -> dict[Path, Path]:
    pairs = []
    for bucket, names in manifest["build"]["plugins"].items():
        destination = PLUGINS if bucket == "root" else PLUGINS / relative_path(bucket)
        for name in names:
            if not re.fullmatch(r"[A-Za-z0-9_][A-Za-z0-9_.-]*", name):
                raise ValueError(f"Invalid plugin name in {MAP_PATH}: {name}")
            pairs.append((destination / f"{name}.smx", SCRIPTING / f"{name}.sp"))
    if not pairs:
        raise ValueError(f"No product plugins in {MAP_PATH}")
    unique_paths([binary for binary, _ in pairs])
    return dict(pairs)


def require_file(root: Path, path: Path) -> Path:
    source = root / path
    if source.resolve() != source or not source.is_file() or not source.stat().st_size:
        raise ValueError(f"Missing, empty or linked file: {source}")
    return source


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_digests(root: Path, manifest: dict) -> dict[str, str]:
    sources = set(plugin_paths(manifest).values())
    # These modes keep the additional compiler inputs as vendored .inc files.
    sources.update(path.relative_to(root) for path in (root / SCRIPTING).rglob("*.inc"))
    return {path.as_posix(): digest(require_file(root, path)) for path in sorted(sources)}


def build_record(root: Path, manifest: dict, compiled: Path) -> dict:
    binaries = {}
    for path in sorted(plugin_paths(manifest)):
        file = require_file(compiled, path)
        data = file.read_bytes()
        if data[:4] != b"FFPS":
            raise ValueError(f"Invalid SMX header: {file}")
        binaries[path.as_posix()] = hashlib.sha256(data).hexdigest()
    return {
        "sources": source_digests(root, manifest),
        "binaries": binaries,
    }


def product_sources(root: Path, manifest: dict) -> set[Path]:
    plugins = plugin_paths(manifest)
    paths = []
    for mode, names in manifest["modes"].items():
        if not re.fullmatch(r"[a-z][a-z0-9_]*", mode):
            raise ValueError(f"Invalid Confogl mode identifier: {mode}")
        roles = {"confogl.cfg", "confogl_plugins.cfg", "confogl_off.cfg", f"{mode}.cfg"}
        if mode in manifest["selectable_modes"] and not roles <= set(names):
            raise ValueError(f"Missing Confogl entrypoints in {mode}: {sorted(roles - set(names))}")
        for name in names:
            if not re.fullmatch(r"[a-zA-Z0-9_][a-zA-Z0-9_.-]*\.(?:cfg|txt)", name):
                raise ValueError(f"Invalid mode configuration path: {name}")
            paths.append(Path("cfg/cfgogl") / mode / name)
    if not set(manifest["selectable_modes"]) <= manifest["modes"].keys():
        raise ValueError("Missing selectable mode declaration")

    resources = [relative_path(value) for value in manifest["resources"]]
    resource_roots = {
        SOURCE_ROOT / "data": {".cfg"},
        SOURCE_ROOT / "gamedata": {".txt"},
        SOURCE_ROOT / "translations": {".txt"},
        Path("cfg/stripper"): {".cfg"},
    }
    for resource in resources:
        if not any(resource.is_relative_to(directory) and resource.suffix in suffixes
                   for directory, suffixes in resource_roots.items()):
            raise ValueError(f"Unsupported runtime resource: {resource}")
    legal = [relative_path(name) for name in manifest["license_files"]]
    if any(not path.is_relative_to("LICENSES") or path.suffix != ".txt" for path in legal):
        raise ValueError("Additional license texts must live in LICENSES/")
    product = unique_paths([*paths, *resources, *sorted(set(plugins.values())), *PROJECT_FILES, *legal])
    unique_paths([*product, *plugins])
    for path in sorted(product):
        require_file(root, path)

    external_exec = set(manifest["external_exec"])
    external_stripper = set(manifest.get("external_stripper", []))
    local_plugins = {path.relative_to(PLUGINS).as_posix() for path in plugins}
    loaded = set()
    for relative in sorted(paths):
        if relative.suffix != ".cfg":
            continue
        for number, line in enumerate((root / relative).read_text(encoding="utf-8-sig").splitlines(), 1):
            if match := EXEC.match(line):
                target = match[1] or match[2]
                if Path("cfg") / target not in product and target not in external_exec:
                    raise ValueError(f"{relative}:{number}: undeclared exec target {target}")
            if match := STRIPPER.match(line):
                target = match[1]
                if Path(target) / "global_filters.cfg" not in product and target not in external_stripper:
                    raise ValueError(f"{relative}:{number}: missing Stripper filters for {target}")
            if match := PLUGIN_LOAD.match(line):
                target = match[1] or match[2]
                loaded.add(target if target.endswith(".smx") else f"{target}.smx")
    if missing := local_plugins - loaded:
        raise ValueError(f"Product plugins missing from Confogl load commands: {sorted(missing)}")
    return product


def load_product(root: Path, manifest: dict, compiled: Path) -> dict[Path, Path]:
    product = {path: root / path for path in product_sources(root, manifest)}
    previous = json.loads(require_file(compiled, Path(BUILD_RECORD)).read_text(encoding="utf-8"))
    if previous != build_record(root, manifest, compiled):
        raise ValueError("Compiled plugins or source inputs changed. Run make build-smx.")
    product.update({path: compiled / path for path in plugin_paths(manifest)})
    return product


def stage_product(root: Path, product: dict[Path, Path]) -> None:
    stage = root / STAGE
    if stage.resolve() != stage:
        raise ValueError(f"Staging path must not traverse symlinks: {stage}")
    stage.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(dir=stage.parent) as temporary:
        candidate = Path(temporary) / "artifact"
        for relative in sorted(product):
            destination = candidate / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(product[relative], destination)
        if stage.exists():
            shutil.rmtree(stage)
        candidate.rename(stage)


def validate_stage(root: Path, product: dict[Path, Path]) -> None:
    stage = root / STAGE
    actual = {path.relative_to(stage) for path in stage.rglob("*") if path.is_file()}
    if actual != product.keys():
        raise ValueError(f"Staging differs from package map: missing {product.keys() - actual}, extra {actual - product.keys()}")
    for path in sorted(product):
        if product[path].read_bytes() != (stage / path).read_bytes():
            raise ValueError(f"Stale staged file: {path}")


def validate_archive(product: dict[Path, Path], archive: Path) -> None:
    members = {path.as_posix(): path for path in product}
    with ZipFile(archive) as package:
        files = package.namelist()
        if len(files) != len(members) or set(files) != set(members):
            raise ValueError("ZIP entries do not match the package map")
        for name, path in members.items():
            if package.read(name) != product[path].read_bytes():
                raise ValueError(f"ZIP content differs from source: {name}")


def release(root: Path, product: dict[Path, Path], archive: Path) -> None:
    validate_stage(root, product)
    archive.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(dir=archive.parent) as temporary:
        candidate = Path(temporary) / archive.name
        with ZipFile(candidate, "w", compression=ZIP_DEFLATED) as package:
            for path in sorted(product):
                package.write(root / STAGE / path, arcname=path.as_posix())
        validate_archive(product, candidate)
        os.replace(candidate, archive)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("validate-modes", "package-modes", "release", "validate-artifact"))
    parser.add_argument("--basename")
    parser.add_argument("--build-dir", type=Path, default=Path(".build/smx"))
    args = parser.parse_args()
    if args.operation in {"release", "validate-artifact"} and (
        not args.basename or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", args.basename)
    ):
        parser.error("expected a ZIP basename without path separators")

    root = Path(__file__).resolve().parents[2]
    archive = root / RELEASE_DIR / f"{args.basename}.zip"
    try:
        manifest = load_map(root)
        if args.operation == "validate-modes":
            product_sources(root, manifest)
            print("validate-modes: OK")
            return
        product = load_product(root, manifest, (root / args.build_dir).resolve())
        if args.operation == "package-modes":
            stage_product(root, product)
            validate_stage(root, product)
        if args.operation == "release":
            release(root, product, archive)
            print(archive)
        if args.operation == "validate-artifact":
            validate_archive(product, archive)
    except (OSError, ValueError, BadZipFile) as error:
        parser.exit(1, f"{error}\n")
    print(f"{args.operation}: OK")


if __name__ == "__main__":
    main()
