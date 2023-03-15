import sys

import paramiko as paramiko


def _default_message_handler(msg_prefix, msg_number, msg_type, msg_text):
    sys.stderr.write("%s%s%s %s\n" %
                     (msg_prefix, msg_number, msg_type, msg_text))


class BrocadeCmd(object):

    def __init__(self, message_handler=None):
        self.logfile = None
        self.ip = None
        self.password = None
        self.user = None
        self.switch = None

        self.massage_handler = _default_message_handler
        if message_handler is not None:
            self.message_handler = message_handler

    def open(self, switch, ip, user, password, logfile):
        self.switch = switch
        self.user = user
        self.password = password
        self.ip = ip
        self.logfile = logfile

        conn = paramiko.SSHClient()
        conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        conn.connect(switch, username=user, password=password)
        self.conn = conn

    def close(self):
        if self.conn:
            self.conn.close()


    def set_message_handler(self, message_handler):
        self.message_handler = message_handler

    def _message(self, msg_prefix, msg_number, msg_type, msg_text):
        self.message_handler(msg_prefix, msg_number, msg_type, msg_text)

    def run_cmd(self, command):
        if self.conn:
            stdin, stdout, stderr = self.conn.exec_command(command)
            stdin.close()
            return stdout.readlines()
