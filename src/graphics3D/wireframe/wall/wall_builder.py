import numpy as np
from shapely.geometry import LineString

from graphics3D.wireframe.alias import color
from graphics3D.wireframe.wall.wall import Wall
from graphics3D.wireframe.wireframe_builder import WireframeBuilder


class WallBuilder(WireframeBuilder):

    def __init__(self, base: LineString, height: int, edge_color: color, mesh_color: color) -> None:
        super().__init__()
        self._base = base
        self._normal = WallBuilder._create_normal(base)
        self._height = height
        self._edge_color = edge_color
        self._mesh_color = mesh_color

    @staticmethod
    def _create_normal(line: LineString) -> LineString:
        # Normal is always on the 'right' side when facing in the direction of the line
        # This is with reference to how the wall will be built; when facing the wall standing at the normal
        # the winding order of the wall nodes will be ccw.
        start, end = tuple(line.coords)
        cx, cy = line.centroid.coords[0]
        normal = np.array([end[1] - start[1], -(end[0] - start[0])])
        normal /= np.linalg.norm(normal)
        return LineString([(cx, cy), (cx + normal[0], cy + normal[1])])

    def build(self) -> Wall:
        start, end = tuple(self._base.coords)
        self.add_node(start[0], 0, start[1])
        self.add_node(end[0], 0, end[1])
        self.add_node(end[0], self._height, end[1])
        self.add_node(start[0], self._height, start[1])
        self.add_edges([((0, 1), self._edge_color), ((1, 2), self._edge_color),
                        ((2, 3), self._edge_color), ((3, 0), self._edge_color)])
        self.add_mesh(((0, 1, 2, 3), self._mesh_color))
        return Wall(self._nodes, tuple(self._edges), tuple(self._meshes), self._base, self._normal)
