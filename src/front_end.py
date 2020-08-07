from shapely.geometry import box

from graphics.pygame_graphics import PyGameGraphics
from linecreator.line_creator import create_lines
from sptree.sp_tree import SPTree

if __name__ == "__main__":
    width = 768
    height = 768
    b_box = box(0, 0, width, height)  # Bounding box in the first quadrant with above width and height

    num_lines = 10
    lines = create_lines(b_box, num_lines)

    sptree = SPTree(lines, b_box)

    display = PyGameGraphics(sptree)
    display.run()
