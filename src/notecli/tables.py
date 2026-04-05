from notecli.entities.ancestry import (
    SLIMEMAN,
    VAGALOIDE,
    FAERIE,
    GNOME,
    ELF,
    HUMAN,
    DWARF,
    HALFLING,
    CAT_PEOPLE,
    RINOCEROID,
    HALF_DRAGON
)
from notecli.entities.dungeon import DungeonType

from notecli.entities import occupation

ANCESTRIES = {
    2: SLIMEMAN,
    3: VAGALOIDE,
    4: FAERIE,
    5: GNOME,
    6: ELF,
    7: HUMAN,
    8: DWARF,
    9: HALFLING,
    10: CAT_PEOPLE,
    11: RINOCEROID,
    12: HALF_DRAGON
}

OCCUPATIONS = {
    2: occupation.BEGGAR,
    3: occupation.GRAVEDIGGER,
    4: occupation.NOBLE,
    5: occupation.STUDENT,
    6: occupation.BLACKSMITH,
    7: occupation.GUARD,
    8: occupation.CHEF,
    9: occupation.LOCKSMITH,
    10: occupation.LUMBERJACK,
    11: occupation.LUMBERJACK,
    12: occupation.GLADIATOR
}

DUNGEON_TYPES = {
    1: DungeonType(
        name="Palácio",
        entrance_description=(
            "Portões de ferro retorcido marcam a entrada de uma residência real "
            "há muito abandonada. O vento uiva através de janelas vazias, "
            "carregando o cheiro de pedra úmida e algo podre nas profundezas."
        ),
    ),
    2: DungeonType(
        name="Cripta",
        entrance_description=(
            "Uma escadaria em espiral desce para a escuridão, com paredes cobertas "
            "de nichos vazios. O ar é gelado e um silêncio pesado preenche o "
            "corredor, interrompido apenas pelo gotejar distante de água."
        ),
    ),
    3: DungeonType(
        name="Tumba",
        entrance_description=(
            "Um arco de pedra selado com runas desgastadas pelo tempo bloqueia "
            "parcialmente a entrada. Do interior vem um cheiro doce de incenso "
            "antigo misturado com o odor metálico de armadilhas enferrujadas."
        ),
    ),
    4: DungeonType(
        name="Santuário",
        entrance_description=(
            "Colunas negras sustentam um póreo ornamentado com símbolos de uma fé "
            "esquecida. A entrada parece absorver a luz ao redor, e sussurros "
            "indistinguíveis ecoam das paredes internas."
        ),
    ),
    5: DungeonType(
        name="Templo",
        entrance_description=(
            "Colunas antigas sustentam um telhado parcialmente desabado, revelando "
            "fragmentos de afrescos divinos. O cheiro de incenso antigo mistura-se "
            "com algo metálico no ar — sangue ou ferro, difícil dizer."
        ),
    ),
    6: DungeonType(
        name="Calabouço",
        entrance_description=(
            "Uma grade enferrujada foi arrombada há muito tempo, revelando um "
            "corredor úmido que desce em direção ao subsolo. Gritos abafados ou "
            "ecos de correntes — é impossível saber se vêm do presente ou do passado."
        ),
    ),
}

DUNGEON_NAME_TABLES = {
    "articles": ["O", "A", "As", "Os"],
    "substantives": [
        "Palácio", "Cripta", "Tumba", "Santuário", "Templo", "Calabouço",
        "Catacumba", "Fortaleza", "Masmorra", "Torre",
    ],
    "prepositions": ["de", "da", "do", "das", "dos"],
    "modifiers": [
        "Dor", "Névoa", "Trevas", "Sangue", "Sombras",
        "Ossos", "Cinzas", "Medo", "Silêncio", "Esquecimento",
        "Nebulosa", "Profunda", "Antiga", "Amaldiçoada", "Perdida",
    ],
}
