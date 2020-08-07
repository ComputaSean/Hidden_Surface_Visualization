from random import randint

from shapely.geometry import box, Point

from src.world.SPTree import SPTree
from src.world.VectorLine import VectorLine


class World:

    def __init__(self, length, width, num_polygons):
        self.lines = []
        for i in range(num_polygons):
            while True:
                start_point = World.__get_rand_point(length, width)
                end_point = World.__get_rand_point(length, width)
                if start_point != end_point:
                    line = VectorLine([start_point, end_point])
                    if World.__is_valid_line(self.lines, line):
                        continue
                    self.lines.append(line)
                    break

    @staticmethod
    def __is_valid_line(lines, new_line):
        for line in lines:
            # Line whose endpoint is on another line is allowed
            if line.crosses(new_line):
                return True
        return False

    @staticmethod
    def __get_rand_point(max_length, max_width):
        return randint(0, max_length), randint(0, max_width)


def extend_line(line, polygon):
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
        extended_line = VectorLine([(p1.x, miny), (p1.x, maxy)])
    elif p1.y == p2.y:  # horizontal line
        extended_line = VectorLine([(minx, p1.y), (maxx, p1.y)])
    else:
        # linear equation: y = mx + b
        m = (p2.y - p1.y) / (p2.x - p1.x)  # Slope
        b = p1.y - m * p1.x  # y-intercept
        y0 = m * minx + b
        y1 = m * maxx + b
        x0 = (miny - b) / m
        x1 = (maxy - b) / m
        points_on_boundary_lines = [Point(minx, y0), Point(maxx, y1), Point(x0, miny), Point(x1, maxy)]
        points_sorted_by_distance = sorted(points_on_boundary_lines, key=bounding_box.distance)
        extended_line = VectorLine(points_sorted_by_distance[:2])

    return extended_line


if __name__ == "__main__":
    length = 200
    height = 100

    while True:
        a = World(length, height, 100)
        test = SPTree(a.lines, 0, 0, length, height)
        print("Build complete")

    # bounding_box = Polygon([(0, 0), (0, height), (length, height), (length, 0)])

    # xs, ys = bounding_box.exterior.xy
    # plt.plot(xs, ys)
    #
    # for line in a.lines:
    #     lx, ly = line.get_plot()
    #     plt.plot(lx, ly)
    #     nx, ny = line.get_normal_plot()
    #     plt.plot(nx, ny)
    #     extended = extend_line(line, bounding_box)
    #     ex, ey = extended.get_plot()
    #     # plt.plot(ex, ey)
    #
    # # lines = a.get_polygon_points_to_plot()
    # #
    # # for line in lines:
    # #     plt.plot(lines[0], lines[1])
    # #     plt.plot(normals[i][0], normals[i][1])
    #
    # plt.gca().set_aspect('equal', adjustable='box')
    # plt.show()
