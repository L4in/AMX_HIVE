#!/usr/bin/python3.4

import configparser
import sys
import threading
import queue
import amx_comm
from module import Module

VERSION = "0.0.1"

"""
Loader system for AMX HIVE adding an abstraction layer
between the modules and the system
"""


class Nexus:
    """
    AMX HIVE core function handing parsing,
    and message handling alongside testing
    modules for correct functioning
    """

    def __init__(self):

        # Create the parser and initalize it
        self.parser = configparser.RawConfigParser()
        self.parser.read("config.cfg")
        self.stop_on_module_error = \
                         self.parser.getboolean('General', 'StopOnModuleError')
        self.max_module_number = \
                         self.parser.getint('General', 'MaxModuleNumber')

        print("Max number of modules is " + str(self.max_module_number))

        # Get the numbers of modules to load
        self.section_list = self.parser.sections()
        self.failed_modules = 0
        self.queue = queue.Queue()
        del self.section_list[0] # Delete the General section


        self.module_list = []
        for name in self.section_list:
            self.module_list.append( \
                                (name, self.parser.get(name, "ModuleName")))

        print("Attempting to load " + str(len(self.module_list)) + " modules.")

        self.imported_modules  = []

        # Import listed libraries
        print("The following modules will be loaded:")
        for bundle in self.module_list:
            section_name, module_name = bundle
            module = Module(section_name, module_name, self.parser, self.queue)
            if module.exists is True:
                self.imported_modules.append(module)
            else:
                self.failed_modules += 1

        print("")
        print("-------- Module loading summary --------")
        print(str(len(self.imported_modules)) + " modules loaded, " + \
                                    str(self.failed_modules) + " failed to load")


    def check_module_number(self):
        """
        Check if there is not too much modules loaded
        """

        number_ok = True

        if len(self.imported_modules) > self.max_module_number:
            number_ok = False

        return number_ok


    def module_launch(self):
        """
        Create threads and launch the modules into them
        Waits for queue messages
        """

        for module in self.imported_modules:
            module.module_launch()

    def message_loop(self):
        """
        Loops into message reception
        """

        while threading.active_count() != 1:
            amx_comm.get_message(self)

if __name__ == "__main__":
    print("AMX HIVE version " + VERSION)
    nexus = Nexus()
    if not nexus.check_module_number():
        print("Too much modules loaded!")
    else:
        nexus.module_launch()
        try:
            nexus.message_loop()
        except KeyboardInterrupt:
            print("\nExitting via keyboard.")
            exit()
