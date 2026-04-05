"""Procedural dungeon name generation from tables."""

import random


def generate_dungeon_name() -> str:
    """Generate a thematic dungeon name from name tables.

    Pattern: article + substantive + preposition + modifier
    Example: "O Palácio da Dor Nebulosa"

    Returns:
        A composed dungeon name string.
    """
    # Import here to avoid circular dependency at module load time
    from notecli.tables import DUNGEON_NAME_TABLES

    article = random.choice(DUNGEON_NAME_TABLES["articles"])
    substantive = random.choice(DUNGEON_NAME_TABLES["substantives"])
    preposition = random.choice(DUNGEON_NAME_TABLES["prepositions"])
    modifier = random.choice(DUNGEON_NAME_TABLES["modifiers"])

    return f"{article} {substantive} {preposition} {modifier}"
