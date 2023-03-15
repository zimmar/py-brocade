import sys
from . import command_line

if __name__ == "__main__":
    rc = command_line(sys.argv)
    sys.exit(rc)