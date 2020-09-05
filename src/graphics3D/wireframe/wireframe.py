from typing import Tuple, List

import numpy as np
from numpy import ndarray

from graphics3D.coord import Coord
from graphics3D.wireframe.alias import edge, mesh, color, node_pair, nodes_many


class Wireframe:

    def __init__(self, nodes: ndarray, edges: Tuple[edge], meshes: Tuple[mesh]) -> None:
        self.coord = Coord(np.array([[1, 0, 0, 0],
                                     [0, 1, 0, 0],
                                     [0, 0, 1, 0],
                                     [0, 0, 0, 1]]))
        self._nodes = nodes
        self._edges = edges
        self._meshes = meshes

    def get_global_nodes(self) -> ndarray:
        return self.coord.change_to_global_basis(self._nodes)

    def get_global_edges(self) -> List[Tuple[node_pair, color]]:
        global_edges = []
        for indices, colour in self._edges:
            node1, node2 = self._nodes[indices[0]], self._nodes[indices[1]]
            c1 = self.coord.change_to_global_basis(node1)
            c2 = self.coord.change_to_global_basis(node2)
            global_edges.append(((c1, c2), colour))
        return global_edges

    def get_global_meshes(self) -> List[Tuple[nodes_many, color]]:
        global_meshes = []
        for indices, colour in self._meshes:
            mesh_node_list = []
            for index in indices:
                node = self._nodes[index]
                mesh_node_list.append(self.coord.change_to_global_basis(node))
            global_meshes.append((mesh_node_list, colour))
        return global_meshes
