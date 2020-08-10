import math

import numpy as np

from graphics3D.coord import Coord


class Camera:

    def __init__(self, focal_length=1, canvas_width=1, canvas_height=1):
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
        self.coords.translate(0, 0, self.displacement)

    def dolly_backward(self):
        self.coords.translate(0, 0, -self.displacement)

    def truck_left(self):
        self.coords.translate(self.displacement, 0, 0)

    def truck_right(self):
        self.coords.translate(-self.displacement, 0, 0)

    def pedestal_up(self):
        self.coords.translate(0, -self.displacement, 0)

    def pedestal_down(self):
        self.coords.translate(0, self.displacement, 0)

    def tilt_up(self):
        self.coords.rotate_about_x_axis(-self.keyboard_rotation_angle)

    def tilt_down(self):
        self.coords.rotate_about_x_axis(self.keyboard_rotation_angle)

    def mouse_tilt(self, dist):
        self.coords.rotate_about_x_axis(dist * self.mouse_rotation_angle)

    def pan_left(self):
        self.coords.rotate_about_y_axis(-self.keyboard_rotation_angle)

    def pan_right(self):
        self.coords.rotate_about_y_axis(self.keyboard_rotation_angle)

    def mouse_pan(self, dist):
        self.coords.rotate_about_y_axis(dist * self.mouse_rotation_angle)

    def roll_left(self):
        self.coords.rotate_about_z_axis(-self.keyboard_rotation_angle)

    def roll_right(self):
        self.coords.rotate_about_z_axis(self.keyboard_rotation_angle)

    def get_global_xz_aligned_vector(self, local_v):
        global_v = self.coords.change_to_global_basis(local_v)
        global_v[1] = 0
        new_local_v = self.coords.change_to_local_basis(global_v)
        return new_local_v

    def dolly_forward_xz_aligned(self):
        new_local_z = self.get_global_xz_aligned_vector(np.array((0, 0, self.displacement, 0)))
        self.coords.translate(new_local_z[0], new_local_z[1], new_local_z[2])

    def dolly_backward_xz_aligned(self):
        new_local_z = self.get_global_xz_aligned_vector(np.array((0, 0, -self.displacement, 0)))
        self.coords.translate(new_local_z[0], new_local_z[1], new_local_z[2])

    def truck_left_xz_aligned(self):
        new_local_x = self.get_global_xz_aligned_vector(np.array((self.displacement, 0, 0, 0)))
        self.coords.translate(new_local_x[0], new_local_x[1], new_local_x[2])

    def truck_right_xz_aligned(self):
        new_local_x = self.get_global_xz_aligned_vector(np.array((-self.displacement, 0, 0, 0)))
        self.coords.translate(new_local_x[0], new_local_x[1], new_local_x[2])


if __name__ == "__main__":
    pass
