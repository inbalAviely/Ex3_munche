from queue import PriorityQueue
from typing import List
import json

from src import GraphInterface
from DiGraph import DiGraph


class GraphAlgo:
    def __init__(self):
        self.graph = DiGraph()
    def get_graph(self) -> GraphInterface:
        return self.graph

    def load_from_json(self, file_name: str) -> bool:

        with open(file_name, "r") as f:
            dict = json.load(f)
        for n in dict["Nodes"]:
            if "pos" in n:
                self.graph.add_node(n["id"], (n['pos']['x'], n['pos']['y']))
            else:
                self.graph.add_node(n["id"])
        for i in dict["Edges"]:
            print(i["src"], i["dest"], i["w"])
            self.graph.add_edge(int(i["src"]), int(i["dest"]), i["w"])
        return True
        raise NotImplementedError

    def save_to_json(self, file_name: str) -> bool:
        with open(file_name, 'w') as f:
            json.dump(self, indent=2, fp=f, default=lambda a: a.__dict__)
            return True
        raise NotImplementedError

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        paths=dict()
        dis={}
        v={}
        for i in self.graph.nodes.keys():
            paths[i]=list()
            dis[i]=float('inf')
        dis[id1]=0
        v[id1]=True
        pq = PriorityQueue()
        pq.put(id1)
        while not pq.empty():
            cur_id=pq.get()
            v[cur_id]=True
            path=[]
            for i in paths.get(cur_id):
                path.append(i)
            path.append(cur_id)


            paths[cur_id]=path
            for i in self.graph.all_out_edges_of_node(cur_id).items():
                if i[0] not in v:
                    old_cost=dis[i[0]]
                    new_cost=dis[cur_id]+i[1]
                    if old_cost>new_cost:
                        pq.put(i[0])
                        dis[i[0]]=new_cost
                        paths[i[0]]=paths[cur_id]


        return dis[id2], paths[id2]

    def TSP(self, node_lst: List[int]) -> (List[int], float):
        """
        Finds the shortest path that visits all the nodes in the list
        :param node_lst: A list of nodes id's
        :return: A list of the nodes id's in the path, and the overall distance
        """

    def centerPoint(self) -> (int, float):
        """
        Finds the node that has the shortest distance to it's farthest node.
        :return: The nodes id, min-maximum distance
        """

    def plot_graph(self) -> None:
        """
        Plots the graph.
        If the nodes have a position, the nodes will be placed there.
        Otherwise, they will be placed in a random but elegant manner.
        @return: None
        """
        raise NotImplementedError