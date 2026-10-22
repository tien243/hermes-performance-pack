"""Tool implementations for Hermes Performance Pack with security and bounds validation."""

import json
import os
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Dict, List, Optional


def _is_safe_path(target_path: str, base_dir: Optional[str] = None) -> tuple[bool, Path]:
    """Validate path and resolve canonical target."""
    try:
        target = Path(target_path).resolve()
        
        # If relative path is passed, anchor it to base_dir or current working directory
        if not os.path.isabs(target_path):
            base = Path(base_dir or os.getcwd()).resolve()
            target = (base / target_path).resolve()
            # Must remain within base_dir
            if not (target == base or base in target.parents or target.is_relative_to(base)):
                return False, target

        return True, target
    except Exception:
        return False, Path(target_path)


def _find_ripgrep_binary() -> str:
    """Find installed ripgrep binary."""
    rg_path = shutil.which("rg") or shutil.which("rg.exe")
    if rg_path:
        return rg_path

    # Common Windows locations
    candidates = [
        os.path.expandvars(r"%LOCALAPPDATA%\hermes\bin\rg.exe"),
        os.path.expandvars(r"%USERPROFILE%\AppData\Local\Programs\Microsoft VS Code\resources\app\node_modules.asar.unpacked\@vscode\ripgrep\bin\rg.exe"),
    ]
    for p in candidates:
        if os.path.isfile(p):
            return p
    return ""


def ripgrep_search(pattern: str, path: str = ".", glob: str = "", case_insensitive: bool = False, head_limit: int = 50, **kwargs: Any) -> str:
    """Execute high-speed search using ripgrep binary with strict bounds and path resolution."""
    if not pattern:
        return json.dumps({"status": "error", "message": "Search pattern cannot be empty."})

    safe, resolved_path = _is_safe_path(path)
    if not safe:
        return json.dumps({
            "status": "error",
            "message": f"Path traversal rejected: '{path}' resolves outside the allowed workspace boundary."
        })

    if not resolved_path.exists():
        return json.dumps({
            "status": "error",
            "message": f"Path does not exist: {str(resolved_path)}"
        })

    rg_bin = _find_ripgrep_binary()
    if not rg_bin:
        return json.dumps({
            "status": "error",
            "message": "ripgrep binary ('rg') not found on PATH or Hermes tool store."
        })

    cmd = [rg_bin, "--line-number", "--color", "never", "--no-heading"]

    if case_insensitive:
        cmd.append("-i")

    if glob:
        for g in glob.split(","):
            g_clean = g.strip()
            if g_clean:
                cmd.extend(["-g", g_clean])

    limit = min(max(1, int(head_limit)), 200)
    cmd.extend(["-m", str(limit)])

    cmd.append(pattern)
    cmd.append(str(resolved_path))

    try:
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=15.0,
            check=False,
            encoding="utf-8",
            errors="replace"
        )

        lines = proc.stdout.splitlines()[:limit]
        return json.dumps({
            "status": "ok",
            "pattern": pattern,
            "path": str(resolved_path),
            "match_count": len(lines),
            "matches": lines,
            "truncated": len(proc.stdout.splitlines()) > limit
        })
    except subprocess.TimeoutExpired:
        return json.dumps({"status": "error", "message": "Search timed out after 15 seconds."})
    except Exception as exc:
        return json.dumps({"status": "error", "message": str(exc)})


def _read_single_file(file_path: str, max_lines: int) -> Dict[str, Any]:
    """Read a single file with safe line limits and binary detection."""
    try:
        safe, target = _is_safe_path(file_path)
        if not safe:
            return {"path": file_path, "status": "error", "error": "Path traversal rejected"}

        if not target.exists():
            return {"path": str(target), "status": "error", "error": "File does not exist"}
        if target.is_dir():
            return {"path": str(target), "status": "error", "error": "Path is a directory"}

        # Size check: refuse files larger than 10MB to avoid memory exhaustion
        if target.stat().st_size > 10 * 1024 * 1024:
            return {"path": str(target), "status": "error", "error": "File exceeds 10MB limit"}

        with open(target, "r", encoding="utf-8", errors="replace") as f:
            lines = []
            for i, line in enumerate(f):
                if i >= max_lines:
                    break
                lines.append(line)

        return {
            "path": str(target),
            "status": "ok",
            "line_count": len(lines),
            "content": "".join(lines)
        }
    except Exception as e:
        return {"path": file_path, "status": "error", "error": str(e)}


def batch_read_files(paths: List[str], max_lines_per_file: int = 300, **kwargs: Any) -> str:
    """Read multiple files concurrently using a bounded thread pool."""
    if not isinstance(paths, list) or not paths:
        return json.dumps({"status": "error", "message": "No file paths provided."})

    capped_paths = paths[:10]  # Cap at 10 files per batch
    safe_max_lines = min(max(1, int(max_lines_per_file)), 1000)
    results = []

    with ThreadPoolExecutor(max_workers=min(len(capped_paths), 5)) as executor:
        future_to_path = {executor.submit(_read_single_file, p, safe_max_lines): p for p in capped_paths}
        for future in as_completed(future_to_path):
            results.append(future.result())

    # Sort results to match original request order
    path_order = {p: idx for idx, p in enumerate(capped_paths)}
    results.sort(key=lambda r: path_order.get(r.get("path"), 999))

    return json.dumps({
        "status": "ok",
        "files_requested": len(capped_paths),
        "files_read": len(results),
        "results": results
    })
