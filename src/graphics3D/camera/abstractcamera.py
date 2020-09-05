import math

import numpy as np

from graphics3D.coordsys.coord import Coord


class AbstractCamera:

    def __init__(self, focal_length: float, canvas_width: int, canvas_height: int):
        self.coords = Coord(np.array([[1, 0, 0, 0],
                                      [0, 1, 0, 0],
                                      [0, 0, -1, 0],
                                      [0, 0, 0, 1]]))
        self.focal_length = focal_length
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.keyboard_rotation_angle = math.pi / 180
        self.mouse_rotation_angle = math.pi / 1800
        self.displacement = 10

    def dolly_forward(self) -> None:
        raise NotImplementedError

    def dolly_backward(self) -> None:
        raise NotImplementedError

    def truck_left(self) -> None:
        raise NotImplementedError

    def truck_right(self) -> None:
        raise NotImplementedError

    def pedestal_up(self) -> None:
        raise NotImplementedError

    def pedestal_down(self) -> None:
        raise NotImplementedError

    def tilt_up(self) -> None:
        raise NotImplementedError

    def tilt_down(self) -> None:
        raise NotImplementedError

    def mouse_tilt(self, dist: float) -> None:
        raise NotImplementedError

    def pan_left(self) -> None:
        raise NotImplementedError

    def pan_right(self) -> None:
        raise NotImplementedError

    def mouse_pan(self, dist) -> None:
        raise NotImplementedError

    def roll_left(self) -> None:
        raise NotImplementedError

    def roll_right(self) -> None:
        raise NotImplementedError
