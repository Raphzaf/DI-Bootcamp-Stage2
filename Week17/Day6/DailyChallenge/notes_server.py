import json, logging, sys
from datetime import datetime
from pathlib import Path
from mcp.server.fastmcp import FastMCP

logging.basicConfig(level=logging.INFO, stream=sys.stderr, format="[notes] %(message)s")
NOTES_FILE = Path("notes.json")          # persisted: each STDIO session starts a fresh server process
mcp = FastMCP("Notes")


def _load():
    return json.loads(NOTES_FILE.read_text()) if NOTES_FILE.exists() else []


@mcp.tool()
def add_note(text: str, tag: str = "general") -> dict:
    """Save a short note (e.g. a shortlist of places to stay) with an optional tag."""
    notes = _load()
    note = {"id": len(notes) + 1, "tag": tag, "text": text, "created": datetime.now().isoformat(timespec="seconds")}
    notes.append(note)
    NOTES_FILE.write_text(json.dumps(notes, indent=2))
    logging.info("note %s saved (%s)", note["id"], tag)
    return note


@mcp.tool()
def list_notes(tag: str = "") -> list[dict]:
    """List saved notes, optionally filtered by tag."""
    return [n for n in _load() if not tag or n["tag"] == tag]


if __name__ == "__main__":
    mcp.run()
