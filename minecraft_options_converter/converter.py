def convert(ifile, ofile, modifier_sides, target='1.16', forge_modifiers=False,
            jek_ifile=None, jek_ofile=None):
    from .dictionary import forward, backward, modifiers
    if target < '1.16':
        forward, backward = backward, forward
    del backward
    modifiers = {**modifiers}
    for mod in ('ALT', 'CONTROL', 'SHIFT'):
        modifiers[mod] = 'R' + mod if modifier_sides[mod.lower()] == 'right' \
                                   else 'L' + mod

    key_modifiers = {}
    if jek_ifile is not None:
        while True:  # for each line
            try:
                line = jek_ifile.readline()
                if not line:
                    break
                line = line.strip()
                line_skip = True
                try:
                    key, value = line.split(':', 1)
                    line_skip = False
                except ValueError:  # Not a key-value pair
                    pass
                if not line_skip and key.startswith('modifiers.'):
                    mods = tuple(modifiers.get(i, i) for i in value.split(','))
                    key_modifiers[key[len('modifiers.'):]] = mods
                elif jek_ofile is not None:
                    print(line, file=jek_ofile)
            except EOFError:
                break

    while True:  # for each line
        try:
            line = ifile.readline()
            if not line:
                break
            line = line.strip()
            line_skip = True
            try:
                key, value = line.split(':', 1)
                line_skip = False
            except ValueError:  # Not a key-value pair
                pass
            if not line_skip and key.startswith('key_'):
                name = key[len('key_'):]
                keycode, *mods = value.split(':')
                keycode = forward.get(keycode, keycode)
                mods = tuple(modifiers.get(i, i) for i in mods) \
                    + key_modifiers.get(name, ())
                key_modifiers[name] = mods
                if not forge_modifiers:
                    mods = ()
                elif mods:
                    mods = (mods[0].lstrip('LR'),)
                line = ':'.join((key, keycode, *mods))
            print(line, file=ofile)
        except EOFError:
            break

    if jek_ofile is not None:
        for name, mods in key_modifiers.items():
            mods = set(forward.get(i, i) for i in mods)
            print(f'modifiers.{name}:{",".join(mods)}', file=jek_ofile)
