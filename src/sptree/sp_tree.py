import random
from enum import Enum

from shapely.geometry import box, LineString, Point, LinearRing
from shapely.ops import split

from src.vectorline.vector_line import VectorLine

error = 1e-13  # Floating point precision


class SPTree:

    def __init__(self, lines, bounding_box):
        self.root = SPTree.__construct(lines, bounding_box)
        self.bounding_box = bounding_box

    @staticmethod
    def __construct(lines, bounding_box):
        if len(lines) == 0:
            return None

        splitting_line = SPTree.__pick_splitting_line(lines, bounding_box)
        coincident_lines = [splitting_line]
        front = []
        back = []

        splitting_plane = get_splitting_plane(splitting_line, bounding_box)

        for i in range(len(lines)):
            if lines[i] == splitting_line:
                continue
            line = lines[i]
            line_start = Point(line.coords[0])
            line_end = Point(line.coords[1])
            # Coincident line to splitting plane
            if splitting_plane.distance(line_start) < error and splitting_plane.distance(line_end) < error:
                coincident_lines.append(line)
            # Splitting plane crosses line
            elif splitting_plane.crosses(line):
                first_half, second_half = split(line, splitting_plane)
                first_half = VectorLine(first_half.coords, line.normal_dir)
                second_half = VectorLine(second_half.coords, line.normal_dir)
                SPTree.__categorize_line(first_half, splitting_line, front, back)
                SPTree.__categorize_line(second_half, splitting_line, front, back)
            # Line enclosed within one of the planes created by the splitting plane
            else:
                SPTree.__categorize_line(line, splitting_line, front, back)

        front_node = SPTree.__construct(front, bounding_box)
        back_node = SPTree.__construct(back, bounding_box)
        cur_node = Node(coincident_lines, front_node, back_node)

        return cur_node

    @staticmethod
    def __pick_splitting_line(lines, bounding_box):
        """
        Randomly selects a sampling of lines and returns the one that results in the least number of lines split
        from its splitting plane.

        :param lines:
        :param bounding_box:
        :return:
        """
        line_sample = random.sample(lines, 5) if len(lines) >= 5 else lines
        sample_num_pieces = []
        for i in range(len(line_sample)):
            num_pieces = 0
            splitting_plane = get_splitting_plane(line_sample[i], bounding_box)
            for j in range(len(line_sample)):
                if j == i:
                    continue
                line = lines[j]
                line_start = Point(line.coords[0])
                line_end = Point(line.coords[1])
                # Coincident line to splitting plane: no resulting pieces
                if splitting_plane.distance(line_start) < error and splitting_plane.distance(line_end) < error:
                    continue
                # Splitting plane crosses line: cuts line in half
                elif splitting_plane.crosses(line):
                    num_pieces += 2
                # Line enclosed within one of the planes created by the splitting plane: one piece
                else:
                    num_pieces += 1
            sample_num_pieces.append(num_pieces)

        min_index = min((val, index) for (index, val) in enumerate(sample_num_pieces))[1]
        return line_sample[min_index]

    @staticmethod
    def __categorize_line(line, splitting_line, front, behind):
        if is_point_in_front_of_line(splitting_line, line.centroid):
            front.append(line)
        else:
            behind.append(line)


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

    @staticmethod
    def classify(point, splitting_line, bounding_box):
        splitting_plane = get_splitting_plane(splitting_line, bounding_box)
        if splitting_plane.distance(point) < error:
            return Perspective.ON
        if is_point_in_front_of_line(splitting_line, point):
            return Perspective.FRONT
        else:
            return Perspective.BACK


def is_point_in_front_of_line(line, point):
    """
    Determines whether the point is in front or behind the line.

    https://stackoverflow.com/questions/50393718/determine-the-left-and-right-side-of-a-split-shapely-geometry
    :param line:
    :param point:
    :return:
    """
    # If both linear rings result in the same winding order, then the point must be on the same side as the normal and
    # hence in the front of the line
    normal_end_point = Point(line.normal.coords[1])
    normal_on_left = LinearRing([line.coords[0], line.coords[1], normal_end_point]).is_ccw
    line_on_left = LinearRing([line.coords[0], line.coords[1], point]).is_ccw
    return normal_on_left == line_on_left


def get_splitting_plane(line, polygon):
    """
    Extends a line inside a polygon to split the polygon.

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
