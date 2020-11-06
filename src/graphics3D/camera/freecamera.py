from graphics3D.camera.abstractcamera import AbstractCamera


class FreeCamera(AbstractCamera):
    """
    All camera motions are relative to the camera's frame of reference.
    For example, if the camera is 'upside-down', then pedestalling down will appear to move it 'up' viewing from
    a 'right side up' perspective.
    """

    def __init__(self, focal_length: float = 1, canvas_width: int = 1, canvas_height: int = 1):
        super().__init__(focal_length, canvas_width, canvas_height)

    def dolly_forward(self) -> None:
        self.coords.translate(0, 0, self.displacement)

    def dolly_backward(self) -> None:
        self.coords.translate(0, 0, -self.displacement)

    def truck_left(self) -> None:
        self.coords.translate(self.displacement, 0, 0)

    def truck_right(self) -> None:
        self.coords.translate(-self.displacement, 0, 0)

    def pedestal_up(self) -> None:
        self.coords.translate(0, -self.displacement, 0)

    def pedestal_down(self) -> None:
        self.coords.translate(0, self.displacement, 0)

    def tilt_up(self) -> None:
        self.coords.rotate_about_x_axis(-self.keyboard_rotation_angle)

    def tilt_down(self) -> None:
        self.coords.rotate_about_x_axis(self.keyboard_rotation_angle)

    def mouse_tilt(self, dist) -> None:
        self.coords.rotate_about_x_axis(dist * self.mouse_rotation_angle)

    def pan_left(self) -> None:
        self.coords.rotate_about_y_axis(-self.keyboard_rotation_angle)

    def pan_right(self) -> None:
        self.coords.rotate_about_y_axis(self.keyboard_rotation_angle)

    def mouse_pan(self, dist: float) -> None:
        self.coords.rotate_about_y_axis(dist * self.mouse_rotation_angle)

    def roll_left(self) -> None:
        self.coords.rotate_about_z_axis(-self.keyboard_rotation_angle)

    def roll_right(self) -> None:
        self.coords.rotate_about_z_axis(self.keyboard_rotation_angle)
