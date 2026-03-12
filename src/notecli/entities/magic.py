def uses_light(pc):
    pc.light_on = True

def factory_magic(name) -> dict:
    if name == 'Light':
        return {'name': 'Light', 'applier': uses_light}
    return {}

