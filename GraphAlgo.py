import sys
from queue import PriorityQueue
from typing import List
import json

from src import GraphInterface
from DiGraph import DiGraph


class GraphAlgo:
    def __init__(self, g=None):
        if not g:
            self.graph = DiGraph()
        else:
            self.graph = g

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
        paths = dict()
        dis = {}
        v = {}
        for i in self.graph.nodes.keys():
            paths[i] = list()
            dis[i] = float('inf')
        dis[id1] = 0
        v[id1] = True
        pq = PriorityQueue()
        pq.put(id1)
        while not pq.empty():
            cur_id = pq.get()
            v[cur_id] = True
            path = []
            for i in paths.get(cur_id):
                path.append(i)
            path.append(cur_id)

            paths[cur_id] = path
            for i in self.graph.all_out_edges_of_node(cur_id).items():
                if i[0] not in v:
                    old_cost = dis[i[0]]
                    new_cost = dis[cur_id] + i[1]
                    if old_cost > new_cost:
                        pq.put(i[0])
                        dis[i[0]] = new_cost
                        paths[i[0]] = paths[cur_id]

        return dis[id2], paths[id2]

    def TSP(self, node_lst: List[int]) -> (List[int], float):
        total_w = sys.maxsize
        ls_r = []

        def move(i, dis, db, ls_p, ls_b) -> (List[int], float):

            if self.graph.v_size() > len(ls_p) and self.graph.e_size()-2 > len(ls_b):
                w = sys.maxsize
                k = 0
                check = False
                dic = self.graph.all_out_edges_of_node(i)
                for j in dic.items():
                    if w > j[1] and (i, j[0]) not in ls_b:
                        w = j[1]
                        db = j[1]
                        k = j[0]
                        check = True
                print(ls_p)
                if check:
                    ls_p.append(k)
                    ls_b.append((i, k))
                    dis += db
                    move(k, dis, db, ls_p, ls_b)
                else:
                    b = ls_p.pop()
                    dis -= db
                    move(b, dis, db, ls_p, ls_b)
            return ls_p, dis

        for i in self.graph.nodes.keys():
            dis = 0
            db = 0

            ls_b = []
            ls_p = [i]
            ls = move(i, dis, db, ls_p, ls_b)
            a, b = ls
            if total_w > b:
                total_w = b
                ls_r = a
        return ls_r, total_w

    def centerPoint(self) -> (int, float):
        min_p = -1
        min_dis = float('inf')
        for n in self.graph.nodes.values():
            max_p = -1
            max_dis = 0.0
            for p in self.graph.nodes.values():
                if n != p:
                    cur_dis = self.shortest_path(n.id, p.id)
                    if len(cur_dis[1]) != 0 and cur_dis[0] > max_dis:
                        max_p = p.id
                        max_dis = cur_dis[0]
            if max_p != -1 and min_dis > max_dis:
                min_p = n.id
                min_dis = max_dis
        return min_p, min_dis

    def plot_graph(self) -> None:
        """
        Plots the graph.
        If the nodes have a position, the nodes will be placed there.
        Otherwise, they will be placed in a random but elegant manner.
        @return: None
        """
        raise NotImplementedError
