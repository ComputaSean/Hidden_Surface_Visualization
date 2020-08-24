import math
import sys
from random import randint

import numpy as np
import pygame
from pygame.locals import *
from shapely.geometry import Point

from graphics3D.camera.groundcamera import GroundCamera
from graphics3D.wireframe.wall_builder import WallBuilder
from graphics3D.wireframe.wireframe_builder import WireframeBuilder
from sptree.sp_tree import Perspective


class Game:
    key_to_motion = {
        pygame.K_w: (lambda x: x.camera.dolly_forward()),
        pygame.K_s: (lambda x: x.camera.dolly_backward()),
        pygame.K_a: (lambda x: x.camera.truck_left()),
        pygame.K_d: (lambda x: x.camera.truck_right()),
        pygame.K_q: (lambda x: x.camera.pedestal_down()),
        pygame.K_e: (lambda x: x.camera.pedestal_up()),
        pygame.K_HOME: (lambda x: x.camera.tilt_up()),
        pygame.K_END: (lambda x: x.camera.tilt_down()),
        pygame.K_DELETE: (lambda x: x.camera.pan_left()),
        pygame.K_PAGEDOWN: (lambda x: x.camera.pan_right()),
        pygame.K_PAGEUP: (lambda x: x.camera.roll_left()),
        pygame.K_c: (lambda x: x.camera.roll_left()),
        pygame.K_INSERT: (lambda x: x.camera.roll_right()),
        pygame.K_z: (lambda x: x.camera.roll_right())
    }

    def __init__(self, sptree):
        pygame.init()
        self.sptree = sptree
        self.fps = 144
        self.fpsClock = pygame.time.Clock()
        self.screen_width = 1024
        self.screen_height = 1024
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.camera = GroundCamera()
        self.wireframes = []

    def run(self):

        node_radius = 3
        line_radius = 5
        node_color = (255, 255, 255)

        pygame.key.set_repeat(10, 10)  # Required for continuous motion when key is held down

        pygame.mouse.set_pos((self.screen_width // 2, self.screen_height // 2))
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)

        camera_moved = True

        # Game loop.
        while True:

            for event in pygame.event.get():
                # Update Events
                if event.type == QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                    pygame.quit()
                    sys.exit()

                # User moves their mouse
                if event.type == pygame.MOUSEMOTION:
                    rx, ry = pygame.mouse.get_rel()
                    if rx != 0 or ry != 0:
                        self.camera.mouse_pan(rx)
                        self.camera.mouse_tilt(ry)
                        camera_moved = True

                # User presses a keyboard button
                if event.type == pygame.KEYDOWN:
                    if event.key in Game.key_to_motion:
                        Game.key_to_motion[event.key](self)
                        camera_moved = True

            # Draw once when the camera is physically moved, and only once
            if camera_moved:

                self.screen.fill((0, 0, 0))

                camera_location_3d = self.camera.coords.change_to_global_basis(np.array([0, 0, 0, 1]))
                camera_location_2d = Point(camera_location_3d[0], camera_location_3d[2])

                render_order = self._get_render_order(self.sptree, camera_location_2d)

                for wf in render_order:

                    for n1, n2, edge_color in wf.get_global_edges():
                        pr_line_start = self.get_camera_visible_projection(n1)
                        pr_line_end = self.get_camera_visible_projection(n2)
                        if pr_line_start is not None and pr_line_end is not None:
                            pygame.draw.line(self.screen, edge_color, pr_line_start, pr_line_end, line_radius)

                    for node in wf.get_global_nodes():
                        pr_pt = self.get_camera_visible_projection(node)
                        if pr_pt is not None:
                            pygame.draw.circle(self.screen, node_color, pr_pt, node_radius)

                    for mesh in wf.get_global_meshes():
                        mesh_nodes = []
                        for node in mesh[0]:
                            pr_pt = self.get_camera_visible_projection(node)
                            if pr_pt is not None:
                                mesh_nodes.append(pr_pt)
                        if len(mesh_nodes) > 2:
                            pygame.draw.polygon(self.screen, mesh[1], mesh_nodes)

                camera_moved = False

            pygame.display.flip()
            self.fpsClock.tick(self.fps)

    def get_camera_visible_projection(self, node):
        # Camera space point
        cs_pt = self.camera.coords.change_to_local_basis(node)

        if cs_pt[2] < 0 and abs(cs_pt[2]) > self.camera.focal_length:
            # Screen space - Perspective division onto near plane
            ss_x = self.camera.focal_length * cs_pt[0] / -cs_pt[2]
            ss_y = self.camera.focal_length * cs_pt[1] / -cs_pt[2]

            # if abs(ss_x) <= self.camera.canvas_width / 2 or abs(ss_y) <= self.camera.canvas_height / 2:
            # NDC Space
            ndc_x = (ss_x + self.camera.canvas_width / 2) / self.camera.canvas_width
            ndc_y = (ss_y + self.camera.canvas_height / 2) / self.camera.canvas_height
            # Raster space
            rs_x = math.floor(ndc_x * self.screen_width)
            rs_y = math.floor((1 - ndc_y) * self.screen_height)

            return rs_x, rs_y

        return None

    @staticmethod
    def _get_render_order(sptree, camera_location):
        render_order = []
        Game._get_render_order_helper(sptree.root, sptree.bounding_box, camera_location, render_order)
        return render_order

    @staticmethod
    def _get_render_order_helper(cur_node, bounding_box, camera_location, render_order):
        if cur_node is None:
            return

        elif cur_node.is_leaf():
            Game._get_walls_at_node(cur_node, render_order)

        elif Perspective.classify(camera_location, cur_node.lines[0], bounding_box) == Perspective.FRONT:
            Game._get_render_order_helper(cur_node.right, bounding_box, camera_location, render_order)
            Game._get_walls_at_node(cur_node, render_order)
            Game._get_render_order_helper(cur_node.left, bounding_box, camera_location, render_order)

        elif Perspective.classify(camera_location, cur_node.lines[0], bounding_box) == Perspective.BACK:
            Game._get_render_order_helper(cur_node.left, bounding_box, camera_location, render_order)
            Game._get_walls_at_node(cur_node, render_order)
            Game._get_render_order_helper(cur_node.right, bounding_box, camera_location, render_order)

        else:
            Game._get_render_order_helper(cur_node.left, bounding_box, camera_location, render_order)
            Game._get_render_order_helper(cur_node.right, bounding_box, camera_location, render_order)

    @staticmethod
    def _get_walls_at_node(node, render_order):
        for line in node.lines:
            render_order.append(WallBuilder(line, 50, (255, 255, 255), (0, 255, 0)).build())


def get_rand_color():
    return randint(0, 255), randint(0, 255), randint(0, 255)


if __name__ == "__main__":
    white_edge = (255, 255, 255)
    red_edge = (255, 0, 0)
    green_edge = (0, 255, 0)
    blue_edge = (0, 0, 255)

    # surface_color = (255, 255, 0)

    axis_builder = WireframeBuilder()
    axis_builder.add_node(0, 0, 0)
    axis_builder.add_node(40, 0, 0)
    axis_builder.add_node(0, 40, 0)
    axis_builder.add_node(0, 0, 40)
    axis_builder.add_edges(((0, 1, red_edge), (0, 2, green_edge), (0, 3, blue_edge)))
    axis = axis_builder.build()

    cube_builder = WireframeBuilder()
    cube_builder.add_nodes([(x, y, z) for x in (50, 200) for y in (-50, 100) for z in (50, 200)])
    cube_builder.add_mesh(((0, 4, 6, 2), get_rand_color()))
    cube_builder.add_edges([(n, n + 4, white_edge) for n in range(0, 4)])
    cube_builder.add_edges([(n, n + 1, white_edge) for n in range(0, 8, 2)])
    cube_builder.add_edges([(n, n + 2, white_edge) for n in (0, 1, 4, 5)])
    cube = cube_builder.build()
