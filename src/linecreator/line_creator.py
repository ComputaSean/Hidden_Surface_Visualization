from random import randint

from shapely.geometry import LineString


def create_lines(bounding_box, num_lines):
    lines = []
    for i in range(num_lines):
        while True:
            start_point = _get_rand_point(bounding_box)
            end_point = _get_rand_point(bounding_box)
            if start_point != end_point:
                line = LineString([start_point, end_point])
                if _is_valid_line(lines, line):
                    continue
                lines.append(line)
                break
    return lines


def _is_valid_line(lines, new_line):
    for line in lines:
        # Line whose endpoint is on another line is allowed
        if line.crosses(new_line):
            return True
    return False


def _get_rand_point(bounding_box):
    minx, miny, maxx, maxy = bounding_box.bounds
    return randint(minx, maxx), randint(miny, maxy)
