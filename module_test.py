"""
Test module for AMX HIVE
"""

REQUIRED_PARAMETERS = ['sentencetosay', 'lol']

def parameters_test(name, parser):
    """
    Check if the given parameters matches the module requirments
    """

    for parameter in REQUIRED_PARAMETERS:
        if not parser.has_option(name, parameter):
            return False

    return True


def init():
    """
    Test init function
    """
    print "All is going according to plan"

    return 0

