"""
Test module for AMX HIVE
"""

import configparser
import socket
import re
from amx_toolbox import amx_comm

REQUIRED_PARAMETERS = ['port', 'banner']
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

    return Simple_ftp(name, queue, parser.getint(name, 'port'), \
                                   parser.get(name, 'banner'))

class Simple_ftp:
    """
    Class containing all the methods for the module to operate
    """

    def __init__(self, name, queue, number, banner):

        self.name = name
        self.port = number
        self.queue = queue
        self.banner = banner


    def launch(self):
        """
        Main function for the module
        """

        print("[{}] Attempting to open socket on port {}".format(self.name, self.port))
        print("[{}] Banner is {}".format(self.name, self.banner))

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('0.0.0.0', self.port))
        s.listen(5)
        level = 0
        string = ""
        username = ""
        passwd = ""
        while True:
                level = 0
                username = None
                passwd = None
                c, addr = s.accept()
                print(str(addr) + " is connected")
                level = 1
                c.settimeout(60)
                try:
                    c.send(("220 " + self.banner + "\n").encode())
                except socket.error as e:
                    print(e)
                    continue
                try:
                    string = c.recv(1024).decode()
                except socket.error:
                    message = amx_comm.create_message(\
                            addr[0], self.port, self.name, 1, \
                            "Connection established, no further action")
                    message.send(self.queue)
                    continue
                matches = re.search('(?<=(USER\s)).*(?=$)', string)
                if matches != None:
                    username = matches.group(0).rstrip()
                    print("Username is {}".format(username))
                else:
                    c.close()

                try:
                    c.send("331 Password required to access user account {}\n".format(username).encode())
                    string = c.recv(1024).decode()
                except socket.error:
                    message = amx_comm.create_message(\
                            addr[0], self.port, self.name, 2, \
                            "Identification attempt with username {}".format(username))
                    message.send(self.queue)
                    continue

                matches = re.search('(?<=(PASS\s)).*', string)
                if matches != None:
                    passwd = matches.group(0).rstrip()
                    print("Password is {}".format(passwd))
                else:
                    c.close()

                if passwd != "":
                    message = amx_comm.create_message(\
                        addr[0], self.port, self.name, 3, \
                        "Identification attempt with {} : {}".format(\
                                                            username, passwd))
                    message.send(self.queue)

                else:
                    message = amx_comm.create_message(\
                            addr[0], self.port, self.name, 2, \
                            "Identification attempt with username {}".format(username))
                    message.send(self.queue)

                c.close()

        s.close()
