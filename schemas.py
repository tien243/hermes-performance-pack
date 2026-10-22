"""JSON Schema definitions for Hermes Performance Pack tools."""

RIPGREP_SEARCH_SCHEMA = {
    "name": "ripgrep_search",
    "description": (
        "Search file contents using native ripgrep (rg). "
        "Returns matched lines with file paths and line numbers. "
        "Enforces directory containment within workspace and bounds output results."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "pattern": {
                "type": "string",
                "description": "Regex or string pattern to search for.",
            },
            "path": {
                "type": "string",
                "description": "Directory or file to search in (relative to workspace or within allowed path). Defaults to current directory.",
                "default": ".",
            },
            "glob": {
                "type": "string",
                "description": "Optional glob pattern to filter files (e.g. '*.py' or '*.ts,*.tsx').",
            },
            "case_insensitive": {
                "type": "boolean",
                "description": "Case-insensitive search (default: false).",
                "default": False,
            },
            "head_limit": {
                "type": "integer",
                "description": "Max matched lines to return (default: 50, maximum: 200).",
                "default": 50,
            },
        },
        "required": ["pattern"],
    },
}

BATCH_READ_FILES_SCHEMA = {
    "name": "batch_read_files",
    "description": (
        "Read multiple text files concurrently using a bounded thread pool in a single turn. "
        "Optimized for batch I/O inspection across related files."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "paths": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of relative or absolute file paths to read (max 10 files per call).",
            },
            "max_lines_per_file": {
                "type": "integer",
                "description": "Maximum lines to read per file (default: 300, maximum: 1000).",
                "default": 300,
            },
        },
        "required": ["paths"],
    },
}
