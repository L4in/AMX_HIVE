"""
AMX Communication module
Handles the internal messaging system
"""

import time
import queue
import ssl
import socket
from os.path import exists
from amx_toolbox import serialization

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
    epoch = int(time.time()*1000)
    bundle = (epoch, attacker_ip, attacked_port, module_name, level, module_message)
    return Message(bundle)


def test_connection_to_server(nexus):
    """
    Tests the connection to the server
    Gives a console-based feedback
    """

    print("[NETWORK] Probing server connection...")
    try:
        connection = open_ssl(nexus)
    except ConnectionRefusedError:
        print("[NETWORK] Can't reach the server - is the adress correct or is the server online?")
        if nexus.stop_on_module_error:
            exit()
        else:
            print("Do you want to continue? [y/N]")
            choice = input().lower().rstrip()
            if choice == 'y':
                pass
            else:
                print("Aborting...")
                exit()
    else:
        print("[NETWORK] Server connected.")
        connection.close()


def open_ssl(nexus):
    """
    Creates and initialize the ssl socket for sending data
    """
    #Create SSL context
    context = ssl.create_default_context()
    # Todo: add cert file on the config file rather than hardcoded
    context.load_verify_locations(nexus.sslcert)
    # For the moment
    context.check_hostname = False
    connection = context.wrap_socket( \
                             socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    connection.connect((nexus.server_adress, nexus.server_port))

    return connection

def send_line_to_server(connection, line):
    """
    Send line to the server
    """
    connection.send(bytes(line,  "utf-8"))


def send_bundle_to_server(connection, bundle):
    """
    Send bundle to the server
    """
    epoch, attacker_ip, attacked_port, module_name, level, message = bundle
    connection.send(bytes(  str(epoch) + "|" + \
                            attacker_ip + "|" + \
                            str(attacked_port) + "|" + \
                            module_name + "|" + \
                            str(level) + "|" + \
                            message.strip("\n"), \
                                "utf-8"))


def get_message(nexus):
    """
    Display messages coming from the modules
    """
    try:
        bundle = nexus.queue.get(timeout=2)
    except queue.Empty:
        #Nothing to do
        return

    try:
        connection = open_ssl(nexus)
    except ConnectionRefusedError:
        print("Connection to server refused - serializing the data")
        serialization.store_report(bundle)
        return

    if exists(".unsent_reports"):
        print("Attenpting to send data backlog")
        # Sending the previous reports first
        reports = serialization.get_report_line()
        #There's still lines in the file
        generation_continues = True
        #There's no network error
        socket_error = False
        while(generation_continues and not socket_error):

            try:
                send_line_to_server(connection, next(reports).strip("\n"))
            except StopIteration:
                generation_continues = False
                print("No more data in file while outputting")
                serialization.remove_reports_file()

            except (socket.error, ssl.SSLError):
                socket_error = True

        if (generation_continues):
            with open("./.usent_reports.swp", "w") as w:
                while(generation_continues):
                    try:
                        w.write(reports.next().strip('\n'))
                    except StopIteration:
                        generation_continues = False
                        print("No more data in file while serializing")

            serialization.replace_report_file()


    epoch, attacker_ip, attacked_port, module_name, level, message = bundle
    print("[" + module_name + "] - Level " + str(level) + " from " + \
                  attacker_ip + " on port " + str(attacked_port)  + \
                  " at " + str(epoch) + " : " + message)

    try:
        send_bundle_to_server(connection, bundle)
    except (socket.error, ssl.SSLError):
        print("An error occured on the transport layer - serializing")
        serialization.store_report(bundle)
    finally:
        connection.close()
