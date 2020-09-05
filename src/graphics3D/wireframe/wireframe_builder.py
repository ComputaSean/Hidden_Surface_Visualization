from typing import List

import numpy as np
from numpy import ndarray

from graphics3D.wireframe.alias import edge, mesh
from graphics3D.wireframe.wireframe import Wireframe


class WireframeBuilder:

    def __init__(self) -> None:
        self._nodes = np.empty([0, 4])
        self._edges: List[edge] = []
        self._meshes: List[mesh] = []

    def add_node(self, nx: int, ny: int, nz: int) -> None:
        self._nodes = np.vstack((self._nodes, np.array([nx, ny, nz, 1])))

    def add_nodes(self, node_arr: ndarray) -> None:
        ones_col = np.ones([len(node_arr), 1])
        ones_added = np.hstack((node_arr, ones_col))
        self._nodes = np.vstack((self._nodes, ones_added))

    def add_edge(self, e: edge) -> None:
        self._edges.append(e)

    def add_edges(self, edges: List[edge]) -> None:
        self._edges.extend(edges)

    def add_mesh(self, m: mesh) -> None:
        self._meshes.append(m)

    def add_meshes(self, meshes: List[mesh]) -> None:
        self._meshes.extend(meshes)

    def build(self) -> Wireframe:
        return Wireframe(self._nodes, tuple(self._edges), tuple(self._meshes))
