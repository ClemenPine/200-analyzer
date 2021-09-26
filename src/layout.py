import json
import random
import glob
from typing import Dict

JSON = Dict[str, any]


def load_file(filename: str):
    
    fingers = ['LP', 'LR', 'LM', 'LI', 'RI', 'RM', 'RR', 'RP']

    shifted = dict(zip(
        "abcdefghijklmnopqrstuvwxyz,./;'-=[]",
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ<>?:\"_+{}"
    ))

    keys = json.load(open('src/static/TEMPLATE.json', 'r'))

    with open(filename, 'r') as f:
        tokens = []
        for i, line in enumerate(f.readlines()):
            if i == 0:
                keys['name'] = ' '.join(line.split())
            else:
                tokens.append(line.split())

    chars = tokens[:len(tokens) // 2]
    indexes = tokens[len(tokens) // 2:]

    rows = []

    for i in range(len(tokens) // 2):
        rows.append(list(zip(chars[i], indexes[i])))

    for i, keymap in enumerate(rows):
        for j, item in enumerate(keymap):
            finger = fingers[int(item[1])]

            primary = ''
            shift = ''

            if len(item[0]) == 2:
                primary = item[0][0]
                shift = item[0][1]
            else:
                primary = item[0]
                if item[0] in shifted:
                    shift = shifted[item[0]]
                else:
                    shift = None

            keys['keys'][primary] = {
                'finger': finger,
                'row': i,
                'col': j,
                'shift': False,
            }

            if shift:
                keys['keys'][shift] = {
                    'finger': finger,
                    'row': i,
                    'col': j,
                    'shift': True,
                }   

    return keys


def load_dir(dirname: str):
    layouts = []
    for filename in glob.glob(dirname + "/*"):
        layouts.append(load_file(filename))

    return layouts


def pretty_print(keys: JSON):
    pass