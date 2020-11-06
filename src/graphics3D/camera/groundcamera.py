import numpy as np

from graphics3D.camera.abstractcamera import AbstractCamera


class GroundCamera(AbstractCamera):
    """
    Camera motions are done with respect to the ground/xz-plane.
    """

    def __init__(self, focal_length: float = 1, canvas_width: int = 1, canvas_height: int = 1):
        super().__init__(focal_length, canvas_width, canvas_height)

    def dolly_forward(self) -> None:
        new_local_z = self._get_global_xz_aligned_vector(np.array((0, 0, self.displacement, 0)))
        self.coords.translate(new_local_z[0], new_local_z[1], new_local_z[2])

    def dolly_backward(self) -> None:
        new_local_z = self._get_global_xz_aligned_vector(np.array((0, 0, -self.displacement, 0)))
        self.coords.translate(new_local_z[0], new_local_z[1], new_local_z[2])

    def truck_left(self) -> None:
        new_local_x = self._get_global_xz_aligned_vector(np.array((self.displacement, 0, 0, 0)))
        self.coords.translate(new_local_x[0], new_local_x[1], new_local_x[2])

    def truck_right(self) -> None:
        new_local_x = self._get_global_xz_aligned_vector(np.array((-self.displacement, 0, 0, 0)))
        self.coords.translate(new_local_x[0], new_local_x[1], new_local_x[2])

    def _get_global_xz_aligned_vector(self, local_v: np.ndarray) -> np.ndarray:
        """
        Converts a local vector into another local vector that is parallel to the global xz-plane.

        :param local_v: vector in the local basis of the camera
        :return: vector of the same magnitude that is parallel to the global xz-plane
        """
        # Project vector in standard basis onto xz plane
        global_v = self.coords.change_to_global_basis(local_v)
        global_v[1] = 0
        new_local_v = self.coords.change_to_local_basis(global_v)
        # Return a vector in the camera basis with magnitude of the original vector
        return np.linalg.norm(local_v) * (new_local_v / np.linalg.norm(new_local_v))

    def pedestal_up(self) -> None:
        up = self.coords.change_to_local_basis(np.array([0, -self.displacement, 0, 0]))
        self.coords.translate(up[0], up[1], up[2])

    def pedestal_down(self) -> None:
        down = self.coords.change_to_local_basis(np.array([0, self.displacement, 0, 0]))
        self.coords.translate(down[0], down[1], down[2])

    def tilt_up(self) -> None:
        self.coords.rotate_about_x_axis(-self.keyboard_rotation_angle)

    def tilt_down(self) -> None:
        self.coords.rotate_about_x_axis(self.keyboard_rotation_angle)

    def mouse_tilt(self, dist) -> None:
        self.coords.rotate_about_x_axis(dist * self.mouse_rotation_angle)

    def pan_left(self) -> None:
        axis_of_rotation = self.coords.change_to_local_basis(np.array([0, 1, 0, 0]))
        self.coords.rotate_about_arb_axis(axis_of_rotation, -self.keyboard_rotation_angle)

    def pan_right(self) -> None:
        axis_of_rotation = self.coords.change_to_local_basis(np.array([0, 1, 0, 0]))
        self.coords.rotate_about_arb_axis(axis_of_rotation, self.keyboard_rotation_angle)

    def mouse_pan(self, dist) -> None:
        axis_of_rotation = self.coords.change_to_local_basis(np.array([0, 1, 0, 0]))
        self.coords.rotate_about_arb_axis(axis_of_rotation, dist * self.mouse_rotation_angle)

    def roll_left(self):
        pass

    def roll_right(self):
        pass
