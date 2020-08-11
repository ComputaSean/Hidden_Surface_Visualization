import math

import numpy as np

from graphics3D.coord import Coord


class AbstractCamera:

    def __init__(self, focal_length, canvas_width, canvas_height):
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

    def dolly_forward(self):
        raise NotImplementedError

    def dolly_backward(self):
        raise NotImplementedError

    def truck_left(self):
        raise NotImplementedError

    def truck_right(self):
        raise NotImplementedError

    def pedestal_up(self):
        raise NotImplementedError

    def pedestal_down(self):
        raise NotImplementedError

    def tilt_up(self):
        raise NotImplementedError

    def tilt_down(self):
        raise NotImplementedError

    def mouse_tilt(self, dist):
        raise NotImplementedError

    def pan_left(self):
        raise NotImplementedError

    def pan_right(self):
        raise NotImplementedError

    def mouse_pan(self, dist):
        raise NotImplementedError

    def roll_left(self):
        raise NotImplementedError

    def roll_right(self):
        raise NotImplementedError
