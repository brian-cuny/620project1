from neo4j.v1 import GraphDatabase
import csv
from itertools import islice

'''
This program will import open flights text files, clean them and then add them to a neo4j database for 
further querying.
'''


class OpenFlights(object):

    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def query(self, query):
        with self._driver.session() as session:
            return session.run(query)


if __name__ == '__main__':
    neo = OpenFlights('bolt://localhost:7687', 'neo4j', 'password')

    neo.query('MATCH (n) DETACH DELETE n')
    neo.query('CREATE CONSTRAINT ON (r:Airport) ASSERT r.id IS UNIQUE')

    airport_id = []
    with open('openflights_airports.txt', newline='') as csvfile:
        next(islice(csvfile, 1, 1), None)
        for r in csv.reader(csvfile, delimiter=' '):
            if r[3] in ['Canada', 'United Kingdom']:
                r[1] = r[1].replace("'", "")
                airport_id.append(r[0])
                neo.query(f"MERGE (a1:Airport {{id: {r[0]}, name: '{r[1]}', country: '{r[3]}' }}) ")

    with open('openflights.txt', newline='') as csvfile:
        for r in csv.reader(csvfile, delimiter=' '):
            if r[0] in airport_id and r[1] in airport_id:
                neo.query(f"MATCH (a1: Airport {{id: {r[0]}}}) "
                          f"MATCH (a2: Airport {{id: {r[1]}}}) "
                          f"CREATE (a1)-[c:CONNECTS]->(a2) "
                          f"SET c.routes = {r[2]}")

    #508 airports with 1924 connections most resiprocal but not all

    results = neo.query('MATCH (a1:Airport) '
                        'RETURN a1.id, a1.name, a1.country')

    with open('airports_sub.csv', 'w') as write_file:
        writer = csv.writer(write_file)
        writer.writerows(results)

    results2 = neo.query('MATCH (a1:Airport)-[c:CONNECTS]->(a2:Airport) '
                         'RETURN a1.id, a2.id, c.routes')

    with open('connections_sub.csv', 'w') as write_file:
        writer = csv.writer(write_file)
        writer.writerows(results2)