"""
AMX Communication module
Handles the internal messaging system
"""

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
    Packs the message contents into a message
    """

    bundle = (attacker_ip, attacked_port, module_name, level, module_message)
    return Message(bundle)

def get_message(nexus):
    """
    Display messages coming from the modules
    """
    try:
        attacker_ip, attacked_port, module_name, level, message = nexus.queue.get(timeout=2)
        print("[" + module_name + "] - Level " + str(level) + " from " + \
                  attacker_ip + " on port " + attacked_port " : "+ message)
    except queue.Empty:
        return
