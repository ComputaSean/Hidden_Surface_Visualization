from math import cos, sin

import numpy as np


class Coord:

    def __init__(self, basis):
        self.basis = basis

    def rotate_about_arb_axis(self, axis, angle):
        normalized = axis / np.linalg.norm(axis)
        ux = normalized[0]
        uy = normalized[1]
        uz = normalized[2]
        c = cos(angle)
        s = sin(angle)
        rotation_matrix = np.array(
            [[c + (ux ** 2) * (1 - c), ux * uy * (1 - c) - uz * s, ux * uz * (1 - c) + uy * s, 0],
             [uy * ux * (1 - c) + uz * s, c + (uy ** 2) * (1 - c), uy * uz * (1 - c) - ux * s, 0],
             [uz * ux * (1 - c) - uy * s, uz * uy * (1 - c) + ux * s, c + (uz ** 2) * (1 - c), 0],
             [0, 0, 0, 1]]).T
        # np.array([[c + (ux ** 2) * (1 - c), uy * ux * (1 - c) + uz * s, uz * ux * (1 - c) - uy * s, 0],
        #           [ux * uy * (1 - c) - ux * s, c + (uy ** 2) * (1 - c), uz * uy * (1 - c) + ux * s, 0],
        #           [ux * uz * (1 - c) + uy * s, uy * uz * (1 - c) - ux * s, c + (uz ** 2) * (1 - c), 0],
        #           [0, 0, 0, 1]])

        self.basis = np.matmul(self.basis, rotation_matrix)

    def rotate_about_x_axis(self, angle):
        self.basis = np.matmul(self.basis, Coord.__get_x_rotation_matrix(angle))

    # def rotate_about_x_axis_limited(self, angle):
    #     rotation_result = np.matmul(self.basis, Coord.__get_x_rotation_matrix(angle))
    #     new_z_global = self.change_to_global_basis(np.array([0, 0, 1, 0]))
    #     cross_product = np.cross(new_z_global[:3], np.array([0, 1, 0]))
    #     print(np.linalg.norm(cross_product))
    #     if np.linalg.norm(cross_product) > 0.5:
    #         self.basis = rotation_result

    @staticmethod
    def __get_x_rotation_matrix(a):
        return np.array([[1, 0, 0, 0],
                         [0, cos(a), sin(a), 0],
                         [0, -sin(a), cos(a), 0],
                         [0, 0, 0, 1]])

    def rotate_about_y_axis(self, angle):
        self.basis = np.matmul(self.basis, Coord.__get_y_rotation_matrix(angle))

    @staticmethod
    def __get_y_rotation_matrix(a):
        return np.array([[cos(a), 0, -sin(a), 0],
                         [0, 1, 0, 0],
                         [sin(a), 0, cos(a), 0],
                         [0, 0, 0, 1]])

    def rotate_about_z_axis(self, angle):
        self.basis = np.matmul(self.basis, Coord.__get_z_rotation_matrix(angle))

    @staticmethod
    def __get_z_rotation_matrix(a):
        return np.array([[cos(a), sin(a), 0, 0],
                         [-sin(a), cos(a), 0, 0],
                         [0, 0, 1, 0],
                         [0, 0, 0, 1]])

    def translate(self, x_units, y_units, z_units):
        """
        Units are in the basis of self
        :param x_units:
        :param y_units:
        :param z_units:
        :return:
        """
        self.basis = np.matmul(self.basis, self.__get_translation_matrix(x_units, y_units, z_units))

    @staticmethod
    def __get_translation_matrix(x_units, y_units, z_units):
        return np.array([[1, 0, 0, 0],
                         [0, 1, 0, 0],
                         [0, 0, 1, 0],
                         [x_units, y_units, z_units, 1]])

    def scale(self, x_factor, y_factor, z_factor):
        """
        Units are in the basis of self
        :param x_units:
        :param y_units:
        :param z_units:
        :return:
        """
        self.basis = np.matmul(self.basis, self.__get_scale_matrix(x_factor, y_factor, z_factor))

    @staticmethod
    def __get_scale_matrix(x_factor, y_factor, z_factor):
        return np.array([[x_factor, 0, 0, 0],
                         [0, y_factor, 0, 0],
                         [0, 0, z_factor, 0],
                         [0, 0, 0, 1]])

    def change_to_local_basis(self, v):
        """
        Change of basis from global basis to local basis.
        Applies all the transformations.

        :param v: vector expressed in local basis
        :return:
        """
        return np.matmul(v, self.basis)

    def change_to_global_basis(self, v):
        """
        Change of basis from local basis to global basis.
        Undoes all the transformations.

        :param v: vector expresses in global basis
        :return:
        """
        return np.matmul(v, np.linalg.inv(self.basis))


if __name__ == "__main__":
    pass
