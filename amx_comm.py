"""
AMX Communication module
Handles the internal messaging system
"""

import time
import queue
import ssl
import socket

class Message():
    """
    Contains the message data and stands ready to be sent
    """
    def __init__(self, bundle):

        self.bundle = bundle

    def send(self, queue):
        """
        Send the message through the queue
        """

        queue.put(self.bundle)


def create_message(attacker_ip, attacked_port, module_name, level, module_message):
    """
    Gets the time then packs the message contents into a message
    """

    epoch = int(time.time())
    bundle = (epoch, attacker_ip, attacked_port, module_name, level, module_message)
    return Message(bundle)

def get_message(nexus):
    """
    Display messages coming from the modules
    """
    try:
        epoch, attacker_ip, attacked_port, module_name, level, message = \
                                                     nexus.queue.get(timeout=2)
        print(attacker_ip)
        print("[" + module_name + "] - Level " + str(level) + " from " + \
                  attacker_ip + " on port " + str(attacked_port)  + \
                  " at " + str(epoch) + " : " + message)
    except queue.Empty:
        return
    #Create SSL context
    context = ssl.create_default_context()
    # Todo: add cert file on the config file rather than hardcoded
    context.load_verify_locations("/home/lain/amx_hive.pem")
    # For the moment
    context.check_hostname = False
    connection = context.wrap_socket( \
                    socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    connection.connect((nexus.server_adress, nexus.server_port))
    try:
         connection.send(bytes(str(epoch) + "|" + \
                               attacker_ip + "|" + \
                               str(attacked_port) + "|" + \
                               module_name + "|" + \
                               str(level) + "|" + \
                               message, \
                                    "utf-8"))
    finally:
        connection.close()
