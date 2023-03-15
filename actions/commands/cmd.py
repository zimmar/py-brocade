from abc import ABC

from ..base import BrocadeCommand


class Command(BrocadeCommand, ABC):
    help = "Run CLI command"

    def add_arguments(self, parser):
        print("parser %s" % parser)
        super(Command, self).add_arguments(parser)
        parser.add_argument('cmd', nargs='+', help="cli command")

    def handle_brocade(self, args, f, d):

        f.output_head("Command Cli")

        d.close()
