"""JSON Schema definitions for Hermes Performance Pack tools."""

RIPGREP_SEARCH_SCHEMA = {
    "name": "ripgrep_search",
    "description": (
        "High-performance regex and pattern search across files using native ripgrep (rg). "
        "Supports file glob filtering, max head limits, case-insensitivity, and line numbers. "
        "Much faster than shell grep or find."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "pattern": {
                "type": "string",
                "description": "Regular expression or literal text to search for.",
            },
            "path": {
                "type": "string",
                "description": "Directory or file path to search in (relative to workspace or absolute). Defaults to current directory.",
                "default": ".",
            },
            "glob": {
                "type": "string",
                "description": "Optional glob filter for file names (e.g. '*.py', '*.ts,*.tsx').",
            },
            "case_insensitive": {
                "type": "boolean",
                "description": "Whether to perform case-insensitive search (default: false).",
                "default": False,
            },
            "head_limit": {
                "type": "integer",
                "description": "Maximum number of matched lines to return (default: 50, max: 200).",
                "default": 50,
            },
        },
        "required": ["pattern"],
    },
}

BATCH_READ_FILES_SCHEMA = {
    "name": "batch_read_files",
    "description": (
        "Read multiple text files concurrently in a single turn. "
        "Prevents multiple sequential round-trips when inspecting multiple related files."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "paths": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of file paths to read concurrently.",
            },
            "max_lines_per_file": {
                "type": "integer",
                "description": "Max lines to read per file to prevent prompt flooding (default: 300).",
                "default": 300,
            },
        },
        "required": ["paths"],
    },
}

PRUNE_TOOL_CONTEXT_SCHEMA = {
    "name": "prune_tool_context",
    "description": (
        "Signal to summarize and trim bulky, spent tool results from the active conversation context. "
        "Use this after a large file dump or search phase has concluded to keep the context window fast and lean."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "reason": {
                "type": "string",
                "description": "Short explanation of which spent outputs can be condensed (e.g. 'Completed reading file logs').",
            },
            "key_facts_to_retain": {
                "type": "string",
                "description": "Summary of essential numbers, paths, or findings that must be preserved.",
            },
        },
        "required": ["reason"],
    },
}
