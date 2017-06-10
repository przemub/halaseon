from .mierz import main
from .losowo import main as lmain

import sys

if (len(sys.argv) > 1):
    lmain()
else:
    main()

