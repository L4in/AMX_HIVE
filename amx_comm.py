"""
AMX Communication module
Handles the internal messaging system
"""

class Message():
    """
    Contains the message data and stands ready to be sent
    """
    def __init__(self, bundle):

        self.bundle = bundle

    def send(self):
        """
        Send the message through the queue
        """

        self.queue.put(bundle)


def create_message(attacker_adress, attacker_port, module_name, level, module_message):
    """
    Packs the message contents into a message
    """

    bundle = (attacker_adress, attacker_port, module_name, level, module_message)
    return Message(bundle)
