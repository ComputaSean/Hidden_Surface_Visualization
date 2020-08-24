import numpy as np
from shapely.geometry import LineString

from graphics3D.wireframe.wall import Wall
from graphics3D.wireframe.wireframe_builder import WireframeBuilder


class WallBuilder(WireframeBuilder):

    def __init__(self, base, height, edge_color, mesh_color):
        super().__init__()
        self._base = base
        self._normal = self._create_normal(base)
        self._height = height
        self._edge_color = edge_color
        self._mesh_color = mesh_color

    @staticmethod
    def _create_normal(line):
        start, end = tuple(line.coords)
        # Calculate normal components
        nx = end[1] - start[1]
        ny = -(end[0] - start[0])
        normal = np.array([nx, ny])
        normal /= np.linalg.norm(normal)
        cx, cy = line.centroid.coords[0]
        return LineString([(cx, cy), (cx + normal[0], cy + normal[1])])

    def build(self):
        start, end = tuple(self._base.coords)
        self.add_node(start[0], 0, start[1])
        self.add_node(end[0], 0, end[1])
        self.add_node(end[0], self._height, end[1])
        self.add_node(start[0], self._height, start[1])
        self.add_edges(((0, 1, self._edge_color), (1, 2, self._edge_color),
                        (2, 3, self._edge_color), (3, 0, self._edge_color)))
        self.add_mesh(((0, 1, 2, 3), self._mesh_color))
        return Wall(self._nodes, self._edges, self._meshes, self._base, self._normal)
