from os.path import dirname as dn
import sys

# Required for cogs to find parent modules
def __init__(self):
    sys.path.insert(0, dn(dn(sys.path[0])))