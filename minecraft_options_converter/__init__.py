def main():
    import argparse
    import sys
    from .converter import convert

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', type=str, choices=('1.12', '1.16'),
                        default='1.16', help='Target Minecraft version')
    parser.add_argument('-i', '--input', type=argparse.FileType('r'),
                        default=sys.stdin, help='Original options.txt')
    parser.add_argument('-o', '--output', type=argparse.FileType('a'),
                        default=sys.stdout, help='New options.txt')
    parser.add_argument('-f', '--forge-modifiers', action='store_true',
                        help='Write modifiers in FML format')
    parser.add_argument('-I', '--jek-input', type=argparse.FileType('r'),
                        default=None, help='Original options.justenoughkeys.txt')
    parser.add_argument('-O', '--jek-output', type=argparse.FileType('a'),
                        default=None, help='New options.justenoughkeys.txt')
    for mod in ('alt', 'control', 'shift'):
        parser.add_argument(f'--{mod}-side', type=str, choices=('left', 'right'),
                            default='left', help=f'Which "{mod}" to use when '
                            'converting from FML to JEK modifier formart')
    args = parser.parse_args()

    convert(args.input, args.output, {
        'alt': args.alt_side,
        'control': args.control_side,
        'shift': args.shift_side,
    }, args.target, args.forge_modifiers, args.jek_input, args.jek_output)

    for f in (args.input, args.output, args.jek_input, args.jek_output):
        if f:
            f.close()
