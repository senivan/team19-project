"""

This module contains functions to calculate pagerank for oriented graph.

"""
NUMBER_OF_ITERATIONS = 100

class Node:
    def __init__(self, name: str):
        self.name = name
        self.pagerank = 1
        self.children = []
        self.parents = []
    def get_name(self) -> str:
        return self.name
    def get_pagerank(self) -> float:
        return self.pagerank
    def get_children(self) -> list:
        return self.children
    def get_parents(self) -> list:
        return self.parents
    def set_pagerank(self, pagerank: float):
        self.pagerank = pagerank
    def add_child(self, child):
        self.children.append(child)
    def add_parent(self, parent):
        self.parents.append(parent)
    def update_pagerank(self, damp:float, num:int):
        """
            Function to update pagerank for node.
            Algorithm complexity: O(n) - where n number of neighbours.
        """
        neighbours = self.get_parents()
        pager_sum = sum(node.pagerank/len(node.get_children()) for node in neighbours)
        rand_walk = damp / num
        self.set_pagerank(rand_walk + ((1-damp) * pager_sum))


class Graph:
    def __init__(self, file_name: str):
        self.graph = []
        self.read_graph(file_name)
    def get_children(self, node: str) -> list:
        return node.get_children()
    def get_parents(self, node: str) -> list:
        return node.get_parents()
    
    def create_unique_node(self, name: str) -> Node:
        """
            Function to create unique node.
            returns node.
            Algorithm complexity: O(n^2) - where n number of nodes in graph.
        """
        flag = False
        for node in self.graph:
            if node.get_name() == name:
                flag = True
                break
        if not flag:
            new_node = Node(name)
            self.graph.append(new_node)
            return new_node
        else:
            for node in self.graph:
                if node.get_name() == name:
                    return node
    
    def add_edge(self, node1: str, node2: str):
        """
            Function to add edge between two nodes.
            returns None.
            Algorithm complexity: O(n^2 + n^2 + 2(n-1)) - where n number of nodes in graph.
        """
        node1 = self.create_unique_node(node1)
        node2 = self.create_unique_node(node2)
        node1.add_child(node2)
        node2.add_parent(node1)
        

    def read_graph(self, file_name: str) -> dict:
        """
            Function to read oriented graph from file.
            returns dict with nodes as keys and list of neighbours as values.
            File structure:
            node->node
            node->node
            node->node
            ...
            # >>> read_graph("graph.txt")
            # {'1': ['2', '3'], '2': ['3', '4'], '3': ['4'], '4': ['1']}
            Algorithm complexity: O(n) - where n number of lines in file.
        """
        with open(file_name, "r") as file:
            for line in file:
                line = line.strip()
                node1, node2 = line.split("->")
                self.add_edge(node1, node2)
        self.graph.sort(key=lambda node: node.name)
    def normalize_pageranks(self):
        """
            Function to normalize pageranks.
            returns None.
            # >>> graph = Graph("graph.txt")
            # >>> graph.normalize_pageranks()
            # >>> graph.pageranks
            # [0.25, 0.25, 0.25, 0.25]
            Algorithm complexity: O(n^2) - where n number of nodes in graph.
        """
        sum_pageranks = sum(node.pagerank for node in self.graph)
        for node in self.graph:
            node.pagerank /= sum_pageranks
    
    def get_pageranks(self) -> list:
        """
            Function to return pageranks.
            returns list of pageranks.
            # >>> graph = Graph("graph.txt")
            # >>> graph.get_pageranks()
            # [0.25, 0.25, 0.25, 0.25]
            Algorithm complexity: O(n) - where n number of nodes in graph.
        """
        return [float(f"{node.pagerank:.3f}") for node in self.graph]

def pagerank_iter(graph: Graph, damp: float):
    """
        Function to calculate pagerank for each node in graph.
        returns None.
        # >>> graph = Graph("graph.txt")
        # >>> pagerank_iter(graph, 0.15)
        # >>> graph.pageranks
        # [0.25, 0.25, 0.25, 0.25]
        Algorithm complexity: O(n^2) - where n number of nodes in graph.
    """
    for node in graph.graph:
        node.update_pagerank(damp, len(graph.graph))
    graph.normalize_pageranks()

if __name__ == "__main__":
    graph = Graph("graph5.txt")
    for iteration in range(NUMBER_OF_ITERATIONS):
        pagerank_iter(graph, 0.15)
    print('PageRank:')
    print(graph.get_pageranks())

