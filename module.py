import importlib
import inspect
import sys

REQUIRED_FUNCTIONS = ['parameters_test', 'init']

class Module():
    """
    The class containing the characteristics of a module,
    i.e. its name and module.
    """

    def __init__(self, name, parser):
        self.exists = False
        self.name = name
        sys.stdout.write(str(name)+ '...')
        try:
            self.modulefd = importlib.import_module(name)
        except ImportError:
            print " FAILED - Import did not succeeded"
            return
        except SyntaxError:
            print " FAILED - Syntax Error"
            return

        if self.module_selftesting(name, parser) is False:
            print "FAILED - Functions/arguments are missing"
            return

        print " Added!"
        self.exists = True


    def module_selftesting(self, name, parser):
        """
        Tests that the functions required exists
        Return true
        """
        passed = True
        for function in REQUIRED_FUNCTIONS:
            if function not in dir(self.modulefd):
                    passed = False
                    break

        if passed is not True:
            return False


        return self.modulefd.parameters_test(name, parser)
