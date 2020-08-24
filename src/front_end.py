from shapely.geometry import box

from graphics3D.game import Game
from linecreator.line_creator import create_lines
from sptree.sp_tree import SPTree

if __name__ == "__main__":
    width = 768
    height = 768
    b_box = box(0, 0, width, height)  # Bounding box in the first quadrant with above width and height

    num_lines = 5
    lines = create_lines(b_box, num_lines)

    sptree = SPTree(lines, b_box)

    game = Game(sptree)
    game.run()

    # display = PyGameGraphics(sptree)
    # display.run()
