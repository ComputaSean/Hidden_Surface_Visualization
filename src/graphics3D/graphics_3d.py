import math
import sys
from typing import Generator, List

import numpy as np
import pygame
from pygame.locals import *
from shapely.geometry import Point

from graphics3D.camera.groundcamera import GroundCamera
from sptree.partitionable import Partitionable
from sptree.sp_tree import SPTree


class Graphics3D:
    """
    Visualizes hidden surface determination from a 3D perspective for a dynamic scene.

    W - moves camera forward
    A - moves camera backward
    S - moves camera left
    D - moves camera right
    Q - moves camera down
    E - moves camera up
    """
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
        self.screen_width = 1920
        self.screen_height = 1080
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)
        self.camera = GroundCamera()
        self.wireframes = []

    def run(self):
        """
        Starts the game loop of the visualization.
        The game loop contains the logic to update the visualization and to render it.

        :return: None
        """
        pygame.mouse.set_pos((self.screen_width // 2, self.screen_height // 2))
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)

        pygame.key.set_repeat(10, 10)  # Required for continuous motion when key is held down

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
                    if event.key in Graphics3D.key_to_motion:
                        Graphics3D.key_to_motion[event.key](self)
                        camera_moved = True

            # Draw once when the camera is physically moved, and only once
            if camera_moved:
                self.screen.fill((0, 0, 0))
                self._draw_walls()
                camera_moved = False

            pygame.display.flip()
            self.fpsClock.tick(self.fps)

    @staticmethod
    def _update_draw_order(camera: GroundCamera, sptree: SPTree) -> Generator[List[Partitionable], None, None]:
        """
        Returns a generator which encodes the order sptree nodes should be drawn given the camera's current location.

        :param camera: camera in the scene
        :param sptree: precomputed SPTree of the scene
        :return: generator encoding order of sptree nodes to be drawn
        """
        camera_location_3d = camera.coords.change_to_global_basis(np.array([0, 0, 0, 1]))
        camera_location_2d = Point(camera_location_3d[0], camera_location_3d[2])
        return sptree.painters_alg(camera_location_2d)

    def _draw_walls(self) -> None:
        """
        Draws the walls of the scene using an SPTree and painter's algorithm.

        :return: None
        """
        draw_order = Graphics3D._update_draw_order(self.camera, self.sptree)
        node_radius = 3
        line_radius = 5
        for coincident_walls in draw_order:
            for wall in coincident_walls:

                for edge in wall.get_edges():
                    pr_line_start = self._get_camera_visible_projection(edge[0])
                    pr_line_end = self._get_camera_visible_projection(edge[1])
                    if pr_line_start is not None and pr_line_end is not None:
                        pygame.draw.line(self.screen, wall.edge_color, pr_line_start, pr_line_end, line_radius)

                for node in wall.nodes:
                    pr_pt = self._get_camera_visible_projection(node)
                    if pr_pt is not None:
                        pygame.draw.circle(self.screen, wall.wall_color, pr_pt, node_radius)

                mesh_nodes = []
                for node in wall.get_nodes():
                    pr_pt = self._get_camera_visible_projection(node)
                    if pr_pt is not None:
                        mesh_nodes.append(pr_pt)

                if len(mesh_nodes) >= 3:
                    pygame.draw.polygon(self.screen, wall.wall_color, mesh_nodes)

    def _get_camera_visible_projection(self, world_point):
        # Camera space point
        cs_pt = self.camera.coords.change_to_local_basis(world_point)

        # Check if point is within viewing frustum
        if cs_pt[2] < 0 and abs(cs_pt[2]) > self.camera.focal_length:
            # Screen space - Perspective division onto near image plane
            ss_x = self.camera.focal_length * cs_pt[0] / -cs_pt[2]
            ss_y = self.camera.focal_length * cs_pt[1] / -cs_pt[2]

            if abs(ss_x) <= self.camera.canvas_width / 2 or abs(ss_y) <= self.camera.canvas_height / 2:
                # NDC Space - coordinates are in [0, 1]
                ndc_x = (ss_x + self.camera.canvas_width / 2) / self.camera.canvas_width
                ndc_y = (ss_y + self.camera.canvas_height / 2) / self.camera.canvas_height
                # Raster space
                rs_x = math.floor(ndc_x * self.screen_width)
                rs_y = math.floor((1 - ndc_y) * self.screen_height)

                return rs_x, rs_y

        return None
