import random
import sys
from queue import PriorityQueue
from typing import List
import json

from src import GraphInterface
from DiGraph import DiGraph
import matplotlib.pyplot as plt


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
                posi=n['pos'].split(",")
                self.graph.add_node(n["id"], (float(posi[0]), float(posi[1])))
            else:
                self.graph.add_node(n["id"])
        for i in dict["Edges"]:
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
        d = 0

        def full(ls_p, id) -> bool:
            dic = self.graph.all_out_edges_of_node(id)
            for i in dic.items():
                if (id, i[1]) not in ls_p:
                    return True
            return False

        def get_all(ls_p,node_lst)-> bool:
            for i in node_lst:
                if i not in ls_p:
                    return True
            return False

        def move(i, dis, db, ls_p, ls_b, l, ) -> (List[int], float):
            global d
            d = 0
            if get_all(ls_p,node_lst) and self.graph.e_size() > len(ls_b):
                w = sys.maxsize
                k = 0
                if len(ls_p) == 0:
                    d = sys.maxsize
                    return ls_p, d
                check = False
                dic = self.graph.all_out_edges_of_node(i)
                for j in dic.items():
                    if w > j[1] and (i, j[0]) not in ls_b and full(ls_p, j[0]):
                        w = j[1]
                        db = j[1]
                        k = j[0]
                        check = True
                if check:
                    ls_p.append(k)
                    ls_b.append((i, k))
                    dis += db
                    move(k, dis, db, ls_p, ls_b,l)
                else:
                    b = ls_p.pop()
                    dis -= db
                    move(b, dis, db, ls_p, ls_b,l)
            if d < dis:
                d = dis
            return ls_p, d

        for i in node_lst:
            dis = 0
            db = 0
            l = 1
            ls_b = []
            ls_p = [i]
            ls = move(i, dis, db, ls_p, ls_b,l)
            a, b = ls
            if total_w > b:
                total_w = b
                ls_r = a
        if total_w == sys.maxsize:
            return(ls_p, float("inf"))
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
        plt.close()
        max_x = 0
        min_x = float('inf')
        max_y = 0
        min_y = float('inf')
        for n in self.graph.nodes.values():
            if n.pos:
                if n.pos[0] > max_x:
                    max_x = n.pos[0]
                if n.pos[0] < min_x:
                    min_x = n.pos[0]
                if n.pos[1] > max_y:
                    max_y = n.pos[1]
                if n.pos[1] < min_y:
                    min_y = n.pos[1]
        print(min_x)
        print(min_y)

        if min_x == float('inf'):
            max_x = 1
            min_x = 0
        if min_y==float('inf'):
            max_y = 1
            min_y = 0
        if min_x==max_x:
            max_x=max_x+0.5
        if min_y==max_y:
            max_y=max_y+0.5
        x = []
        y = []
        for n in self.graph.nodes.values():
            if not n.pos:
                n.pos = random.uniform(min_x, max_x), random.uniform(min_y, max_y)
            x.append(n.pos[0])
            y.append((n.pos[1]))
        # plt.plot(x,y,".")
        # plt.show()
        for v in self.graph.nodes.values():
            x, y = v.pos[0], v.pos[1]
            plt.plot(x, y, markersize=4, marker='o', color='blue')
            plt.text(x, y, str(v.id), color="red", fontsize=12)
            for i in self.graph.all_out_edges_of_node(v.id).items():
                nai = i[0]
                w = i[1]
                u = self.graph.nodes[nai]
                x_, y_ = u.pos[0], u.pos[1]
                plt.annotate("", xy=(x, y), xytext=(x_, y_), arrowprops=dict(arrowstyle="<-"))

        plt.show()

