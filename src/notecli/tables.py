from notecli.entities import ancestry
from notecli.entities.magic import factory_magic

ANCESTRIES = {
    2: ancestry.SLIMEMAN,
    3: ancestry.VAGALOIDE,
    6: ancestry.ELF
}

BASIC_MAGICS = {
    1: factory_magic('Heal'),
    2: factory_magic('Light'),
    3: factory_magic('Light'),
    4: factory_magic('Light'),
    5: factory_magic('Light'),
    6: factory_magic('Light')
}
