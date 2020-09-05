from typing import Tuple

from numpy import ndarray
from shapely.geometry import LineString

from graphics3D.wireframe.alias import edge, mesh
from graphics3D.wireframe.wireframe import Wireframe


class Wall(Wireframe):

    def __init__(self, nodes: ndarray, edges: Tuple[edge], meshes: Tuple[mesh],
                 base: LineString, normal: LineString) -> None:
        super().__init__(nodes, edges, meshes)
        self.base = base
        self.normal = normal
