"""Hermes Performance Pack - Plugin Registration Entry Point."""

import logging
from . import schemas, tools

logger = logging.getLogger(__name__)


def register(ctx):
    """Register tools and hooks into Hermes Plugin Context."""
    # 1. Native Ripgrep Search Tool
    ctx.register_tool(
        name="ripgrep_search",
        toolset="performance",
        schema=schemas.RIPGREP_SEARCH_SCHEMA,
        handler=tools.ripgrep_search
    )

    # 2. Parallel Batch File Reader Tool
    ctx.register_tool(
        name="batch_read_files",
        toolset="performance",
        schema=schemas.BATCH_READ_FILES_SCHEMA,
        handler=tools.batch_read_files
    )

    # 3. Context Pruning Marker Tool
    ctx.register_tool(
        name="prune_tool_context",
        toolset="performance",
        schema=schemas.PRUNE_TOOL_CONTEXT_SCHEMA,
        handler=tools.prune_tool_context
    )

    logger.info("Hermes Performance Pack tools registered successfully.")
