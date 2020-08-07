import matplotlib.pyplot as plt
import numpy as np

from src.world.SPTree import SPTree, Perspective


class Graphics:

    def __init__(self):
        plt.gca().set_prop_cycle(plt.cycler('color', plt.cm.get_cmap('gist_gray')(np.linspace(0, 1))))
        plt.gca().set_aspect('equal', adjustable='box')

    @staticmethod
    def draw(lines, bounding_box):
        bx, by = bounding_box.exterior.xy
        plt.plot(bx, by)
        for line in lines:
            lx, ly = Graphics.get_plottable_line(line)
            plt.plot(lx, ly)
            nx, ny = Graphics.get_normal_plot(line)
            plt.plot(nx, ny)

        plt.show()

    @staticmethod
    def draw_sptree(sptree, bounding_box, camera_location):
        bx, by = bounding_box.exterior.xy
        plt.plot(bx, by)
        Graphics.__draw_sptree_helper(sptree.root, bounding_box, camera_location)
        # Redraw root line
        lx, ly = Graphics.get_plottable_line(sptree.root.lines[0])
        plt.plot(lx, ly, color="MAGENTA")
        cx, cy = camera_location.xy
        plt.plot([cx], [cy], marker='o', markersize=3, color="red")
        plt.show()

    @staticmethod
    def __draw_lines_at_node(node):
        for line in node.lines:
            lx, ly = Graphics.get_plottable_line(line)
            plt.plot(lx, ly)
            nx, ny = Graphics.get_normal_plot(line)
            plt.plot(nx, ny)

    @staticmethod
    def __draw_sptree_helper(cur_node, bounding_box, camera_location):
        if cur_node is None:
            return

        if cur_node.is_leaf():
            Graphics.__draw_lines_at_node(cur_node)

        elif SPTree.classify_perspective(camera_location, cur_node.lines[0], bounding_box) == Perspective.FRONT:
            Graphics.__draw_sptree_helper(cur_node.right, bounding_box, camera_location)
            Graphics.__draw_lines_at_node(cur_node)
            Graphics.__draw_sptree_helper(cur_node.left, bounding_box, camera_location)

        elif SPTree.classify_perspective(camera_location, cur_node.lines[0], bounding_box) == Perspective.BACK:
            Graphics.__draw_sptree_helper(cur_node.left, bounding_box, camera_location)
            Graphics.__draw_lines_at_node(cur_node)
            Graphics.__draw_sptree_helper(cur_node.right, bounding_box, camera_location)

        else:
            Graphics.__draw_sptree_helper(cur_node.left, bounding_box, camera_location)
            Graphics.__draw_sptree_helper(cur_node.right, bounding_box, camera_location)

    @staticmethod
    def get_plottable_line(line):
        start, end = tuple(line.coords)
        return (start[0], end[0]), (start[1], end[1])

    @staticmethod
    def get_normal_plot(vector_line):
        return Graphics.get_plottable_line(vector_line.normal)
