from random import randrange

import numpy as np
from shapely.geometry import LineString


class VectorLine(LineString):

    def __init__(self, points, normal=None):
        super().__init__(points)
        self.direction = VectorLine.__create_direction(self)
        self.normal = VectorLine.__create_normal(self) if normal is None else normal

    @staticmethod
    def __create_direction(line):
        start, end = tuple(line.coords)
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        direction = np.array([dx, dy])
        direction /= np.linalg.norm(direction)
        return direction

    @staticmethod
    def __create_normal(line):
        start, end = tuple(line.coords)
        direction = randrange(-1, 2, 2)
        # Calculate normal components
        nx = direction * (end[1] - start[1])
        ny = -direction * (end[0] - start[0])
        normal = np.array([nx, ny])
        normal /= np.linalg.norm(normal)
        return normal

    def get_plot(self):
        start, end = tuple(self.coords)
        return (start[0], end[0]), (start[1], end[1])

    def get_normal_plot(self):
        cx, cy = self.centroid.coords[0]
        nx, ny = self.normal
        return (cx, cx + nx), (cy, cy + ny)

    def get_direction(self):
        return self.direction

    def is_vertical(self):
        return self.direction[1] == 1

    def is_horizontal(self):
        return self.direction[0] == 1
