#!/usr/bin/python3.4

import asyncio
import ssl
import configparser
from report import Report

class Connection_handler(asyncio.Protocol):
    """
    Encapsulates a connection to the server
    """
    def __init__(self):
        self.client_adress = 0

    def connection_made(self, transport):
        """
        Called once the new connection is made
        """
        print("Opening new connection to client")
        self.transport = transport
        self.client_adress = transport.get_extra_info('peername')

    def data_received(self, data):
        """
        Called when the client send data
        """
        #Notify that the data is received
        print("Message received from {}".format(self.client_adress))

        data_list = data.decode("utf-8").split("|")
        print(data_list)
        report = Report(self.client_adress, data_list)

    def connection_lost(self, exc):
        """
        Called when the connection ends
        """
        print("Connection to {} closed.".format(self.client_adress))

#Create the parser for the configuration file
parser = configparser.RawConfigParser()
parser.read("server_config.cfg")
try:
    port = parser.getint('General', 'ServerPort')
    adress = parser.get('General', 'ServerAdress')
    ssl_certificate = parser.get('General', 'SSLCert')
except configparser.NoSectionError:
    print("Section [General] missing.")
    exit()

#Create SSL context
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile=ssl_certificate)

#Create event loop
loop = asyncio.get_event_loop()

#Create coroutine
socket_coroutine = loop.create_server(Connection_handler, adress, port, \
                                    ssl=context)

#Add the coroutine to the loop
server = loop.run_until_complete(socket_coroutine)



try:
    #Run the loop forever
    loop.run_forever()
except KeyboardInterrupt:
    print("\nExitting via keyboard.")
finally:
    #Stop the server
    server.close()
    #Shut down the loop
    loop.close()
