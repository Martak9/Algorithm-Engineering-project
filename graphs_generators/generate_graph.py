class GraphGenerator:
    result_folder: str
    graph_flag: str


    def __init__(self, result_folder: str, graph_flag: str):
        if result_folder[-1] == '/':
            result_folder = result_folder[:-1]
        self.result_folder = result_folder
        self.graph_flag = graph_flag

    def run(self):
        raise NotImplementedError("abstract method")