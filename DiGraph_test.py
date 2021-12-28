import unittest
import DiGraph
from DiGraph import DiGraph



def createGraph():
    graph = DiGraph()
    for i in range(10):
        graph.add_node(i)
    for j in range(1,4):
        for i in range(4,7):
            graph.add_edge(j,i,j*i)

    return graph


class DiGraph_test(unittest.TestCase):


    def test_v_size(self):
        graph = createGraph()
        self.assertEqual(10,graph.v_size())

    def test_e_size(self):
        graph = createGraph()
        self.assertEqual(9,graph.e_size())

    def test_getnode(self):
        graph = createGraph()
        size = graph.get_all_v().keys()
        self.assertEqual(10,len(size))

    def test_all_out_edges_of_node(self):
        graph = createGraph()
        size = graph.all_out_edges_of_node(1)
        self.assertEqual(3,len(size))

    def test_all_in_edges_of_node(self):
        graph = createGraph()
        edge = graph.all_in_edges_of_node(6)
        self.assertEqual(3,len(edge))


    def test_act(self):
        graph = createGraph()
        graph.add_edge(4,6,7)
        graph.add_node(10)
        graph.remove_node(2)
        graph.remove_edge(6,4)
        self.assertEqual(graph.mc,22)

if __name__ == '__main__':
    unittest.main()
