
import json, time
from pathlib import Path
from rich.console import Console

console = Console()
LOG_PATH = Path("logs/audit.jsonl")
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

def emit(event: dict):
    event = {"ts": time.time(), **event}
    LOG_PATH.write_text(LOG_PATH.read_text() + json.dumps(event) + "\n" if LOG_PATH.exists() else json.dumps(event) + "\n")
    # pretty to console as well
    console.print(f"[bold cyan]AUDIT[/]: {event}")
