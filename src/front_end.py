from shapely.geometry import box

from graphics.pygame_graphics import PyGameGraphics
from graphics3D.game import Game
from linecreator.line_creator import create_lines
from sptree.sp_tree import SPTree
from vectorline.vector_line import VectorLine

if __name__ == "__main__":
    width = 768
    height = 768
    b_box = box(0, 0, width, height)  # Bounding box in the first quadrant with above width and height

    num_lines = 5
    lines = create_lines(b_box, num_lines)

    # line_coords = [((618.0, 705.0), (526.0, 528.0)), ((382.0, 192.0), (589.0, 367.0)), ((232.0, 408.0), (204.0, 569.0)),
    #                ((365.0, 543.0), (279.0, 235.0)), ((536.0, 472.0), (464.0, 273.0))]
    # lines = [VectorLine(coords) for coords in line_coords]

    sptree = SPTree(lines, b_box)

    game = Game(sptree)
    game.run()

    # display = PyGameGraphics(sptree)
    # display.run()
