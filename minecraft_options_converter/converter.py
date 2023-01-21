def convert(ifile, ofile, modifier_sides, target='1.16', forge_modifiers=False,
            jek_ifile=None, jek_ofile=None,
            amecs_ifile=None, amecs_ofile=None,
            ):
    from .dictionary import forward, backward, modifiers
    if target < '1.16':
        forward, backward = backward, forward
    del backward
    modifiers = {**modifiers}
    for mod in ('ALT', 'CONTROL', 'SHIFT'):
        modifiers[mod] = 'R' + mod if modifier_sides[mod.lower()] == 'right' \
                                   else 'L' + mod

    key_modifiers = dict(
            read_modifiers(
                modifiers=modifiers,
                jek_ifile=jek_ifile,
                jek_ofile=jek_ofile,
                amecs_ifile=amecs_ifile,
                amecs_ofile=amecs_ofile,
            )
        )

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

    if jek_ofile is not None or amecs_ofile is not None:
        write_modifiers(
                key_modifiers_items=key_modifiers.items(),
                modifiers=modifiers,
                forward=forward,
                jek_ofile=jek_ofile,
                amecs_ofile=amecs_ofile,
            )


def read_modifiers(modifiers={},
                   jek_ifile=None, jek_ofile=None,
                   amecs_ifile=None, amecs_ofile=None,
                   ):
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
                    yield (key[len('modifiers.'):], mods)
                elif jek_ofile is not None:
                    print(line, file=jek_ofile)
            except EOFError:
                break

    if amecs_ifile is not None:
        while True:  # for each line
            try:
                line = amecs_ifile.readline()
                if not line:
                    break
                line = line.strip()
                line_skip = True
                try:
                    key, value = line.split(':', 1)
                    line_skip = False
                except ValueError:  # Not a key-value pair
                    pass
                if not line_skip and key.startswith('key_modifiers_'):
                    try:
                        has_alt, has_control, has_shift = map(int,
                                                              value.split(','))
                        mods = []
                        if has_alt:
                            mods.append('ALT')
                        if has_control:
                            mods.append('CONTROL')
                        if has_shift:
                            mods.append('SHIFT')
                        mods = tuple(modifiers.get(i, i) for i in mods)
                        yield (key[len('key_modifiers_'):], mods)
                    except ValueError:  # Invalid number of modifiers
                        print(line, file=amecs_ofile)
                elif amecs_ofile is not None:
                    print(line, file=amecs_ofile)
            except EOFError:
                break


def write_modifiers(key_modifiers_items, modifiers, forward={},
                    jek_ofile=None, amecs_ofile=None):
    for name, mods in key_modifiers_items:
        if jek_ofile is not None:
            mods_keys = set(forward.get(i, i) for i in mods)
            print(f'modifiers.{name}:{",".join(mods_keys)}', file=jek_ofile)
        if amecs_ofile is not None:
            mods_types = set(modifiers.get(i, i)[1:] for i in mods)
            print(f'key_modifiers_{name}:' +
                  ",".join(map(str, map(int, [
                      'ALT' in mods_types,
                      'CONTROL' in mods_types,
                      'SHIFT' in mods_types,
                  ]))), file=amecs_ofile)
