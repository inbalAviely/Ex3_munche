import unittest
import GraphAlgo
from GraphAlgo import GraphAlgo

class DiGraph_test(unittest.TestCase):

    def test_save(self):
        graph1 = GraphAlgo()
        graph1.load_from_json("A1.json")
        graph1.save_to_json("A2.json")
        graph2 = GraphAlgo()
        graph2.load_from_json("A2.json")
        self.assertTrue(graph2.get_graph().v_size() == graph1.get_graph().v_size())


    def test_functions(self):
        graph = GraphAlgo()
        graph.load_from_json("A1.json")
        self.assertTrue(graph.TSP([1,2,3]) != None)
        self.assertTrue(graph.centerPoint() != None)
        self.assertTrue(graph.shortest_path(1, 5) != None)

