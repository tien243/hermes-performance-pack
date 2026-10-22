"""Tool implementations for Hermes Performance Pack."""

import json
import os
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, List


def _find_ripgrep_binary() -> str:
    """Find installed ripgrep binary."""
    # Check PATH first
    rg_path = shutil.which("rg") or shutil.which("rg.exe")
    if rg_path:
        return rg_path

    # Common Windows locations (e.g. bundled with Hermes, VSCode, Scoop, etc.)
    common_paths = [
        os.path.expandvars(r"%LOCALAPPDATA%\hermes\bin\rg.exe"),
        os.path.expandvars(r"%USERPROFILE%\AppData\Local\Programs\Microsoft VS Code\resources\app\node_modules.asar.unpacked\@vscode\ripgrep\bin\rg.exe"),
        r"C:\Program Files\Git\usr\bin\grep.exe",
    ]
    for p in common_paths:
        if os.path.isfile(p):
            return p
    return ""


def ripgrep_search(pattern: str, path: str = ".", glob: str = "", case_insensitive: bool = False, head_limit: int = 50, **kwargs: Any) -> str:
    """Execute high-speed search using ripgrep binary."""
    rg_bin = _find_ripgrep_binary()
    if not rg_bin:
        return json.dumps({
            "status": "error",
            "message": "ripgrep binary ('rg') was not found on PATH. Please install ripgrep or ensure rg is accessible."
        })

    cmd = [rg_bin, "--line-number", "--color", "never", "--no-heading"]

    if case_insensitive:
        cmd.append("-i")

    if glob:
        for g in glob.split(","):
            g_clean = g.strip()
            if g_clean:
                cmd.extend(["-g", g_clean])

    # Add head limit safety
    limit = min(max(1, head_limit), 200)
    cmd.extend(["-m", str(limit)])

    cmd.append(pattern)
    cmd.append(path)

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
            "path": path,
            "match_count": len(lines),
            "matches": lines,
            "truncated": len(proc.stdout.splitlines()) > limit
        })
    except subprocess.TimeoutExpired:
        return json.dumps({"status": "error", "message": "Search timed out after 15 seconds."})
    except Exception as exc:
        return json.dumps({"status": "error", "message": str(exc)})


def _read_single_file(file_path: str, max_lines: int) -> Dict[str, Any]:
    """Read a single file with safe line limits."""
    try:
        if not os.path.exists(file_path):
            return {"path": file_path, "status": "error", "error": "File does not exist"}
        if os.path.isdir(file_path):
            return {"path": file_path, "status": "error", "error": "Path is a directory"}

        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            lines = []
            for i, line in enumerate(f):
                if i >= max_lines:
                    break
                lines.append(line)
        return {
            "path": file_path,
            "status": "ok",
            "line_count": len(lines),
            "content": "".join(lines)
        }
    except Exception as e:
        return {"path": file_path, "status": "error", "error": str(e)}


def batch_read_files(paths: List[str], max_lines_per_file: int = 300, **kwargs: Any) -> str:
    """Read multiple files concurrently using a thread pool."""
    if not paths:
        return json.dumps({"status": "error", "message": "No file paths provided."})

    capped_paths = paths[:10]  # Cap at 10 files per batch
    results = []

    with ThreadPoolExecutor(max_workers=min(len(capped_paths), 5)) as executor:
        futures = [executor.submit(_read_single_file, p, max_lines_per_file) for p in capped_paths]
        for f in futures:
            results.append(f.result())

    return json.dumps({
        "status": "ok",
        "files_read": len(results),
        "results": results
    })


def prune_tool_context(reason: str, key_facts_to_retain: str = "", **kwargs: Any) -> str:
    """Pruning marker tool: acknowledges that earlier bulky outputs are spent and captures facts."""
    return json.dumps({
        "status": "ok",
        "action": "pruned",
        "reason": reason,
        "retained_facts": key_facts_to_retain or "No explicit facts provided.",
        "note": "Context marked for distillation. Prior large file reads or searches can now be treated as referenced."
    })
