import numpy as np

from graphics3D.coord import Coord


class Wireframe:

    def __init__(self):
        self.coord = Coord(np.array([[1, 0, 0, 0],
                                     [0, 1, 0, 0],
                                     [0, 0, 1, 0],
                                     [0, 0, 0, 1]]))
        self.nodes = np.empty([0, 4])
        self.edges = []
        self.meshes = []

    def add_node(self, nx, ny, nz):
        self.nodes = np.vstack((self.nodes, np.array([nx, ny, nz, 1])))

    def add_nodes(self, node_arr):
        ones_col = np.ones([len(node_arr), 1])
        ones_added = np.hstack((node_arr, ones_col))
        self.nodes = np.vstack((self.nodes, ones_added))

    def add_edge(self, edge):
        self.edges.append(edge)

    def add_edges(self, edge_list):
        self.edges.extend(edge_list)

    def add_mesh(self, mesh):
        self.meshes.append(mesh)

    def add_meshes(self, mesh_list):
        self.edges.extend(mesh_list)

    def output_Nodes(self):
        print("\n --- Nodes --- ")
        for i, (x, y, z, _) in enumerate(self.nodes):
            print("   %d: (%d, %d, %d)" % (i, x, y, z))

    def get_global_nodes(self):
        return self.coord.change_to_global_basis(self.nodes)

    def get_global_edges(self):
        global_edges = []
        for n1, n2, color in self.edges:
            node1, node2 = self.nodes[n1], self.nodes[n2]
            c1 = self.coord.change_to_global_basis(node1)
            c2 = self.coord.change_to_global_basis(node2)
            global_edges.append((c1, c2, color))
        return global_edges

    def get_global_meshes(self):
        global_meshes = []
        for mesh in self.meshes:
            mesh_node_list = []
            for n in mesh[0]:
                node = self.nodes[n]
                c = self.coord.change_to_global_basis(node)
                mesh_node_list.append(c)
            global_meshes.append((mesh_node_list, mesh[1]))
        return global_meshes


if __name__ == "__main__":
    pass
