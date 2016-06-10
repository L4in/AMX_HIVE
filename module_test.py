"""
Test module for AMX HIVE
"""

import configparser
import socket
import amx_comm

REQUIRED_PARAMETERS = ['sentencetosay', 'port']
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

    print("All is going according to plan")

    return Module_test(name, queue, parser.get(name, 'sentencetosay'), \
            parser.getint(name, 'port'))

class Module_test:
    """
    Class containing all the methods for the module to operate
    """

    def __init__(self, name, queue, string, number):

        self.name = name
        self.string = string
        self.port = number
        self.queue = queue

        print("Initialized with string " + string + \
                                                    " and number " + str(number))


    def launch(self):
        """
        Main function for the module
        """

        print("Consider thyself launched")

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('0.0.0.0', self.port))
        s.listen(5)
        c, addr = s.accept()
        print(str(addr) + " is connected")
        c.send(b"Correctly launched\n")
        message = amx_comm.create_message(\
                            addr[0], self.port, self.name, 1, "Conn established")
        message.send(self.queue)
        c.close()
        s.close()
