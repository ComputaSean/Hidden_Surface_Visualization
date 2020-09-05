from math import cos, sin

import numpy as np


class Coord:

    def __init__(self, basis: np.array) -> None:
        self.basis = basis

    def rotate_about_arb_axis(self, axis: np.array, angle: float) -> None:
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
        self.basis = np.matmul(self.basis, rotation_matrix)

    def rotate_about_x_axis(self, angle: float) -> None:
        rotation_matrix = np.array([[1, 0, 0, 0],
                                    [0, cos(angle), sin(angle), 0],
                                    [0, -sin(angle), cos(angle), 0],
                                    [0, 0, 0, 1]])
        self.basis = np.matmul(self.basis, rotation_matrix)

    def rotate_about_y_axis(self, angle: float) -> None:
        rotation_matrix = np.array([[cos(angle), 0, -sin(angle), 0],
                                    [0, 1, 0, 0],
                                    [sin(angle), 0, cos(angle), 0],
                                    [0, 0, 0, 1]])
        self.basis = np.matmul(self.basis, rotation_matrix)

    def rotate_about_z_axis(self, angle: float) -> None:
        rotation_matrix = np.array([[cos(angle), sin(angle), 0, 0],
                                    [-sin(angle), cos(angle), 0, 0],
                                    [0, 0, 1, 0],
                                    [0, 0, 0, 1]])
        self.basis = np.matmul(self.basis, rotation_matrix)

    def translate(self, x_units: float, y_units: float, z_units: float) -> None:
        """
        Units are in the basis of self
        :return:
        """
        translation_matrix = np.array([[1, 0, 0, 0],
                                       [0, 1, 0, 0],
                                       [0, 0, 1, 0],
                                       [x_units, y_units, z_units, 1]])
        self.basis = np.matmul(self.basis, translation_matrix)

    def scale(self, x_factor: float, y_factor: float, z_factor: float) -> None:
        """
        Units are in the basis of self
        :return:
        """
        scale_matrix = np.array([[x_factor, 0, 0, 0],
                                 [0, y_factor, 0, 0],
                                 [0, 0, z_factor, 0],
                                 [0, 0, 0, 1]])
        self.basis = np.matmul(self.basis, scale_matrix)

    def change_to_local_basis(self, v: np.array) -> np.array:
        """
        Change of basis from global basis to local basis.
        Applies all the transformations.

        :param v: vector expressed in local basis
        :return:
        """
        return np.matmul(v, self.basis)

    def change_to_global_basis(self, v: np.array) -> np.array:
        """
        Change of basis from local basis to global basis.
        Undoes all the transformations.

        :param v: vector expresses in global basis
        :return:
        """
        return np.matmul(v, np.linalg.inv(self.basis))
