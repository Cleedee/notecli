def uses_light(pc):
    pc.light_on = True

def uses_heal(pc):
    pc.health_points += 5

def factory_magic(name) -> dict:
    if name == 'Light':
        return {'name': 'Light', 'applier': uses_light}
    if name == 'Heal':
        return {'name': 'Heal', 'applier': uses_heal}
    return {}

BASIC_MAGICS : dict = {
    1: factory_magic('Heal'),
    2: factory_magic('Light'),
    3: factory_magic('Light'),
    4: factory_magic('Light'),
    5: factory_magic('Light'),
    6: factory_magic('Light')
}
