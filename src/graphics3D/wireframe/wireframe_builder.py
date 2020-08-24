import numpy as np

from graphics3D.wireframe.wireframe import Wireframe


class WireframeBuilder:

    def __init__(self):
        self._nodes = np.empty([0, 4])
        self._edges = []
        self._meshes = []

    def add_node(self, nx, ny, nz):
        self._nodes = np.vstack((self._nodes, np.array([nx, ny, nz, 1])))

    def add_nodes(self, node_arr):
        ones_col = np.ones([len(node_arr), 1])
        ones_added = np.hstack((node_arr, ones_col))
        self._nodes = np.vstack((self._nodes, ones_added))

    def add_edge(self, edge):
        self._edges.append(edge)

    def add_edges(self, edge_list):
        self._edges.extend(edge_list)

    def add_mesh(self, mesh):
        self._meshes.append(mesh)

    def add_meshes(self, mesh_list):
        self._edges.extend(mesh_list)

    def build(self):
        return Wireframe(self._nodes, self._edges, self._meshes)
