import networkit as nk
from networkit import writeGraph, Format
from random import choice, randint
from generate_graph import GraphGenerator
import os
import pdb

def double_exp_generator(n : int, m: int, connect=True):
    if m < n-1 and connect:
        raise ValueError('graph must have at least n-1 edges to be connect')
    if m > n * (n-1)/2:
        raise ValueError('graph can have at most n*(n-1)/2 edges')
    G = nk.graph.Graph(weighted=True)
    G.addNodes(n)
    added_node = []
    number_edges = 0
    for node in G.iterNodes():
        if len(added_node) == 0:
            added_node.append(node)
        else:
            u = choice(added_node)
            G.addEdge(u, node,1)
            added_node.append(node)
            number_edges += 1
    while number_edges < m:
        nodes = [i for i in range(0, n)]
        while len(nodes) > 0 and number_edges < m:
            v = nodes.pop(randint(0, len(nodes)-1))
            v_neighbors = [neighbor for neighbor in G.iterNeighbors(v)]
            possible_nodes = [node for node in G.iterNodes() if node not in v_neighbors and node != v]
            if len(possible_nodes) > 0:
                u = choice(possible_nodes)
                G.addEdge(u, v)
                number_edges += 1
    return G


class StdGraphGenerator(GraphGenerator):
    n: int
    m: int
    doubling_n_factor: int
    doubling_m_factor: int
    max_number_of_graph: int

    def __init__(self, graph_flag, result_folder: str, n: int, m: int, doubling_n_factor: int = 1,
                 doubling_m_factor: int = 1, max_number_of_graph=10):
        super(StdGraphGenerator, self).__init__(result_folder, graph_flag)
        self.n = n
        self.m = m
        self.doubling_n_factor = doubling_n_factor
        self.doubling_m_factor = doubling_m_factor
        self.max_number_of_graph = max_number_of_graph

    def run(self):
        generate = True
        numberOfGraph = 0
        writer = nk.graphio.EdgeListWriter(separator=" ", firstNode=0)

        while generate and numberOfGraph < self.max_number_of_graph:
            try:
                G = double_exp_generator(self.n, self.m)
                if not os.path.exists(self.result_folder):
                    os.makedirs(self.result_folder)
                writer.write(G, f"{self.result_folder}/{self.graph_flag}(n={self.n}, m={self.m}).txt")
                print("genereted: ", f"{self.result_folder}/{self.graph_flag}(n={self.n}, m={self.m}).txt")

                self.n *= self.doubling_n_factor
                self.m *= self.doubling_m_factor
                numberOfGraph += 1
            except:
                generate = False
        print("generation terminated")


if __name__ == '__main__':
    output_folder = "../../graphs/"
    value_to_doubling = "n"
    result_folder = "2exp"+"node" if value_to_doubling == "n" else "2exp"+"edge"
    maxNumberOfGraph = 10
    numberOfNodes = int(input('number of nodes:'))
    numberOfEdges = int(input('number of edges:'))
    doubling_n_factor = 2
    doubling_m_factor = 1
    generator = StdGraphGenerator(output_folder, result_folder, numberOfNodes, numberOfEdges, doubling_n_factor, doubling_m_factor, maxNumberOfGraph)
    generator.run()


