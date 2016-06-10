from neo4j.v1 import GraphDatabase, basic_auth
from neo4j.v1.exceptions import ProtocolError
from report import Report

class Session():
    """
    Contains the database connection data
    """

    def __init__(self, adress, user, password):
        """
        Creates the session to the database
        """

        #TODO Remove hardcoded password and implement a
        driver = GraphDatabase.driver(adress, \
                                   auth=basic_auth(user, password))

        try:
            self.session = driver.session()
        except ProtocolError:
            print("Cannot connect to neo4j. Aborting.")
            exit()

    def add_report_to_database(self, report):
        """
        Self-explanatory
        """

        string = """
MERGE (a:NNode {{adress:'{}'}})
MERGE (h:NNode {{adress:'{}'}})
CREATE (a)-[:LAUNCHED]->(strike:Attack{{time:{}, module:'{}', port:{},\
message:'{}', level:{} }})-[:ON]->(h)""".format(report.attacker_ip, \
                report.honeypot_ip, report.epoch, report.module_name, \
                report.attacked_port, report.module_message, report.level)

        self.session.run(string)

    def close_session(self):
        """
        Close the communication to the database
        """

        self.session.close()
