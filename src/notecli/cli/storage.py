"""Character persistence via local JSON storage."""

import json
from pathlib import Path
from typing import List, Dict, Any

_STORAGE_PATH = Path.home() / ".notecli" / "characters.json"


def _get_storage_path() -> Path:
    """Return the path to the characters file, creating the directory if needed."""
    _STORAGE_PATH.parent.mkdir(parents=True, exist_ok=True)
    return _STORAGE_PATH


def load_characters() -> List[Dict[str, Any]]:
    """Load all character records from storage.

    Returns:
        List of character dictionaries. Empty list if file doesn't exist.

    Raises:
        ValueError: If the storage file contains invalid JSON.
    """
    path = _get_storage_path()
    if not path.exists():
        return []

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Erro ao carregar personagens. O arquivo pode estar corrompido: {e}")

    return data.get("characters", [])


def save_characters(characters: List[Dict[str, Any]]) -> None:
    """Persist character records to storage.

    Args:
        characters: List of character dictionaries to save.
    """
    path = _get_storage_path()
    data = {"version": 1, "characters": characters}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
