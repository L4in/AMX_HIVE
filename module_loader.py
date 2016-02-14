import ConfigParser
import sys
from module import Module

VERSION = "0.0.1"

"""
Loader system for AMX HIVE adding an abstraction layer
between the modules and the system
"""

def __main__():
    """
    Main section of AMX HIVE
    """

    print "AMX HIVE version " + VERSION
    nexus = Nexus()

class Nexus:
    """
    AMX HIVE core function handing parsing,
    and message handling alongside testing
    modules for correct functioning
    """

    def __init__(self):

        # Create the parser and initalize it
        self.parser = ConfigParser.RawConfigParser()
        self.parser.read("config.cfg")
        self.StopOnModuleError = \
                         self.parser.getboolean('General', 'StopOnModuleError')

        # Get the numbers of modules to load
        self.module_list = self.parser.sections()
        self.failed_modules = 0
        del self.module_list[0] # Delete the General section
        self.imported_modules  = []

        # Import listed libraries
        print "The following modules will be loaded:"
        for name in self.module_list:
            module = Module(name, self.parser)
            if module.exists is True:
                self.imported_modules.append(module)
            else:
                self.failed_modules += 1

        print ""
        print "-------- Module loading summary --------"
        print str(len(self.imported_modules)) + " modules loaded, " + \
                                    str(self.failed_modules) + " failed to load"







if __name__ == "__main__":
    print "AMX HIVE version " + VERSION
    nexus = Nexus()
