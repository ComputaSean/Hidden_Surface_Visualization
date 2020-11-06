from shapely.geometry import box

from graphics2D.graphics_2d import Graphics2D
from graphics3D.graphics_3d import Graphics3D
from sptree.sp_tree import SPTree
from wall.wall_creator import create_walls

if __name__ == "__main__":
    width = 768
    height = 768
    b_box = box(0, 0, width, height)  # Bounding box in the first quadrant with above width and height

    num_walls = 10
    lines = create_walls(b_box, num_walls, 20, 40)

    sptree = SPTree(lines, b_box)

    game = Graphics3D(sptree)
    game.run()

    display = Graphics2D(sptree)
    display.run()
