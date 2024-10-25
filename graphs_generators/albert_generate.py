from networkit.generators import BarabasiAlbertGenerator
from networkit import writeGraph, Format
from random import randint
from generate_graph import GraphGenerator
import os
import networkit as nk


class AlbertGraphGenerator(GraphGenerator):
    start_node_number: int
    max_node_number: int
    doubling_n_factor: int

    def __init__(self, graph_flag: str, result_folder: str, start_node_number: int, max_node_number: int, doubling_n_factor: int = 2):
        super(AlbertGraphGenerator, self).__init__(result_folder, graph_flag)
        self.start_node_number = start_node_number
        self.max_node_number = max_node_number
        self.doubling_n_factor = doubling_n_factor

    def run(self):
        generate = True
        numberOfGraph = 0
        writer = nk.graphio.EdgeListWriter(separator=" ", firstNode=0)
        node_number = self.start_node_number
        while node_number < self.max_node_number:
            attachment_nodes = randint(2, 6)
            graph_generator = BarabasiAlbertGenerator(attachment_nodes, node_number)
            G = graph_generator.generate()
            if not os.path.exists(self.result_folder):
                os.makedirs(self.result_folder)
            writer.write(G, f"{self.result_folder}/{self.graph_flag}(n={node_number}, m={G.numberOfEdges()}).txt")
            print("genereted: ", f"{self.result_folder}/{self.graph_flag}(n={node_number}, m={G.numberOfEdges()}).txt")
            node_number *= self.doubling_n_factor
        print("generation terminated")

if __name__ == "__main__":
    output_folder = "graph"
    graph_flag = "Albert"
    start_node_number = 160
    max_node_number = 30000

    generator = AlbertGraphGenerator(graph_flag, output_folder, start_node_number, max_node_number)