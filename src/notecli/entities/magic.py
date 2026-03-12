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

