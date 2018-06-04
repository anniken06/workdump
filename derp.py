import itertools

variables = ['a', 'b', 'c']
connectives = ['(', ')', ' not ', ' and ', ' or ']
syntax = [
    lambda x: (connectives[0] + connectives[2] +'$1' + connectives[1]).replace('$1', x),
    lambda x, y: (connectives[0] + '$1' + connectives[3] + '$2' + connectives[1]).replace('$1', x).replace('$2', y),
    lambda x, y: (connectives[0] + '$1' + connectives[4] + '$2' + connectives[1]).replace('$1', x).replace('$2', y),
]


def formula_calculation(wffs=variables.copy()):
    new_wffs = wffs.copy()
    for a, b in itertools.combinations(wffs, 2):
        new_stuff = [syntax[0](a), syntax[0](a), syntax[1](a, b)]
        for stuff in new_stuff:
            if stuff not in new_wffs:
                print(stuff)
                new_wffs += [stuff]
    return formula_calculation(wffs=new_wffs)

formula_calculation()
