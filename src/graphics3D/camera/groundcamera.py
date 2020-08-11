import numpy as np

from graphics3D.camera.abstractcamera import AbstractCamera


class GroundCamera(AbstractCamera):

    def __init__(self, focal_length=1, canvas_width=1, canvas_height=1):
        super().__init__(focal_length, canvas_width, canvas_height)

    def dolly_forward(self):
        new_local_z = self.__get_global_xz_aligned_vector(np.array((0, 0, self.displacement, 0)))
        self.coords.translate(new_local_z[0], new_local_z[1], new_local_z[2])

    def dolly_backward(self):
        new_local_z = self.__get_global_xz_aligned_vector(np.array((0, 0, -self.displacement, 0)))
        self.coords.translate(new_local_z[0], new_local_z[1], new_local_z[2])

    def truck_left(self):
        new_local_x = self.__get_global_xz_aligned_vector(np.array((self.displacement, 0, 0, 0)))
        self.coords.translate(new_local_x[0], new_local_x[1], new_local_x[2])

    def truck_right(self):
        new_local_x = self.__get_global_xz_aligned_vector(np.array((-self.displacement, 0, 0, 0)))
        self.coords.translate(new_local_x[0], new_local_x[1], new_local_x[2])

    def __get_global_xz_aligned_vector(self, local_v):
        global_v = self.coords.change_to_global_basis(local_v)
        global_v[1] = 0
        new_local_v = self.coords.change_to_local_basis(global_v)
        return np.linalg.norm(local_v) * (new_local_v / np.linalg.norm(new_local_v))

    def pedestal_up(self):
        up = self.coords.change_to_local_basis(np.array([0, self.displacement, 0, 0]))
        self.coords.translate(up[0], up[1], up[2])

    def pedestal_down(self):
        down = self.coords.change_to_local_basis(np.array([0, -self.displacement, 0, 0]))
        self.coords.translate(down[0], down[1], down[2])

    # def tilt_up(self):
    #     global_x_axis = self.coords.change_to_local_basis(np.array([0, 0, 0, 0]))
    #     self.coords.rotate_about_arb_axis(global_x_axis, -self.keyboard_rotation_angle)
    #
    # def tilt_down(self):
    #     global_x_axis = self.coords.change_to_local_basis(np.array([1, 0, 0, 0]))
    #     self.coords.rotate_about_arb_axis(global_x_axis, self.keyboard_rotation_angle)

    def mouse_tilt(self, dist):
        gtl_x_axis = self.coords.change_to_local_basis(np.array([1, 0, 0, 0]))
        self.coords.rotate_about_arb_axis(gtl_x_axis, dist * self.mouse_rotation_angle)

    def pan_left(self):
        gtl_y_axis = self.coords.change_to_local_basis(np.array([0, 1, 0, 0]))
        self.coords.rotate_about_arb_axis(gtl_y_axis, -self.keyboard_rotation_angle)

    def pan_right(self):
        gtl_y_axis = self.coords.change_to_local_basis(np.array([0, 1, 0, 0]))
        self.coords.rotate_about_arb_axis(gtl_y_axis, self.keyboard_rotation_angle)

    def mouse_pan(self, dist):
        gtl_y_axis = self.coords.change_to_local_basis(np.array([0, 1, 0, 0]))
        self.coords.rotate_about_arb_axis(gtl_y_axis, dist * self.mouse_rotation_angle)

    def roll_left(self):
        self.coords.rotate_about_z_axis(-self.keyboard_rotation_angle)

    def roll_right(self):
        self.coords.rotate_about_z_axis(self.keyboard_rotation_angle)
