from random import randint
from typing import Tuple

import pygame
from pygame.locals import *
from shapely.geometry import Point

from sptree.sp_tree import SPTree

Color = Tuple[int, int, int]


class Graphics2D:
    """
    Visualizes hidden surface determination from a top-down perspective for a dynamic scene.
    The red dot represents the user's camera which can be moved by the keyboard.
    Clicking Mouse1 will draw the walls using painter's algorithm.

    W - moves camera forward
    A - moves camera backward
    S - moves camera left
    D - moves camera right
    Mouse1 - draws a single wall
    Mouse2 - clears the screen of all drawn walls
    Mouse3 - draw all remaining walls
    """
    key_to_motion = {
        pygame.K_w: (lambda x: x.update_camera_location(0, -1)),
        pygame.K_s: (lambda x: x.update_camera_location(0, 1)),
        pygame.K_a: (lambda x: x.update_camera_location(-1, 0)),
        pygame.K_d: (lambda x: x.update_camera_location(1, 0))
    }

    def __init__(self, sptree: SPTree) -> None:
        pygame.init()
        self.fps = 120
        self.fpsClock = pygame.time.Clock()
        minx, miny, maxx, maxy = sptree.bounding_box.bounds  # sptree bounding box will be the screen's dimension
        self.border = Rect(0, 0, maxx, maxy)
        self.screen = pygame.display.set_mode((int(maxx), int(maxy)))
        self.sptree = sptree
        self.camera_location = Point((maxx // 2, maxy // 2))  # Camera starts centered

    def run(self) -> None:
        """
        Starts the game loop of the visualization.
        The game loop contains the logic to update the visualization and to render it.

        :return: None
        """
        pygame.key.set_repeat(10, 10)  # Required for continuous motion when key is held down

        camera_moved = True  # Flag for when the camera has moved
        clear_screen = True  # Flag for when the screen should be wiped
        draw_order = None  # Generator for the next wall to be drawn given the camera's current position
        draw_all_walls = False  # Flag for when all remaining walls should be drawn
        draw_next_wall = False  # Flag to draw the next wall

        # Game loop
        while True:

            # Update events
            for event in pygame.event.get():

                if event.type == QUIT:
                    pygame.quit()
                    return

                if event.type == pygame.MOUSEBUTTONUP:
                    # Mouse1 - draw next wall
                    if event.button == 1:
                        draw_next_wall = True
                    # Mouse2 - draw all remaining walls
                    elif event.button == 2:
                        draw_all_walls = True
                    # Mouse3 - clear screen
                    elif event.button == 3:
                        clear_screen = True

                if event.type == pygame.KEYDOWN:
                    if event.key in Graphics2D.key_to_motion:
                        Graphics2D.key_to_motion[event.key](self)
                        camera_moved = True

            # Draw order needs to be updated when the the camera moved
            if camera_moved:
                draw_order = self.sptree.painters_alg(self.camera_location)
                camera_moved = False
                clear_screen = True

            # Render

            if clear_screen:
                self.screen.fill((255, 255, 255))  # Whiteout screen
                pygame.draw.rect(self.screen, (0, 0, 0), self.border, 5)  # Draw bounding box
                pygame.draw.circle(self.screen, (255, 0, 0),
                                   tuple(map(int, self.camera_location.coords[0])), 5)  # Draw camera dot
                draw_order = self.sptree.painters_alg(self.camera_location)  # Reset generator
                clear_screen = False

            if draw_next_wall:
                # Only draw when there are more walls to be drawn
                coincident_walls = next(draw_order, [])
                for wall in coincident_walls:
                    wall_base = wall.get_base()
                    pygame.draw.line(self.screen, Graphics2D._get_random_color(),
                                     wall_base.coords[0], wall_base.coords[1], 5)
                draw_next_wall = False

            if draw_all_walls:
                # Draw remaining walls (if any)
                for coincident_walls in draw_order:
                    for wall in coincident_walls:
                        wall_base = wall.get_base()
                        pygame.draw.line(self.screen, Graphics2D._get_random_color(),
                                         wall_base.coords[0], wall_base.coords[1], 5)
                draw_all_walls = False

            pygame.display.flip()
            self.fpsClock.tick(self.fps)

    def update_camera_location(self, dx: int, dy: int) -> None:
        """
        Moves the camera's position by (dx, dy).

        :param dx: distance to move along the x-axis
        :param dy: distance to move along the y-axis
        :return: None
        """
        cx, cy = self.camera_location.coords[0]
        self.camera_location = Point((cx + dx, cy + dy))

    @staticmethod
    def _get_random_color() -> Color:
        """
        :return: a random rgb color
        """
        return randint(0, 255), randint(0, 255), randint(0, 255)
