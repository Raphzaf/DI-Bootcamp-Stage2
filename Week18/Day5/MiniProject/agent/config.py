"""Environment-based configuration (LLM backend, MCP server commands, orchestration limits)."""
import os
import shlex
import sys
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")


def _env(name, default=""):
    return os.environ.get(name, default)


# Tools exposed to the LLM per server (small models plan better with a focused tool list).
# Override with e.g. ARXIV_TOOLS="search_papers,get_abstract".
DEFAULT_ALLOWLIST = {
    "arxiv": "search_papers,get_abstract,export_citations",
    "filesystem": "write_file,read_text_file,list_directory",
    "fetch": "fetch",
    "research": "clean_citations,assemble_brief",
}


@dataclass
class ServerSpec:
    name: str
    command: list[str]
    third_party: bool
    allow: list[str] = field(default_factory=list)


@dataclass
class Settings:
    backend: str
    base_url: str
    model: str
    api_key: str
    workspace: Path
    servers: list[ServerSpec]
    max_steps: int
    tool_timeout_s: float
    tool_retries: int
    log_dir: Path

    def public_summary(self) -> dict:
        """Config safe to display/log (no secrets)."""
        return {"backend": self.backend, "model": self.model, "base_url": self.base_url,
                "api_key": "set" if self.api_key else "not set", "workspace": str(self.workspace),
                "servers": {s.name: " ".join(s.command) for s in self.servers},
                "max_steps": self.max_steps, "tool_timeout_s": self.tool_timeout_s, "tool_retries": self.tool_retries}


def _resolve(cmd: str) -> list[str]:
    # make relative paths in server commands relative to the project root
    parts = shlex.split(cmd)
    return [str((ROOT / p).resolve()) if p.startswith("./") else p for p in parts]


def load_settings() -> Settings:
    backend = _env("LLM_BACKEND", "ollama").lower()
    if backend == "groq":
        base_url, model, key = _env("GROQ_BASE_URL", "https://api.groq.com/openai/v1"), _env("GROQ_MODEL", "llama-3.3-70b-versatile"), _env("GROQ_API_KEY")
        if not key:
            raise RuntimeError("LLM_BACKEND=groq but GROQ_API_KEY is not set (see .env.example).")
    elif backend == "ollama":
        base_url, model, key = _env("OLLAMA_BASE_URL", "http://localhost:11434/v1"), _env("OLLAMA_MODEL", "qwen2.5:3b"), "ollama"
    else:
        raise RuntimeError(f"Unknown LLM_BACKEND={backend!r}: use 'groq' or 'ollama'.")

    workspace = (ROOT / _env("WORKSPACE_DIR", "./workspace")).resolve()
    (workspace / "papers").mkdir(parents=True, exist_ok=True)

    def allow(name):
        return [t.strip() for t in _env(f"{name.upper()}_TOOLS", DEFAULT_ALLOWLIST[name]).split(",") if t.strip()]

    servers = [
        ServerSpec("arxiv", _resolve(_env("ARXIV_SERVER_CMD", "uvx arxiv-mcp-server --storage-path ./workspace/papers")), True, allow("arxiv")),
        ServerSpec("filesystem", _resolve(_env("FILESYSTEM_SERVER_CMD", "npx -y @modelcontextprotocol/server-filesystem ./workspace")), True, allow("filesystem")),
        ServerSpec("research", [sys.executable, str(ROOT / "research_tools_server.py")], False, allow("research")),
    ]
    if _env("ENABLE_FETCH", "1") == "1":
        servers.insert(2, ServerSpec("fetch", _resolve(_env("FETCH_SERVER_CMD", "uvx mcp-server-fetch")), True, allow("fetch")))

    return Settings(backend, base_url, model, key, workspace, servers,
                    int(_env("MAX_STEPS", "12")), float(_env("TOOL_TIMEOUT_S", "90")), int(_env("TOOL_RETRIES", "2")),
                    (ROOT / _env("LOG_DIR", "./logs")).resolve())
