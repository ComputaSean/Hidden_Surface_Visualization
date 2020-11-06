from math import cos, sin

import numpy as np


class Coord:
    """
    A 4x4 matrix representing the basis of a coordinate system in R^3.
    This matrix is represented in row-major order.
    """

    def __init__(self, basis: np.ndarray) -> None:
        self._basis = basis  # global to coordinate change of basis

    def rotate_about_arb_axis(self, axis: np.ndarray, angle: float) -> None:
        """
        Applies a rotation matrix from a given axis and angle.
        Credit to https://en.wikipedia.org/wiki/Rotation_matrix#Rotation_matrix_from_axis_and_angle.

        :param axis: axis of rotation
        :param angle: amount to rotate by
        :return: None
        """
        normalized = axis / np.linalg.norm(axis)
        ux = normalized[0]
        uy = normalized[1]
        uz = normalized[2]
        c = cos(angle)
        s = sin(angle)
        rotation_matrix = np.array(
            [[c + (ux ** 2) * (1 - c), uy * ux * (1 - c) + uz * s, uz * ux * (1 - c) - uy * s, 0],
             [ux * uy * (1 - c) - uz * s, c + (uy ** 2) * (1 - c), uz * uy * (1 - c) + ux * s, 0],
             [ux * uz * (1 - c) + uy * s, uy * uz * (1 - c) - ux * s, c + (uz ** 2) * (1 - c), 0],
             [0, 0, 0, 1]])
        self._basis = np.matmul(self._basis, rotation_matrix)

    def rotate_about_x_axis(self, angle: float) -> None:
        """
        Applies a rotation matrix that rotates the basis around the x-axis by a given angle.

        :param angle: amount to rotate by
        :return: None
        """
        rotation_matrix = np.array([[1, 0, 0, 0],
                                    [0, cos(angle), sin(angle), 0],
                                    [0, -sin(angle), cos(angle), 0],
                                    [0, 0, 0, 1]])
        self._basis = np.matmul(self._basis, rotation_matrix)

    def rotate_about_y_axis(self, angle: float) -> None:
        """
        Applies a rotation matrix that rotates the basis around the y-axis by a given angle.

        :param angle: amount to rotate by
        :return: None
        """
        rotation_matrix = np.array([[cos(angle), 0, -sin(angle), 0],
                                    [0, 1, 0, 0],
                                    [sin(angle), 0, cos(angle), 0],
                                    [0, 0, 0, 1]])
        self._basis = np.matmul(self._basis, rotation_matrix)

    def rotate_about_z_axis(self, angle: float) -> None:
        """
        Applies a rotation matrix that rotates the basis around the z-axis by a given angle.

        :param angle: amount to rotate by
        :return: None
        """
        rotation_matrix = np.array([[cos(angle), sin(angle), 0, 0],
                                    [-sin(angle), cos(angle), 0, 0],
                                    [0, 0, 1, 0],
                                    [0, 0, 0, 1]])
        self._basis = np.matmul(self._basis, rotation_matrix)

    def translate(self, x_units: float, y_units: float, z_units: float) -> None:
        """
        Applies a translation matrix to the basis.
        Note that all units are given with respect to the coordinate basis.

        :param x_units: amount to translate along the x-axis
        :param y_units: amount to translate along the y-axis
        :param z_units: amount to translate along the z-axis
        :return: None
        """
        translation_matrix = np.array([[1, 0, 0, 0],
                                       [0, 1, 0, 0],
                                       [0, 0, 1, 0],
                                       [x_units, y_units, z_units, 1]])
        self._basis = np.matmul(self._basis, translation_matrix)

    def scale(self, x_factor: float, y_factor: float, z_factor: float) -> None:
        """
        Applies a scaling matrix to the basis.

        :param x_factor: amount to scale the x-axis by
        :param y_factor: amount to scale the y-axis by
        :param z_factor: amount to scale the z-axis by
        :return: None
        """
        scale_matrix = np.array([[x_factor, 0, 0, 0],
                                 [0, y_factor, 0, 0],
                                 [0, 0, z_factor, 0],
                                 [0, 0, 0, 1]])
        self._basis = np.matmul(self._basis, scale_matrix)

    def change_to_local_basis(self, v: np.ndarray) -> np.ndarray:
        """
        Change of basis from the global basis to the local coordinate basis.

        :param v: vector expressed in the global basis
        :return: v expressed in the local basis
        """
        return np.matmul(v, self._basis)

    def change_to_global_basis(self, v: np.ndarray) -> np.ndarray:
        """
        Change of basis from the local coordinate basis to the global basis.

        :param v: vector expressed in the local basis
        :return: v expressed in the global basis
        """
        return np.matmul(v, np.linalg.inv(self._basis))
