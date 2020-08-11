from graphics3D.camera.abstractcamera import AbstractCamera


class FreeCamera(AbstractCamera):

    def __init__(self, focal_length=1, canvas_width=1, canvas_height=1):
        super().__init__(focal_length, canvas_width, canvas_height)

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
