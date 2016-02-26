import importlib
import inspect
import sys
import threading

REQUIRED_FUNCTIONS = ['parameters_test', 'init']

class Module:
    """
    The class containing the characteristics of a module,
    i.e. its name and module.
    """

    def __init__(self, section_name, module_name, parser, queue):
        self.exists = False
        self.section_name = section_name
        self.parser = parser
        self.queue = queue
        sys.stdout.write(str(section_name)+ '...')
        try:
            self.modulefd = importlib.import_module(module_name)
        except ImportError:
            print(" FAILED - Import did not succeeded")
            return
        except SyntaxError:
            print(" FAILED - Syntax Error")
            return

        if self.module_selftesting() is False:
            print(" FAILED - Functions/arguments are missing")
            return

        print(" Added!")
        self.exists = True


    def module_selftesting(self):
        """
        Tests that the functions required exists
        Return true if that's the case
        """
        passed = True
        for function in REQUIRED_FUNCTIONS:
            if function not in dir(self.modulefd):
                    passed = False
                    break

        if passed is not True:
            return False


        return self.modulefd.parameters_test(self.section_name, self.parser)

    def module_launch(self):
        """
        Wrapper for the module_launch function
        """

        t = threading.Thread(target=self._module_launch)
        t.start()


    def _module_launch(self):
        """
        Initialize and launch the module
        """
        module = self.modulefd.init(self.section_name, self.parser, self.queue)
        module.launch()

