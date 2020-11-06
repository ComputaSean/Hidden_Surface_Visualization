from __future__ import annotations

import random
from enum import Enum
from typing import List, Optional, Generator

from shapely.geometry import box, LineString, Point, LinearRing, Polygon

from sptree.line_wrapper import LineWrapper
from sptree.node import Node
from sptree.partitionable import Partitionable

error = 1e-13  # Floating point precision


class SPTree:
    """
    A SPTree is a binary tree that partitions space at each level in a 2D plane along a single line.
    The left child contains all lines in front of the splitting line, while the right child contains all lines
    behind the splitting line.
    """

    def __init__(self, lines: List[Partitionable], bounding_box: box) -> None:
        self.root = SPTree._construct(lines, bounding_box)
        self.bounding_box = bounding_box

    @staticmethod
    def _construct(lines: List[Partitionable], bounding_box: box) -> Optional[Node]:
        """
        Create a SPTree from the given lines by subdividing the space in half using planes.

        :param lines: input lines
        :param bounding_box: bounding box for lines
        :return: root node of the created SPTree
        """
        if len(lines) == 0:
            return None

        # Pick a splitting line that results in relatively few required splits
        splitting_line = SPTree._pick_splitting_line(lines, bounding_box)
        coincident_lines = [splitting_line]  # All lines coincident to the splitting line
        front = []  # All lines in front of the splitting line
        back = []  # All lines behind the splitting line

        # Extend splitting line to intersect with the bounding box
        splitting_plane = _get_splitting_plane(splitting_line, bounding_box)
        splitting_base = splitting_plane.get_base()

        # Classify all lines as being behind or in front of the splitting line
        # Lines that are intersected by the splitting plane will be split in half, with halves individually classified
        for i in range(len(lines)):
            # Splitting line already accounted for
            if lines[i] == splitting_line:
                continue
            line = lines[i]
            base = line.get_base()
            line_start = Point(base.coords[0])
            line_end = Point(base.coords[1])
            # Coincident line to splitting plane
            # Distance is checked rather than using contains() because of floating point issues
            if splitting_base.distance(line_start) < error and splitting_base.distance(line_end) < error:
                coincident_lines.append(line)
            # Splitting plane crosses line
            # Split line in half and classify both halves accordingly
            elif splitting_base.crosses(line.get_base()):
                first_half, second_half = line.split(splitting_plane)
                SPTree._categorize_line(first_half, splitting_line, front, back)
                SPTree._categorize_line(second_half, splitting_line, front, back)
            # Line entirely enclosed within one side of the splitting plane
            else:
                SPTree._categorize_line(line, splitting_line, front, back)

        # Recursively subdivide space in front of and behind the splitting line
        front_node = SPTree._construct(front, bounding_box)
        back_node = SPTree._construct(back, bounding_box)
        cur_node = Node(coincident_lines, front_node, back_node)

        return cur_node

    @staticmethod
    def _pick_splitting_line(lines: List[Partitionable], bounding_box: box) -> Partitionable:
        """
        Randomly selects a sampling of lines and returns the one resulting in the least number of lines split
        from its splitting plane.

        :param lines: lines to choose from
        :param bounding_box: bounding box for lines
        :return: sampled line requiring the least number of splits from other lines
        """
        line_sample = random.sample(lines, 5) if len(lines) >= 5 else lines
        sample_num_pieces = []  # Stores the number of split pieces for each sampled line
        # Calculate the number of split pieces for each sampled line
        for i in range(len(line_sample)):
            num_pieces = 0
            splitting_plane = _get_splitting_plane(line_sample[i], bounding_box)
            splitting_base = splitting_plane.get_base()
            for j in range(len(line_sample)):
                # Skip the splitting line because it won't create any pieces with itself
                if j == i:
                    continue
                line = lines[j].get_base()
                line_start = Point(line.coords[0])
                line_end = Point(line.coords[1])
                # Coincident line to splitting plane: no resulting pieces
                if splitting_base.distance(line_start) < error and splitting_base.distance(line_end) < error:
                    continue
                # Splitting plane crosses line: cuts line in half resulting in two disjoint pieces
                elif splitting_base.crosses(line):
                    num_pieces += 2
                # Line enclosed within one side of the splitting plane: one piece
                else:
                    num_pieces += 1
            sample_num_pieces.append(num_pieces)  # Record number of split pieces for this sample line

        min_pieces_index = min((val, index) for (index, val) in enumerate(sample_num_pieces))[1]
        return line_sample[min_pieces_index]

    @staticmethod
    def _categorize_line(line: Partitionable, splitting_line: Partitionable,
                         front: List[Partitionable], behind: List[Partitionable]) -> None:
        """
        Adds line to front or behind depending on its position relative to splitting_line.

        Precondition: line is not split by the splitting plane containing splitting_line

        :param line: line being categorized
        :param splitting_line: chosen line to split the space
        :param front: lines in front of the splitting line
        :param behind: lines behind the splitting line
        :return: None
        """
        if _is_point_in_front_of_line(line.get_base().centroid, splitting_line):
            front.append(line)
        else:
            behind.append(line)

    def painters_alg(self, point: Point) -> Generator[List[Partitionable], None, None]:
        """
        Applies painter's algorithm to the SPTree.
        The SPTree is recursively travelled via the generator, starting from nodes in the background and working
        towards nodes in the foreground.

        :param point: camera location
        :return: generator for Painter's Algorithm
        """
        return SPTree._painters_alg(self.root, point, self.bounding_box)

    @staticmethod
    def _painters_alg(cur_node: Node, point: Point, bounding_box: box) -> Generator[List[Partitionable], None, None]:
        if cur_node is None:
            return

        # Last node to draw
        elif cur_node.is_leaf():
            yield cur_node.lines

        # Point is in front of cur_node, so paint nodes further away i.e. right subtree first, then this node,
        # and finally points in front of this node i.e. left subtree
        elif Perspective.classify(point, cur_node.lines[0], bounding_box) == Perspective.FRONT:
            if cur_node.right is not None:
                yield from SPTree._painters_alg(cur_node.right, point, bounding_box)
            yield cur_node.lines
            if cur_node.left is not None:
                yield from SPTree._painters_alg(cur_node.left, point, bounding_box)

        # Point is in behind cur_node, so paint nodes further away i.e. left subtree first, then this node,
        # and finally points behind this node i.e. right subtree
        elif Perspective.classify(point, cur_node.lines[0], bounding_box) == Perspective.BACK:
            if cur_node.left is not None:
                yield from SPTree._painters_alg(cur_node.left, point, bounding_box)
            yield cur_node.lines
            if cur_node.right is not None:
                yield from SPTree._painters_alg(cur_node.right, point, bounding_box)

        # Point is coincident to cur_node, so it isn't drawn
        else:
            if cur_node.left is not None:
                yield from SPTree._painters_alg(cur_node.left, point, bounding_box)
            if cur_node.right is not None:
                yield from SPTree._painters_alg(cur_node.right, point, bounding_box)


