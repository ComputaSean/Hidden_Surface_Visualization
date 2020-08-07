from random import randrange

import numpy as np
from shapely.geometry import LineString


class VectorLine(LineString):

    def __init__(self, points, normal_dir=randrange(-1, 2, 2)):
        super().__init__(points)
        self.normal_dir = normal_dir
        self.normal = VectorLine.__create_normal(self, normal_dir)

    @staticmethod
    def __create_normal(line, direction):
        start, end = tuple(line.coords)
        # Calculate normal components
        nx = direction * (end[1] - start[1])
        ny = -direction * (end[0] - start[0])
        normal = np.array([nx, ny])
        normal /= np.linalg.norm(normal)
        cx, cy = line.centroid.coords[0]
        return LineString([(cx, cy), (cx + normal[0], cy + normal[1])])
