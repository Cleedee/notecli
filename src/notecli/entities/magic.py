def uses_freeze(pc):
    pass

def uses_light(pc):
    pc.light_on = True

def uses_heal(pc):
    pc.hp_current += 5
    if pc.hp_current > pc.health_points:
        pc.hp_current = pc.health_points

def factory_magic(name) -> dict:
    if name == 'Light':
        return {'name': 'Light', 'applier': uses_light, 'uses': 1}
    if name == 'Heal':
        return {'name': 'Heal', 'applier': uses_heal, 'uses': 1}
    if name == 'Freeze':
        return {'name': 'Freeze', 'applier': uses_freeze, 'uses': 1}
    return {}

BASIC_MAGICS : dict = {
    1: factory_magic('Heal'),
    2: factory_magic('Light'),
    3: factory_magic('Light'),
    4: factory_magic('Freeze'),
    5: factory_magic('Light'),
    6: factory_magic('Light')
}