class Perspective(Enum):
    """
    Describes possible positions of a point relative to a line.
    """
    ON = 1
    FRONT = 2
    BACK = 3

    @staticmethod
    def classify(point: Point, line: Partitionable, bounding_box: box) -> Perspective:
        """
        Classifies the position of point relative to line.

        :param point: point being classified
        :param line: line being used as the point of reference
        :param bounding_box: bounding box containing this line
        :return: ON if point is on the line, FRONT if point is in front of the line, or BACK if point is behind the line
        """
        if _get_splitting_plane(line, bounding_box).get_base().distance(point) < error:
            return Perspective.ON
        if _is_point_in_front_of_line(point, line):
            return Perspective.FRONT
        else:
            return Perspective.BACK


def _is_point_in_front_of_line(point: Point, line: Partitionable) -> bool:
    """
    Determines whether the point is in front or behind the line.
    Winding order for line start, line end, and normal is clockwise.
    Hence a point that is in front will have the same winding order.

    :param point: point being considered for winding order
    :param line: line being used as the point of reference
    :return: True if it's in front, False otherwise
    """
    return not LinearRing([*line.get_base().coords, point]).is_ccw


def _get_splitting_plane(line: Partitionable, polygon: Polygon) -> LineWrapper:
    """
    Extends a line inside a polygon to split said polygon.

    Credit to https://stackoverflow.com/a/62413539
    :param line: line being extended
    :param polygon: polygon being split
    :return: plane that splits the polygon's bounding box
    """
    minx, miny, maxx, maxy = polygon.bounds

    bounding_box = box(minx, miny, maxx, maxy)
    p1, p2 = line.get_base().boundary
    if p1.x == p2.x:  # vertical line
        extended_line = LineString([(p1.x, miny), (p1.x, maxy)])
    elif p1.y == p2.y:  # horizontal line
        extended_line = LineString([(minx, p1.y), (maxx, p1.y)])
    else:
        # Calculate all 4 possible points of intersection

        # Linear equation: y = mx + b
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

        # Use the closest two points to the bounding box to form the splitting plane

        points_sorted_by_distance = sorted(unique_points_on_boundary_lines, key=bounding_box.distance)
        extended_line = LineString(points_sorted_by_distance[:2])

    return LineWrapper(extended_line)
