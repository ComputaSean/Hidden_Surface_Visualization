import numpy as np

from graphics3D.coord import Coord


class Wireframe:

    def __init__(self, nodes, edges, meshes):
        self.coord = Coord(np.array([[1, 0, 0, 0],
                                     [0, 1, 0, 0],
                                     [0, 0, 1, 0],
                                     [0, 0, 0, 1]]))
        self._nodes = nodes
        self._edges = edges
        self._meshes = meshes

    def get_global_nodes(self):
        return self.coord.change_to_global_basis(self._nodes)

    def get_global_edges(self):
        global_edges = []
        for n1, n2, color in self._edges:
            node1, node2 = self._nodes[n1], self._nodes[n2]
            c1 = self.coord.change_to_global_basis(node1)
            c2 = self.coord.change_to_global_basis(node2)
            global_edges.append((c1, c2, color))
        return global_edges

    def get_global_meshes(self):
        global_meshes = []
        for mesh in self._meshes:
            mesh_node_list = []
            for n in mesh[0]:
                node = self._nodes[n]
                c = self.coord.change_to_global_basis(node)
                mesh_node_list.append(c)
            global_meshes.append((mesh_node_list, mesh[1]))
        return global_meshes
