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
        # Project vector in standard basis onto xz plane
        global_v = self.coords.change_to_global_basis(local_v)
        global_v[1] = 0
        new_local_v = self.coords.change_to_local_basis(global_v)
        # Return a vector in the camera basis with magnitude of the original vector
        return np.linalg.norm(local_v) * (new_local_v / np.linalg.norm(new_local_v))

    def pedestal_up(self):
        up = self.coords.change_to_local_basis(np.array([0, -self.displacement, 0, 0]))
        self.coords.translate(up[0], up[1], up[2])

    def pedestal_down(self):
        down = self.coords.change_to_local_basis(np.array([0, self.displacement, 0, 0]))
        self.coords.translate(down[0], down[1], down[2])

    def tilt_up(self):
        self.coords.rotate_about_x_axis(-self.keyboard_rotation_angle)

    def tilt_down(self):
        self.coords.rotate_about_x_axis(self.keyboard_rotation_angle)

    def mouse_tilt(self, dist):
        self.coords.rotate_about_x_axis(dist * self.mouse_rotation_angle)

    def pan_left(self):
        axis_of_rotation = self.coords.change_to_local_basis(np.array([0, 1, 0, 0]))
        self.coords.rotate_about_arb_axis(axis_of_rotation, -self.keyboard_rotation_angle)

    def pan_right(self):
        axis_of_rotation = self.coords.change_to_local_basis(np.array([0, 1, 0, 0]))
        self.coords.rotate_about_arb_axis(axis_of_rotation, self.keyboard_rotation_angle)

    def mouse_pan(self, dist):
        axis_of_rotation = self.coords.change_to_local_basis(np.array([0, 1, 0, 0]))
        self.coords.rotate_about_arb_axis(axis_of_rotation, dist * self.mouse_rotation_angle)

    def roll_left(self):
        pass

    def roll_right(self):
        pass
