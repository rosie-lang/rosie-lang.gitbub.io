# libpath.py
from __future__ import print_function
import rosie, sys
e = rosie.engine()
e.libpath('/usr/local/lib/rosie/rpl:~/rpl')
e.import_pkg('my_rpl')
pat, errs = e.compile('my_rpl.foo')
print(e.match(pat, sys.argv[1], 1, 'color')[0])

