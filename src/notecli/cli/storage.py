"""Character and exploration persistence via local JSON storage."""

import json
from pathlib import Path
from typing import Optional, Dict, Any

_CHARACTERS_PATH = Path.home() / ".notecli" / "characters.json"
_EXPLORATION_PATH = Path.home() / ".notecli" / "exploration.json"

# Backward compatibility alias
_STORAGE_PATH = _CHARACTERS_PATH


def _get_storage_path() -> Path:
    """Return the path to the characters file, creating the directory if needed."""
    _CHARACTERS_PATH.parent.mkdir(parents=True, exist_ok=True)
    return _CHARACTERS_PATH


def _get_exploration_path() -> Path:
    """Return the path to the exploration file, creating the directory if needed."""
    _EXPLORATION_PATH.parent.mkdir(parents=True, exist_ok=True)
    return _EXPLORATION_PATH


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


def load_exploration() -> Optional[Dict[str, Any]]:
    """Load the active exploration session.

    Returns:
        Session dict if one exists and is active, None otherwise.

    Raises:
        ValueError: If the storage file contains invalid JSON.
    """
    path = _get_exploration_path()
    if not path.exists():
        return None

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Erro ao carregar sessão de exploração. O arquivo pode estar corrompido: {e}"
        )

    session = data.get("session")
    if session and session.get("active", False):
        return session
    return None


def save_exploration(session_data: Dict[str, Any]) -> None:
    """Persist the exploration session to storage.

    Args:
        session_data: Session dictionary to save.
    """
    path = _get_exploration_path()
    data = {"version": 1, "session": session_data}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def clear_exploration() -> None:
    """Remove the active exploration session file."""
    path = _get_exploration_path()
    if path.exists():
        path.unlink()
