"""
Test module for AMX HIVE
"""

import configparser
import socket
import re
from amx_toolbox import amx_comm

REQUIRED_PARAMETERS = ['port']
def parameters_test(name, parser):
    """
    Check if the given parameters matches the module requirments
    """

    for parameter in REQUIRED_PARAMETERS:
        if not parser.has_option(name, parameter):
            return False

    return True

def init(name, parser, queue):
    """
    Test init function
    """

    return Module_test(name, queue, parser.getint(name, 'port'))

class Module_test:
    """
    Class containing all the methods for the module to operate
    """

    def __init__(self, name, queue, number):

        self.name = name
        self.port = number
        self.queue = queue


    def launch(self):
        """
        Main function for the module
        """

        print("[{}] Attempting to open port {}".format(self.name, self.port))

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('0.0.0.0', self.port))
        s.listen(5)
        string = ""
        while True:
                c, addr = s.accept()
                print(str(addr) + " is connected")
                try:
                    string = c.recv(4096).decode()
                except socket.error:
                    message = amx_comm.create_message(\
                          addr[0], self.port, self.name, 1, "Conn established")
                    message.send(self.queue)
                    continue
                matches = re.search('(?<=(GET\s)).*', string)

                if matches != None:
                    getmess = matches.group(0).rstrip()
                    print("GET requested {}".format(getmess))
                    message = amx_comm.create_message(\
                            addr[0], self.port, self.name, 2, \
                            "GET request: {}".format(getmess))
                    message.send(self.queue)

                c.close()

        s.close()
