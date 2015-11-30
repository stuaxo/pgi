"""
find pgi coverage of all gi.repositorys.
you need to have access to both 'gi' and 'pgi' in the current python
environment.

In a virtualenv this works:

$ pip install pgi
$ pip install vext.gi

$ python pgi_coverage.py
"""

TYPELIB_DIR="/usr/lib/girepository-1.0"

from os.path import basename
from glob import glob
from textwrap import dedent

def test_pgi_coverage(gi_module, pgi_module):
    name_width = len(max(dir(gi_module), key=len))
    #print('%s %s' % (gi_module.__name__.rjust(name_width), pgi_module.__name__))
    #print("%s\t%s" % ("field".rjust(name_width), "error"))
    missing_count = 0
    for name in dir(gi_module):
        if name.startswith('_'):
            continue
        status = ''
        try:
            getattr(pgi_module, name)
            continue
        except NotImplementedError as e:
            #status = "FAIL: '%s'" % str(e.__class__.__name__)
            for line in str(e).splitlines():
                if line.startswith('NotImplementedError:'):
                    status =  status + line
        if not status:
            continue
        if missing_count == 0:
            print("%s\t%s" % ("Field:".rjust(name_width), "Not Implemented(s):"))
        missing_count += 1
        print("%s\t%s" % (name.rjust(name_width), status))

    if missing_count == 0:
        print("[OK] All methods available.")
    print("")

def test_coverage(typelib):
    code = dedent("""
    from pgi.repository import {0} as PGI_{0}
    from gi.repository import {0} as GI_{0}

    test_pgi_coverage(GI_{0}, PGI_{0})
    """.format(typelib))

    try:
        print("PGI coverage of %s" % typelib)
        exec(code)
    except Exception as e:
        print("Skipped because of %s during test" % str(e))

def get_typelibs():
    typelibs = []

    for typelib in glob(TYPELIB_DIR + "/*.typelib"):
        fn = basename(typelib).partition("-")[0]
        typelibs.append(fn)
    return sorted(typelibs)

if __name__=='__main__':
    import gi.repository   # surface this error early
    import pgi.repository  # surface this error early
    typelibs = get_typelibs()
    for typelib in typelibs:
        test_coverage(typelib)
