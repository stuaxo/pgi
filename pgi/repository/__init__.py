# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

import sys

from pgi.importer import Importer


sys.meta_path.append(Importer())

del sys
del Importer