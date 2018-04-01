from __future__ import print_function

import rosie, sys

e = rosie.engine()
e.import_pkg(b'Unicode/Category')
e.load(b'M = Category.Mc / Category.Me / Category.Mn')
mark, _ = e.compile(b'M')
not_mark, _ = e.compile(b'!M')

n = 0
for codepoint in range(0, 0xFFFF + 1):
    char = unichr(codepoint).encode('utf-8')
    is_mark, _, _, _, _ = e.match(mark, char, 1, b'bool')
    is_not_mark, _, _, _, _ = e.match(not_mark, char, 1, b'bool')
    if not (is_mark or is_not_mark):
        print("error at codepoint", codepoint)
    else:
        n = n + 1
print('\n{} characters found'.format(n))

