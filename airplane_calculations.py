import csv
import networkx as nx
import matplotlib.pyplot as plt

if __name__ == '__main__':

    with open('airports_sub.csv') as read_file:
        airports = {int(r[0]): r for r in csv.reader(read_file, delimiter=',')}

    with open('connections_sub.csv') as read_file:
        connections = [(int(r[0]), int(r[1])) for r in csv.reader(read_file, delimiter=',')]

    G = nx.Graph()
    G.add_edges_from(connections)

    degree_centrality = nx.degree(G)
    # print(degree_centrality)

    degree_closeness = nx.closeness_centrality(G)
    # print(degree_closeness)

    eigenvector_centrality = nx.eigenvector_centrality(G)
    # print(eigenvector_centrality)

    betweenness_centrality = nx.betweenness_centrality(G)
    # print(betweenness_centrality)

    for ap, deg in degree_centrality:
        airports[ap].append(deg)
        airports[ap].append(degree_closeness[ap])
        airports[ap].append(eigenvector_centrality[ap])
        airports[ap].append(betweenness_centrality[ap])

    with open('calculations.csv', 'w') as write_file:
        writer = csv.writer(write_file)
        writer.writerow(('ID', 'Airport', 'Country', 'Centrality', 'Closeness', 'Eigenvector', 'Betweenness'))
        for a in airports.values():
            writer.writerow(a)

