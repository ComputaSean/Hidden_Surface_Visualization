from random import randint

from shapely.geometry import box

from src.world.PyGameGraphics import PyGameGraphics
from src.world.SPTree import SPTree
from src.world.VectorLine import VectorLine


class World:

    def __init__(self, bounding_box, num_lines):
        self.lines = []
        for i in range(num_lines):
            while True:
                start_point = World.__get_rand_point(bounding_box)
                end_point = World.__get_rand_point(bounding_box)
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
    def __get_rand_point(bounding_box):
        minx, miny, maxx, maxy = bounding_box.bounds
        return randint(minx, maxx), randint(miny, maxy)


if __name__ == "__main__":
    width = 768
    height = 768

    b_box = box(0, 0, width, height)
    world = World(b_box, 10)
    sptree = SPTree(world.lines, b_box)

    display = PyGameGraphics(sptree)
    display.run()
