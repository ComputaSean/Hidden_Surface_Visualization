import math

import numpy as np

from graphics3D.coordsys.coord import Coord


class AbstractCamera:
    """
    Base class for all camera types. Cameras should support all normal camera motions.
    Cameras are able to be controlled using a mouse and/or a keyboard.
    """

    def __init__(self, focal_length: float, canvas_width: int, canvas_height: int):
        # Camera faces towards the -z axis.
        self.coords = Coord(np.array([[1, 0, 0, 0],
                                      [0, 1, 0, 0],
                                      [0, 0, -1, 0],
                                      [0, 0, 0, 1]]))
        # Camera distance from the near plane
        self.focal_length = focal_length
        # Near plane dimensions
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        # Mouse/keyboard values for camera motion
        self.keyboard_rotation_angle = math.pi / 180
        self.mouse_rotation_angle = math.pi / 1800
        self.displacement = 10

    def dolly_forward(self) -> None:
        """
        Moves the camera forward.

        :return: None
        """
        raise NotImplementedError

    def dolly_backward(self) -> None:
        """
        Moves the camera backward.

        :return: None
        """
        raise NotImplementedError

    def truck_left(self) -> None:
        """
        Moves the camera left.

        :return: None
        """
        raise NotImplementedError

    def truck_right(self) -> None:
        """
        Moves the camera right.

        :return: None
        """
        raise NotImplementedError

    def pedestal_up(self) -> None:
        """
        Moves the camera up.

        :return: None
        """
        raise NotImplementedError

    def pedestal_down(self) -> None:
        """
        Moves the camera down.

        :return: None
        """
        raise NotImplementedError

    def tilt_up(self) -> None:
        """
        Camera is tilted up.

        :return: None
        """
        raise NotImplementedError

    def tilt_down(self) -> None:
        """
        Camera is tilted down.

        :return: None
        """
        raise NotImplementedError

    def mouse_tilt(self, dist: float) -> None:
        """
        Camera is tilted down using the mouse.

        :param dist: the amount the camera is tilted
        :return: None
        """
        raise NotImplementedError

    def pan_left(self) -> None:
        """
        Camera pans to the left.

        :return: None
        """
        raise NotImplementedError

    def pan_right(self) -> None:
        """
        Camera pans to the right.

        :return: None
        """
        raise NotImplementedError

    def mouse_pan(self, dist) -> None:
        """
        Camera is panned using the mouse.
        :param dist: the amount the camera is panned

        :return: None
        """
        raise NotImplementedError

    def roll_left(self) -> None:
        """
        Camera rolls left.

        :return: None
        """
        raise NotImplementedError

    def roll_right(self) -> None:
        """
        Camera rolls right.

        :return: None
        """
        raise NotImplementedError
