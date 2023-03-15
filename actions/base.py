import argparse
import configparser
import os
from py_brocade.core.formatter import FormatterFactory

from py_brocade.core import BrocadeCmd


class BaseCommand(object):
    help = "Please shoot the messanger"

    def __init__(self):
        self.config = None

    def execute(self, prog, command, args):
        parser = argparse.ArgumentParser(
            description=self.help,
            prog="%s %s" % (prog, command))
        self.add_arguments(parser)

        args = parser.parse_args(args)
        self.handle(args)

    def add_arguments(self, parser):
        pass

    def handle(self, args):
        raise NotImplementedError()

    def get_config(self):
        if self.config is None:
            config_file = os.path.join(os.getenv('HOME'), '.py_brocade', 'py_brocade.conf')

            config = configparser.ConfigParser()
            config.read(config_file)
            self.config = config
        return self.config

    def get_brocade(self, switch):
        config = self.get_config()

        logfile = os.path.join(os.getenv('HOME'), '.py_brocade', 'py_brocade.log')
        if switch is None:
            switch = config.get('main', 'default_switch')
        user = config.get(switch, 'user')
        password = config.get(switch, 'password')
        ip = config.get(switch, 'ip')

        d = BrocadeCmd()
        d.open(switch, ip, user, password, logfile)
        return d


class BrocadeCommand(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--switch', dest="switch",
            help='FC Switch to connect to')
        parser.add_argument(
            '--format', dest="format",
            choices=["readable", "csv", "html"], default="readable",
            help='format to use when displaying results')

    def handle(self, args):
        f = FormatterFactory()
        f.get_formatter(args.format)
        d = self.get_brocade(args.switch)

        self.handle_brocade(args, f, d)
