#!/usr/bin/python3.4

from neo4j_comm import Session
import configparser
import sys

if __name__ == "__main__":

    sys.stdout.write("Reading configuration...")
    parser = configparser.RawConfigParser()
    parser.read("server_config.cfg")
    try:
        neo4j_adress = parser.get('General', 'Neo4jAdress')
        neo4j_username = parser.get('General', 'Neo4jUsername')
        neo4j_password_file = parser.get('General', 'Neo4jPasswordfile')
        neo4j_password = ''
    except configparser.NoSectionError:
        print("Section [General] missing.")
    except configparser.NoOptionError as err:
        print(err)
        exit()

    print(" OK.")

    with open(neo4j_password_file, 'r') as passwd_file:
        neo4j_password = passwd_file.read().strip('\n')


    sys.stdout.write("Connecting to neo4j server...")
    neo4j_handler = Session(neo4j_adress, neo4j_username, neo4j_password)
    print(" OK.")
    string = """
MATCH (a:NNode)-[LAUNCHED]->(n:Attack)-[ON]->(h:NNode)
RETURN count(DISTINCT a) as attackers, count(n) as attacks, count(DISTINCT h) \
AS honeypots"""

    result = neo4j_handler.session.run(string)
    for record in result:
        print("In total, there was {} attacks from {} sources, on {} \
honeypots.".format(record["attacks"], \
                           record["attackers"], \
                           record["honeypots"]))

    neo4j_handler.close_session()
