from typing import Tuple, Generator

import numpy as np
from shapely.geometry import LineString
from shapely.ops import split

from sptree.partitionable import Partitionable

Color = Tuple[int, int, int]


class Wall(Partitionable):
    """
    A 3D rectangular wall defined by four corner nodes.
    The edges and nodes can have a different color from the wall itself.
    """

    def __init__(self, base: LineString, height: int, node_color: Color, edge_color: Color, wall_color: Color) -> None:
        self._base = base
        self._height = height
        self.nodes = Wall._create_nodes(base, height)
        self.node_color = node_color
        self.edge_color = edge_color
        self.wall_color = wall_color

    @staticmethod
    def _create_nodes(base: LineString, height: int) -> np.ndarray:
        """
        Create the corner nodes of the wall.
        :param base: line parallel to the ground
        :param height: height of the wall
        :return: array of corner nodes
        """
        start, end = tuple(base.coords)
        nodes = np.empty([0, 4])
        nodes = np.vstack((nodes, np.array([start[0], 0, start[1], 1])))
        nodes = np.vstack((nodes, np.array([end[0], 0, end[1], 1])))
        nodes = np.vstack((nodes, np.array([end[0], height, end[1], 1])))
        nodes = np.vstack((nodes, np.array([start[0], height, start[1], 1])))
        return nodes

    def get_edges(self) -> Generator[Tuple[np.ndarray, np.ndarray], None, None]:
        """
        :return: edges of the wall
        """
        for i in range(4):
            yield self.nodes[i % 4], self.nodes[(i + 1) % 4]
        return

    def get_nodes(self) -> Generator[np.ndarray, None, None]:
        """
        :return: corner nodes
        """
        for i in range(4):
            yield self.nodes[i]
        return

    def split(self, part: Partitionable) -> Tuple[Partitionable, Partitionable]:
        first_half, second_half = split(self._base, part.get_base())
        return Wall(LineString(first_half.coords), self._height, self.node_color, (255, 255, 255), self.wall_color), \
               Wall(LineString(second_half.coords), self._height, self.node_color, (255, 255, 255), self.wall_color)

    def get_base(self) -> LineString:
        return self._base
