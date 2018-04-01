from __future__ import print_function

import rosie, sys

e = rosie.engine()
e.import_pkg(b'Unicode/Script')
greek, errs = e.compile(b'Script.Greek')
if not greek:
    print(errs)
else:
    n = 0
    for codepoint in range(0, 0xFFFF + 1):
        char = unichr(codepoint).encode('utf-8')
        m, _, _, _, _ = e.match(greek, char, 1, b'bool')
        if m:
            sys.stdout.write(char + ' ')
            n = n + 1
    print('\n{} characters found'.format(n))
    
