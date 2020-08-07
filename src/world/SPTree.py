from random import shuffle

from shapely.geometry import box, LineString, Point
from shapely.ops import split

from src.world.VectorLine import VectorLine


class SPTree:

    def __init__(self, lines, minx, miny, maxx, maxy):
        shuffle(lines)
        bounding_box = box(minx, miny, maxx, maxy)
        self.root = SPTree.construct(lines, bounding_box)

    @staticmethod
    def construct(lines, bounding_box):
        if len(lines) == 0:
            return None

        error = 1e-13

        chosen_line = lines[0]
        coincident_lines = [chosen_line]
        front = []
        behind = []

        splitting_line = SPTree.get_splitting_line(chosen_line, bounding_box)
        for i in range(1, len(lines)):
            cur_line = lines[i]
            start = Point(cur_line.coords[0])
            end = Point(cur_line.coords[1])
            # Coincident Line
            if splitting_line.distance(start) < error and splitting_line.distance(end) < error:
                coincident_lines.append(cur_line)
            # Intersected Line
            elif splitting_line.crosses(cur_line):
                first_half, second_half = split(cur_line, splitting_line)
                first_half = VectorLine(tuple(first_half.coords))
                second_half = VectorLine(tuple(second_half.coords))
                SPTree.classify_line(first_half, front, behind)
                SPTree.classify_line(second_half, front, behind)
            # Line enclosed within one of the created planes
            else:
                SPTree.classify_line(cur_line, front, behind)

        front_node = SPTree.construct(front, bounding_box)
        behind_node = SPTree.construct(behind, bounding_box)
        cur_node = Node(coincident_lines, front_node, behind_node)
        return cur_node

    @staticmethod
    def get_splitting_line(line, polygon):
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
            points_sorted_by_distance = sorted(points_on_boundary_lines, key=bounding_box.distance)
            extended_line = LineString(points_sorted_by_distance[:2])

        # assert (extended_line.distance(Point(line.coords[0])) < 1e-13)
        # assert (extended_line.distance(Point(line.coords[1])) < 1e-13)

        return extended_line

    @staticmethod
    def cut_line_at_points(line, points):
        # First coords of line
        coords = list(line.coords)

        # Keep list coords where to cut (cuts = 1)
        cuts = [0] * len(coords)
        cuts[0] = 1
        cuts[-1] = 1

        # Add the coords from the points
        coords += [list(p.coords)[0] for p in points]
        cuts += [1] * len(points)

        # Calculate the distance along the line for each point
        dists = [line.project(Point(p)) for p in coords]

        # sort the coords/cuts based on the distances
        # see http://stackoverflow.com/questions/6618515/sorting-list-based-on-values-from-another-list
        coords = [p for (d, p) in sorted(zip(dists, coords))]
        cuts = [p for (d, p) in sorted(zip(dists, cuts))]

        # generate the Lines
        # lines = [LineString([coords[i], coords[i+1]]) for i in range(len(coords)-1)]
        lines = []

        for i in range(len(coords) - 1):
            if cuts[i] == 1:
                # find next element in cuts == 1 starting from index i + 1
                j = cuts.index(1, i + 1)
                lines.append(LineString(coords[i:j + 1]))

        return lines

    @staticmethod
    def classify_line(line, front, behind):
        nx, ny = line.get_normal_plot()
        end = Point([(nx[1], ny[1])])
        start = line.centroid
        connecting_line = LineString([start, end])
        # If crossed, then behind
        if connecting_line.crosses(line):  # Intersects?
            behind.append(line)
        # Else then in front
        else:
            front.append(line)


class Node:

    def __init__(self, lines, left=None, right=None):
        self.line = lines
        self.left = left
        self.right = right


if __name__ == "__main__":
    my_lines = [VectorLine([(1, 2), (3, 4)])]
    SPTree(my_lines, 0, 0, 100, 100)
