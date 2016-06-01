class Report():
    """
    Contains the data needed to log a report into the database
    """
    def __init__(self, honeypot_ip, data_list):

        self.honeypot_ip = honeypot_ip
        self.attacker_ip, self.module_name, self.module_message = \
                                                                data_list[::2]
        self.attacked_port = int(data_list[1])
        self.level = int(data_list[3])
