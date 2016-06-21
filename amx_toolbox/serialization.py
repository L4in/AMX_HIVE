"""
Read and write from a temp file meant to store logs if the server is offline
"""

from os.path import exists
from os import remove
from os import rename

def store_report(bundle):
    """
    Stores the report into a logfile
    """

    epoch, attacker_ip, attacked_port, module_name, level, message = bundle
    with open("./.unsent_reports", "a") as f:
        f.write(str(epoch) + "|" + \
                attacker_ip + "|" + \
                str(attacked_port) + "|" + \
                module_name + "|" + \
                str(level) + "|" + \
                message + "\n")

def get_report_line():
    """
    Creates a generator reading lines from the file
    """

    with open("./.unsent_reports", "r") as f:
        for line in f:
            yield line

def remove_reports_file():
    """
    Delete the old .unsent_reports
    """

    remove("./.unsent_reports")

def replace_reports_file():
    """
    Replace the old .unsent_reports by the new .unsent_reports.swp
    """

    remove_reports_file()
    rename("./.unsent_reports.swp", "./unsent_reports")

