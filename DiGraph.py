class DiGraph:

    def __init__(self, nodes={}):
        self.nodes = nodes
        self.mc=0

    def v_size(self) -> int:
        return len(self.nodes)
        raise NotImplementedError

    def e_size(self) -> int:
        size=0
        for i in self.nodes:
            size += i.GetSize()
        return size
        raise NotImplementedError

    def get_all_v(self) -> dict:
        return self.nodes
    def all_in_edges_of_node(self, id1: int) -> dict:
        edges={}
        for i in self.nodes.values():
            for e in i.edges.values():
                if e.dest==id1:
                    edges[i.id]=e.w
        return edges

    def all_out_edges_of_node(self, id1: int) -> dict:
        edges= {}
        n=self.nodes.get(id1)
        for i in n.edges.values():
            edges[i.dest]=i.w
        return edges

    def get_mc(self) -> int:
        return self.mc
        raise NotImplementedError

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        if id1 in self.nodes.keys() and id2 in self.nodes.keys():
            self.nodes[id1].edges[id2]=Edge(id1,id2,weight)
            self.mc+=1

            return True
        return False
        raise NotImplementedError

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        if node_id not in self.nodes.keys():
            self.nodes[node_id]=Node(node_id,pos)
            self.mc+=1

            return True
        return False
        raise NotImplementedError

    def remove_node(self, node_id: int) -> bool:
        if node_id in self.nodes.keys():
            del self.nodes[node_id]
            edges=self.all_in_edges_of_node(node_id)
            for n in edges.keys():
                self.remove_edge(n,node_id)
                self.mc += 1
            self.mc+=1
            return True
        return False
        raise NotImplementedError

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        if node_id2 in self.nodes[node_id1].edges.keys():
            del self.nodes[node_id1].edges[node_id2]
            self.mc+=1
            return True
        return False
        raise NotImplementedError
class Node:
    def __init__(self,id,pos):
        self.id=id
        self.pos=pos
        self.edges={}

    def __repr__(self) -> str:
        return f"id:{self.id} pos:{self.pos}"

    def getSize(self)->int:
        return len(self.edges)

    def get_edge_dict(self)->dict:
        return self.edges


class Edge:
    def __init__(self,src,dest,w):
        self.src=src
        self.w=w
        self.dest=dest
