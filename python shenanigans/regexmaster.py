import regex  # pip install regex
import sys

""" Run as:
find /c/Users/jguzman2/git/coleman.ui \
| grep -E 'colemanui.ui/src/' \
| grep -E '\.ts$|\.html$' \
| xargs -d '\n' -I{} python regexmaster.py --substr="categorical" --dist=3 --file={}
"""

def parse_args(kw, default=None):
    arg_name = "--{}=".format(kw)
    try:
        return [s[s.index("=") + 1: ] for s in sys.argv if s.startswith(arg_name)][0]
    except Exception as e:
        print("Failed to get argument: {}<VALUE>. Returning default: {}{}".format(*[arg_name] * 2, default))
        return default

substr = parse_args("substr")
dist = parse_args("dist", "2")
file = parse_args("file")
recomp = regex.compile("(?:(?<![a-z0-9])(?P<cap>{SUBSTR}?)(?![a-z0-9])){{e<={EDIT_DIST}}}".format(SUBSTR=substr.lower(), EDIT_DIST=dist))

with open(file, "r") as f:
    #print(">> Regex: {}".format(recomp))
    for (line_number, line) in enumerate(f.readlines(), start=1):
        if recomp.search(line.lower()):
            print("\t{}\n{}:\t{}".format(file, line_number, line), end="")
            import code; code.interact(local={**locals(), **globals()})
