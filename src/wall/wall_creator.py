from random import randint
from typing import List, Tuple

from shapely.geometry import LineString
from shapely.geometry import box

from wall.wall import Wall

WHITE = (255, 255, 255)
Color = Tuple[int, int, int]


def create_walls(bounding_box: box, num_walls: int, min_height: int, max_height: int) -> List[Wall]:
    """
    Creates a list of non-intersecting walls that fall within a defined bounding box.
    Walls will be of random colors.

    :param bounding_box: boundary containing all created lines
    :param num_walls: number of walls to create
    :param min_height: minimum height of the walls
    :param max_height: maximum height of the walls
    :return: list of non-intersecting walls within bounding_box
    """
    lines = []
    for i in range(num_walls):
        # Continue generating random lines until one doesn't intersect with any existing lines
        while True:
            start_point = _get_rand_point(bounding_box)
            end_point = _get_rand_point(bounding_box)
            if start_point != end_point:
                line = LineString([start_point, end_point])
                if _is_invalid_line(line, lines):
                    continue
                lines.append(line)
                break
    return list(map(lambda x: Wall(x, randint(min_height, max_height), WHITE, WHITE, _get_rand_color()), lines))


def _is_invalid_line(new_line: LineString, lines: List[LineString]) -> bool:
    """
    Checks whether new_line crosses any line in lines.

    :param new_line: line to check
    :param lines: lines to check against
    :return: True if a crossing exists, False otherwise
    """
    for line in lines:
        # Line whose endpoint is on another line is allowed
        if line.crosses(new_line):
            return True
    return False


def _get_rand_point(bounding_box: box) -> Tuple[int, int]:
    """
    Creates a random point contained within bounding_box.

    :param bounding_box: boundary for created point
    :return: random point in bounding_box
    """
    minx, miny, maxx, maxy = bounding_box.bounds
    return randint(minx, maxx), randint(miny, maxy)


def _get_rand_color() -> Color:
    """
    :return: random rgb color
    """
    return randint(0, 255), randint(0, 255), randint(0, 255)
