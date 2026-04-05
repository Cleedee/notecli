"""Procedural dungeon name generation from tables."""

import random


def generate_dungeon_name(dungeon_type):
    """Generate a thematic dungeon name from name tables.

    Pattern: article + substantive + preposition + modifier
    Example: "O Palácio da Dor Nebulosa"

    Returns:
        A composed dungeon name string.
    """
    # Import here to avoid circular dependency at module load time
    from notecli.tables import second_part, third_part

    article = dungeon_type.article
    substantive = dungeon_type.name
    adjectival_phrase = random.choice(second_part)
    adjective = random.choice(third_part)

    return f"{article} {substantive} {adjectival_phrase} {adjective}"
