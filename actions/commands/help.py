import os
import pkgutil
from abc import ABC

from .. import commands as namespace
from .. import load_command
from ..base import BaseCommand


class Command(BaseCommand, ABC):
    help = "List all supported commands."

    def handle(self, args):
        path = os.path.dirname(namespace.__file__)
        for _, name, _ in pkgutil.iter_modules([path]):
            klass = load_command(name)
            print("%24s %s" % (name, klass.help))
