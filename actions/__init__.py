import importlib
import sys

from .base import BrocadeCommand


def load_command(name):
    assert not name.startswith("_")
    assert name.find(".") == -1
    mod = importlib.import_module('py_brocade.actions.commands.' + name)
    return mod.Command


def command_line(argv=None):
    # argv:= kommando + 0 { optionale argumente } n

    if argv is None:  # Argument wurde nicht hinzugefügt.
        argv = sys.argv  # Argument kommt von der Kommandozeile

    print("Argumente: %s" % argv)
    try:
        command = argv[1]  #
    except IndexError:
        command = "help"  # Keine Argumente dann hilfe Anzeigen

    args = argv[2:]  # Weitere Argumente
    print("args %s" %args)
    try:
        klass = load_command(command)
    except ImportError:
        print("Unknown command %s ." % command, file=sys.stderr)
        return 255
    obj = klass()
    rc = obj.execute(argv[0], command, args)
    return rc
