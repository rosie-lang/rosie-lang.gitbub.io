# matchall.py
from __future__ import print_function
import rosie, sys
e = rosie.engine()
e.import_pkg('all')
pat, errs = e.compile('all.things')
print(e.match(pat, sys.argv[1], 1, 'color')[0])
