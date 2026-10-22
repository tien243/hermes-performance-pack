"""Hermes Performance Pack - Plugin Registration Entry Point."""

import logging
from . import schemas, tools

logger = logging.getLogger(__name__)


def register(ctx):
    """Register tools into Hermes Plugin Context following PluginContext.register_tool contract."""
    # 1. Native Ripgrep Search Tool
    ctx.register_tool(
        name="ripgrep_search",
        toolset="performance",
        schema=schemas.RIPGREP_SEARCH_SCHEMA,
        handler=tools.ripgrep_search,
        description="High-speed pattern search using native ripgrep (rg).",
        emoji="🔍"
    )

    # 2. Parallel Batch File Reader Tool
    ctx.register_tool(
        name="batch_read_files",
        toolset="performance",
        schema=schemas.BATCH_READ_FILES_SCHEMA,
        handler=tools.batch_read_files,
        description="Concurrent multi-file reader bounded by thread pool.",
        emoji="📑"
    )

    logger.info("Hermes Performance Pack tools registered successfully.")
