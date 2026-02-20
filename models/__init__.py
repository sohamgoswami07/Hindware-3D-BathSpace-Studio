from os.path import exists as ispath, dirname, join as joinpath, abspath, sep as dirsep,isfile
import sys
d = joinpath(dirname(dirname(abspath(__file__))), 'models', 'libraries')
if d not in sys.path:
    sys.path.insert(0, d)
from libraries import json_tricks
from libraries import inflect 
