class Report():
    """
    Contains the data needed to log a report into the database
    """
    def __init__(self, honeypot_ip, data_list):

        self.honeypot_ip = honeypot_ip
        self.epoch, self.attacked_port, self.level = self.module_message = \
                                               [int(x) for x in data_list[::2]]
        self.attacker_ip, self.module_name, self.module_message = \
                                                                data_list[1::2]
