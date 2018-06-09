from neo4j.v1 import GraphDatabase
import csv
from itertools import islice

'''
This program will import the roadNet-CA.txt file (containing 1965206 nodes and 5533214 edges)
into a Neo4j graph and then query a small subset of that and add it to a network x graph.
All nodes within 3 steps of road id 0 are stored in subgraph.csv for further processing
'''


class RoadNet(object):

    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def query(self, query):
        with self._driver.session() as session:
            return session.run(query)


if __name__ == '__main__':
    neo = RoadNet('bolt://localhost:7687', 'neo4j', 'password')

    neo.query('MATCH (n) DETACH DELETE n')
    neo.query('CREATE CONSTRAINT ON (r:Road) ASSERT r.id IS UNIQUE')

    with open('roadNet-CA.txt', newline='') as csvfile:
        next(islice(csvfile, 4, 4), None)
        for r in csv.reader(csvfile, delimiter='\t'):
            neo.query(f'MERGE (r1:Road {{id: {r[0]}}})'
                      f'MERGE (r2:Road {{id: {r[1]}}})'
                      'CREATE (r1)-[:CONNECTS]->(r2)')

    results = [(r1, r2) for r1, r2 in neo.query('MATCH p=(:Road {id: 0})-[:CONNECTS*1..3]->(:Road) '
                                                'WITH p '
                                                'MATCH (r3:Road)-[:CONNECTS*1..3]->(r4:Road) '
                                                'WHERE r3 IN nodes(p) AND r4 in nodes(p) AND r3 <> r4 '
                                                'RETURN DISTINCT r3.id, r4.id')]

    print(results)

    with open('subgraph.csv', 'w') as write_file:
        writer = csv.writer(write_file)
        writer.writerows(results)