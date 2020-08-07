from enum import Enum
from random import shuffle

from shapely.geometry import box, LineString, Point
from shapely.ops import split

from src.world.VectorLine import VectorLine

error = 1e-13


class SPTree:

    def __init__(self, lines, bounding_box):
        shuffle(lines)
        self.root = SPTree.__construct(lines, bounding_box)
        self.bounding_box = bounding_box

    @staticmethod
    def __construct(lines, bounding_box):
        if len(lines) == 0:
            return None

        splitting_line = lines[0]
        coincident_lines = [splitting_line]
        front = []
        back = []

        splitting_plane = SPTree.__get_splitting_plane(splitting_line, bounding_box)

        for i in range(1, len(lines)):
            line = lines[i]
            line_start = Point(line.coords[0])
            line_end = Point(line.coords[1])
            # Coincident line to splitting line
            if splitting_plane.distance(line_start) < error and splitting_plane.distance(line_end) < error:
                coincident_lines.append(line)
            # Splitting line crosses line
            elif splitting_plane.crosses(line):
                first_half, second_half = split(line, splitting_plane)
                first_half = VectorLine(first_half.coords, line.normal_dir)
                second_half = VectorLine(second_half.coords, line.normal_dir)
                SPTree.__determine_side(first_half, splitting_line, splitting_plane, front, back)
                SPTree.__determine_side(second_half, splitting_line, splitting_plane, front, back)
            # Line enclosed within one of the planes created by the splitting plane
            else:
                SPTree.__determine_side(line, splitting_line, splitting_plane, front, back)

        front_node = SPTree.__construct(front, bounding_box)
        behind_node = SPTree.__construct(back, bounding_box)
        cur_node = Node(coincident_lines, front_node, behind_node)

        return cur_node

    @staticmethod
    def __determine_side(line, splitting_line, splitting_plane, front, behind):
        """
        Determines whether line is in front or behind splitting line.

        :param line:
        :param splitting_line:
        :param splitting_plane:
        :param front:
        :param behind:
        :return:
        """
        normal_end_point = Point(splitting_line.normal.coords[1])
        line_center_point = line.centroid
        connecting_line = LineString([line_center_point, normal_end_point])
        if connecting_line.crosses(splitting_plane):
            behind.append(line)
        else:
            front.append(line)

    @staticmethod
    def __get_splitting_plane(line, polygon):
        """
        Credit to https://stackoverflow.com/a/62413539
        :param line:
        :param polygon:
        :return:
        """
        minx, miny, maxx, maxy = polygon.bounds

        bounding_box = box(minx, miny, maxx, maxy)
        p1, p2 = line.boundary
        if p1.x == p2.x:  # vertical line
            extended_line = LineString([(p1.x, miny), (p1.x, maxy)])
        elif p1.y == p2.y:  # horizontal line
            extended_line = LineString([(minx, p1.y), (maxx, p1.y)])
        else:
            # linear equation: y = mx + b
            m = (p2.y - p1.y) / (p2.x - p1.x)  # Slope
            b = p1.y - m * p1.x  # y-intercept
            y0 = m * minx + b
            y1 = m * maxx + b
            x0 = (miny - b) / m
            x1 = (maxy - b) / m
            points_on_boundary_lines = [Point(minx, y0), Point(maxx, y1), Point(x0, miny), Point(x1, maxy)]
            unique_points_on_boundary_lines = []

            for p in points_on_boundary_lines:
                if p not in unique_points_on_boundary_lines:
                    unique_points_on_boundary_lines.append(p)

            points_sorted_by_distance = sorted(unique_points_on_boundary_lines, key=bounding_box.distance)
            extended_line = LineString(points_sorted_by_distance[:2])

        return extended_line

    @staticmethod
    def classify_perspective(point, splitting_line, bounding_box):
        normal_end_point = Point(splitting_line.normal.coords[1])
        connecting_line = LineString([point, normal_end_point])
        splitting_plane = SPTree.__get_splitting_plane(splitting_line, bounding_box)
        if splitting_plane.distance(point) < error:
            return Perspective.ON
        elif connecting_line.crosses(splitting_plane):
            return Perspective.BACK
        else:
            return Perspective.FRONT


class Node:

    def __init__(self, lines, left=None, right=None):
        self.lines = lines
        self.left = left  # front
        self.right = right  # back

    def is_leaf(self):
        return self.left is None and self.right is None


class Perspective(Enum):
    ON = 1
    FRONT = 2
    BACK = 3
