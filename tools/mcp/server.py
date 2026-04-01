#!/usr/bin/env python3
"""
AIGC Knowledge Base MCP Server

A local stdio MCP server for searching and retrieving knowledge from the repository.
Designed for cross-machine sync via Git with local-only execution.
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

# Server instance
server = Server("aigc-knowledge")

# Configuration
REPO_ROOT = Path(__file__).parent.parent.parent.resolve()
INDEX_DIR = Path(__file__).parent / ".knowledge_index"
INDEX_FILE = INDEX_DIR / "index.json"

# Knowledge source directories (relative to repo root)
KNOWLEDGE_SOURCES = ["wiki", "docs", "raw_data"]

# Supported file extensions
SUPPORTED_EXTENSIONS = {".md", ".txt", ".mdx"}


def ensure_index_dir() -> None:
    """Ensure the index directory exists."""
    INDEX_DIR.mkdir(parents=True, exist_ok=True)


def get_file_mtime(path: Path) -> str:
    """Get file modification time as ISO string."""
    try:
        mtime = path.stat().st_mtime
        return datetime.fromtimestamp(mtime).isoformat()
    except OSError:
        return ""


def extract_title(content: str, path: Path) -> str:
    """Extract title from content or use filename."""
    # Try to find markdown title
    lines = content.split("\n")
    for line in lines[:10]:  # Check first 10 lines
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
    # Fallback to filename without extension
    return path.stem.replace("-", " ").replace("_", " ").title()


def extract_yaml_frontmatter(content: str) -> dict[str, Any]:
    """Extract YAML frontmatter if present."""
    if not content.startswith("---"):
        return {}
    try:
        end_idx = content.index("---", 3)
        frontmatter_text = content[3:end_idx].strip()
        # Simple parsing without yaml dependency
        result = {}
        for line in frontmatter_text.split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                result[key.strip()] = value.strip().strip('"').strip("'")
        return result
    except (ValueError, IndexError):
        return {}


def scan_knowledge_files() -> list[dict[str, Any]]:
    """Scan all knowledge source directories and return file metadata."""
    files = []
    for source_dir in KNOWLEDGE_SOURCES:
        source_path = REPO_ROOT / source_dir
        if not source_path.exists():
            continue
        for ext in SUPPORTED_EXTENSIONS:
            for file_path in source_path.rglob(f"*{ext}"):
                if file_path.is_file():
                    rel_path = file_path.relative_to(REPO_ROOT)
                    try:
                        content = file_path.read_text(encoding="utf-8", errors="ignore")
                        frontmatter = extract_yaml_frontmatter(content)
                        title = frontmatter.get("title") or extract_title(content, file_path)
                        files.append({
                            "path": str(rel_path),
                            "title": title,
                            "size": file_path.stat().st_size,
                            "updated_at": get_file_mtime(file_path),
                            "extension": ext,
                            "source": source_dir,
                        })
                    except Exception:
                        continue
    return files


def build_index() -> dict[str, Any]:
    """Build the knowledge index."""
    files = scan_knowledge_files()
    index = {
        "version": "1.0",
        "built_at": datetime.now().isoformat(),
        "repo_root": str(REPO_ROOT),
        "sources": KNOWLEDGE_SOURCES,
        "supported_extensions": list(SUPPORTED_EXTENSIONS),
        "file_count": len(files),
        "files": files,
    }
    return index


def save_index(index: dict[str, Any]) -> None:
    """Save index to disk."""
    ensure_index_dir()
    INDEX_FILE.write_text(json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8")


def load_index() -> dict[str, Any] | None:
    """Load index from disk."""
    if not INDEX_FILE.exists():
        return None
    try:
        return json.loads(INDEX_FILE.read_text(encoding="utf-8"))
    except Exception:
        return None


def get_or_build_index() -> dict[str, Any]:
    """Get existing index or build a new one."""
    index = load_index()
    if index is None:
        index = build_index()
        save_index(index)
    return index


def search_content(query: str, top_k: int = 10, path_filter: str | None = None) -> list[dict[str, Any]]:
    """
    Search knowledge files for matching content.
    
    Uses simple text matching: title/path keywords + content search.
    Returns scored results with snippets.
    """
    index = get_or_build_index()
    query_lower = query.lower()
    query_words = query_lower.split()
    results = []
    
    for file_info in index.get("files", []):
        file_path = file_info["path"]
        
        # Apply path filter if specified
        if path_filter and path_filter not in file_path:
            continue
        
        full_path = REPO_ROOT / file_path
        if not full_path.exists():
            continue
        
        try:
            content = full_path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        
        content_lower = content.lower()
        title_lower = file_info.get("title", "").lower()
        path_lower = file_path.lower()
        
        # Calculate relevance score
        score = 0.0
        
        # Title exact match (highest weight)
        if query_lower in title_lower:
            score += 10.0
        
        # Title word matches
        for word in query_words:
            if word in title_lower:
                score += 3.0
        
        # Path matches
        for word in query_words:
            if word in path_lower:
                score += 2.0
        
        # Content matches
        content_match_count = 0
        for word in query_words:
            count = content_lower.count(word)
            if count > 0:
                content_match_count += min(count, 10)  # Cap at 10 to avoid spam
                score += min(count * 0.5, 5.0)
        
        if score == 0:
            continue
        
        # Extract snippet around first match
        snippet = ""
        for word in query_words:
            idx = content_lower.find(word)
            if idx >= 0:
                start = max(0, idx - 100)
                end = min(len(content), idx + 200)
                snippet = content[start:end].strip()
                if start > 0:
                    snippet = "..." + snippet
                if end < len(content):
                    snippet = snippet + "..."
                break
        
        if not snippet and content:
            # No match found in content, use beginning
            snippet = content[:300].strip() + "..."
        
        results.append({
            "path": file_path,
            "title": file_info.get("title", ""),
            "score": round(score, 2),
            "snippet": snippet,
            "updated_at": file_info.get("updated_at", ""),
            "source": file_info.get("source", ""),
        })
    
    # Sort by score descending
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]


# Tool definitions
@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available knowledge tools."""
    return [
        Tool(
            name="search_knowledge",
            description=(
                "Search the AIGC knowledge base for documents matching a query. "
                "Use this when the user asks about: AI image generation prompts, "
                "Midjourney/Stable Diffusion techniques, video generation, AI tools usage, "
                "or any content that might be documented in this repository's wiki, docs, or raw_data folders. "
                "Returns ranked results with path, title, relevance score, and content snippets."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query - keywords or phrases to find in the knowledge base"
                    },
                    "top_k": {
                        "type": "integer",
                        "description": "Maximum number of results to return (default: 10)",
                        "default": 10,
                        "minimum": 1,
                        "maximum": 50
                    },
                    "path_filter": {
                        "type": "string",
                        "description": "Optional: filter results to paths containing this string (e.g., 'midjourney', 'wiki/prompt')"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="read_knowledge_file",
            description=(
                "Read the full content of a specific knowledge file. "
                "Use this after search_knowledge returns a relevant file path, "
                "or when you know the exact path of a document to read. "
                "Returns the complete file content (truncated at 50KB for very large files)."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Relative path to the file from repository root (e.g., 'wiki/prompt/midjourney/midjourney-prompt-guide.md')"
                    }
                },
                "required": ["path"]
            }
        ),
        Tool(
            name="list_knowledge_sources",
            description=(
                "List all files and directories in the knowledge base. "
                "Use this to explore what knowledge is available, browse topics, "
                "or find files when you're not sure what to search for. "
                "Can optionally filter to a specific subdirectory."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Optional: subdirectory to list (e.g., 'wiki/prompt', 'raw_data/ai_image'). Leave empty to list all sources."
                    }
                }
            }
        ),
        Tool(
            name="get_knowledge_status",
            description=(
                "Get status information about the knowledge index. "
                "Use this to check: total document count, last index update time, "
                "which directories are indexed, and supported file formats. "
                "Useful for debugging or understanding knowledge base coverage."
            ),
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Handle tool calls."""
    
    if name == "search_knowledge":
        query = arguments.get("query", "")
        top_k = arguments.get("top_k", 10)
        path_filter = arguments.get("path_filter")
        
        if not query:
            return [TextContent(type="text", text="Error: query parameter is required")]
        
        results = search_content(query, top_k, path_filter)
        
        if not results:
            return [TextContent(
                type="text",
                text=f"No results found for query: '{query}'\n\nTry different keywords or use list_knowledge_sources to browse available content."
            )]
        
        output = {
            "query": query,
            "result_count": len(results),
            "results": results
        }
        return [TextContent(type="text", text=json.dumps(output, indent=2, ensure_ascii=False))]
    
    elif name == "read_knowledge_file":
        path = arguments.get("path", "")
        if not path:
            return [TextContent(type="text", text="Error: path parameter is required")]
        
        # Security: prevent path traversal
        try:
            full_path = (REPO_ROOT / path).resolve()
            if not str(full_path).startswith(str(REPO_ROOT)):
                return [TextContent(type="text", text="Error: path must be within the repository")]
        except Exception:
            return [TextContent(type="text", text="Error: invalid path")]
        
        if not full_path.exists():
            return [TextContent(type="text", text=f"Error: file not found: {path}")]
        
        if not full_path.is_file():
            return [TextContent(type="text", text=f"Error: path is not a file: {path}")]
        
        try:
            content = full_path.read_text(encoding="utf-8", errors="ignore")
            # Truncate very large files
            max_size = 50 * 1024  # 50KB
            truncated = False
            if len(content) > max_size:
                content = content[:max_size]
                truncated = True
            
            output = {
                "path": path,
                "size": full_path.stat().st_size,
                "updated_at": get_file_mtime(full_path),
                "truncated": truncated,
                "content": content
            }
            return [TextContent(type="text", text=json.dumps(output, indent=2, ensure_ascii=False))]
        except Exception as e:
            return [TextContent(type="text", text=f"Error reading file: {e}")]
    
    elif name == "list_knowledge_sources":
        subpath = arguments.get("path", "")
        
        if subpath:
            # List specific subdirectory
            target_path = REPO_ROOT / subpath
            if not target_path.exists():
                return [TextContent(type="text", text=f"Error: path not found: {subpath}")]
            if not target_path.is_dir():
                return [TextContent(type="text", text=f"Error: path is not a directory: {subpath}")]
            
            entries = []
            for item in sorted(target_path.iterdir()):
                rel_path = item.relative_to(REPO_ROOT)
                entry = {
                    "path": str(rel_path),
                    "type": "directory" if item.is_dir() else "file",
                    "name": item.name,
                }
                if item.is_file():
                    entry["size"] = item.stat().st_size
                    entry["updated_at"] = get_file_mtime(item)
                entries.append(entry)
            
            output = {
                "base_path": subpath,
                "entry_count": len(entries),
                "entries": entries
            }
        else:
            # List all knowledge sources
            index = get_or_build_index()
            sources_info = []
            for source in KNOWLEDGE_SOURCES:
                source_path = REPO_ROOT / source
                if source_path.exists():
                    file_count = sum(1 for f in index.get("files", []) if f.get("source") == source)
                    sources_info.append({
                        "path": source,
                        "exists": True,
                        "file_count": file_count
                    })
                else:
                    sources_info.append({
                        "path": source,
                        "exists": False,
                        "file_count": 0
                    })
            
            output = {
                "knowledge_sources": sources_info,
                "total_files": index.get("file_count", 0),
                "hint": "Use path parameter to list contents of a specific directory"
            }
        
        return [TextContent(type="text", text=json.dumps(output, indent=2, ensure_ascii=False))]
    
    elif name == "get_knowledge_status":
        index = get_or_build_index()
        
        # Count files by source
        source_counts = {}
        for f in index.get("files", []):
            source = f.get("source", "unknown")
            source_counts[source] = source_counts.get(source, 0) + 1
        
        # Count files by extension
        ext_counts = {}
        for f in index.get("files", []):
            ext = f.get("extension", "unknown")
            ext_counts[ext] = ext_counts.get(ext, 0) + 1
        
        output = {
            "status": "ready",
            "index_version": index.get("version", "unknown"),
            "last_built": index.get("built_at", "unknown"),
            "repo_root": str(REPO_ROOT),
            "index_location": str(INDEX_FILE),
            "total_files": index.get("file_count", 0),
            "files_by_source": source_counts,
            "files_by_extension": ext_counts,
            "knowledge_sources": index.get("sources", []),
            "supported_extensions": index.get("supported_extensions", [])
        }
        return [TextContent(type="text", text=json.dumps(output, indent=2, ensure_ascii=False))]
    
    else:
        return [TextContent(type="text", text=f"Error: unknown tool: {name}")]


def rebuild_index() -> dict[str, Any]:
    """Rebuild the knowledge index (called by script)."""
    index = build_index()
    save_index(index)
    return index


def main():
    """Main entry point."""
    import asyncio
    
    # Check for rebuild command
    if len(sys.argv) > 1 and sys.argv[1] == "--rebuild-index":
        print("Rebuilding knowledge index...", file=sys.stderr)
        index = rebuild_index()
        print(f"Index rebuilt: {index['file_count']} files indexed", file=sys.stderr)
        print(f"Index saved to: {INDEX_FILE}", file=sys.stderr)
        return
    
    # Run MCP server
    async def run():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream, server.create_initialization_options())
    
    asyncio.run(run())


if __name__ == "__main__":
    main()
