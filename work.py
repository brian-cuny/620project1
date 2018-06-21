import csv
import networkx as nx
import matplotlib.pyplot as plt
from scipy import stats
from statistics import mean

class Airport():
    def __init__(self, id, airport, country, centrality, closeness, eigenvector, betweenness, international):
        self.id = id
        self.airport = airport
        self.country = country
        self.centrality = float(centrality)
        self.closeness = float(closeness)
        self.eigenvector = float(eigenvector)
        self.betweenness = float(betweenness)
        self.international = international

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f'{self.id} "{self.airport}" {self.country} {self.international} {self.betweenness}'

def extract(comparison, element, attr):
    return [getattr(x, attr) for x in airports if getattr(x, comparison) == element]

if __name__ == '__main__':
    with open('calculations_international.csv') as read_file:
        reader = csv.reader(read_file, delimiter=',')
        next(reader)
        airports = [Airport(*r) for r in reader]

    # Degree Centrality
    print(mean(extract('country', 'Canada', 'centrality')))
    print(mean(extract('country', 'United Kingdom', 'centrality')))

    print(stats.ttest_ind(extract('country', 'Canada', 'centrality'), extract('country', 'United Kingdom', 'centrality')))

    # # United Kingdom has a statistically significant higher centrality than Canada. Due to it's compact nature
    # # the UK has fewer airports with more bottlenecks to get out of the country while Canada has numerous.

    # Degree Centrality
    print(mean(extract('international', 'True', 'centrality')))
    print(mean(extract('international', 'False', 'centrality')))

    print(stats.ttest_ind(extract('international', 'True', 'centrality'),
                          extract('international', 'False', 'centrality')))

    # International airports have much higher centrality

    print(sorted([a for a in airports], key=lambda a: a.centrality, reverse=True))

    # Betweenness centraltiy
    print(mean(extract('international', 'True', 'betweenness')))
    print(mean(extract('international', 'False', 'betweenness')))

    print(stats.ttest_ind(extract('international', 'True', 'betweenness'),
                          extract('international', 'False', 'betweenness')))


    # International airports have much higher betweenness centrality. This indicates that they serve as bottlenecks
    #in the system.

    print(sorted([a for a in airports], key=lambda a : a.betweenness, reverse=True))

#     Closeness Centrality
    print(mean(extract('country', 'Canada', 'closeness')))
    print(mean(extract('country', 'United Kingdom', 'closeness')))

    print(stats.ttest_ind(extract('country', 'Canada', 'closeness'), extract('country', 'United Kingdom', 'closeness')))

#     The UK is more densly packed together than Canada and combine that with Edinburgh taking in 40% of all airports
# this leads to a smaller closeness











