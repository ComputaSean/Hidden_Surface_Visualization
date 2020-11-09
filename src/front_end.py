import sys

from shapely.geometry import box

from graphics2D.graphics_2d import Graphics2D
from graphics3D.graphics_3d import Graphics3D
from sptree.sp_tree import SPTree
from wall.wall_creator import create_walls

if __name__ == "__main__":
    """
    Arguments:
        bb_width - width of bounding box for all walls
        bb_height - height of bounding box for all walls
        num_walls - number of walls to add to the scene
        min_wall_height - minimum height of a wall
        max_wall_height - maximum height of a wall
        graphics_type - '3D' for 3D graphics and '2D' for top down view (no quotes)
    """
    arg_list = sys.argv
    if len(arg_list) != 7:
        print("Usage: \"python3 front_end.py bb_width bb_height num_walls min_wall_height max_wall_height graphics_type")
        exit(1)

    width = int(arg_list[1])
    height = int(arg_list[2])
    num_walls = int(arg_list[3])
    min_wall_height = int(arg_list[4])
    max_wall_height = int(arg_list[5])

    b_box = box(0, 0, width, height)  # Bounding box in the first quadrant with above width and height

    lines = create_walls(b_box, num_walls, min_wall_height, max_wall_height)

    sptree = SPTree(lines, b_box)

    graphics_type = arg_list[6]

    if graphics_type == '2D':
        display = Graphics2D(sptree)
        display.run()
    elif graphics_type == '3D':
        game = Graphics3D(sptree)
        game.run()
    else:
        print("Unrecognized graphics type. Use '2D' or '3D' for parameter graphics_type.")
        exit(1)
