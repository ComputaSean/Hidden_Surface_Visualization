import sys
from random import randint
from typing import Tuple

import pygame
from pygame.locals import *
from shapely.geometry import Point

from sptree.sp_tree import SPTree


class Graphics2D:
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

        draw_order = None
        camera_moved = True  # Flag for when the camera has moved
        clear_screen = True  # Flag for when the screen should be wiped
        draw_all_lines = False  # Flag for when all remaining lines should be drawn
        draw_next_line = False  # Flag to drawn the next line to render

        pygame.key.set_repeat(10, 10)  # Required for continuous motion when key is held down

        # Game loop
        while True:

            # Update events
            for event in pygame.event.get():

                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONUP:
                    # Left click - draw next line
                    if event.button == 1:
                        draw_next_line = True
                    # Middle click - draw all remaining lines
                    elif event.button == 2:
                        draw_all_lines = True
                    # Right click - clear_screen screen
                    elif event.button == 3:
                        clear_screen = True

                if event.type == pygame.KEYDOWN:
                    if event.key in Graphics2D.key_to_motion:
                        Graphics2D.key_to_motion[event.key](self)
                        camera_moved = True

            # Render

            # Only need to update render order if the camera moved
            if camera_moved:
                draw_order = self.sptree.painters_alg(self.camera_location)
                camera_moved = False
                clear_screen = True

            if clear_screen:
                self.screen.fill((255, 255, 255))  # Whiteout screen
                pygame.draw.rect(self.screen, (0, 0, 0), self.border, 5)  # Draw bounding box
                pygame.draw.circle(self.screen, (255, 0, 0),
                                   tuple(map(int, self.camera_location.coords[0])), 5)  # Draw camera dot
                draw_order = self.sptree.painters_alg(self.camera_location)
                clear_screen = False

            if draw_next_line:
                # Only draw when there are more lines to be drawn
                node = next(draw_order, None)
                if node is not None:
                    pygame.draw.line(self.screen, Graphics2D._get_random_color(),
                                     node.lines[0].coords[0], node.lines[0].coords[1], 5)
                draw_next_line = False

            if draw_all_lines:
                # Draw remaining lines (if any)
                for node in draw_order:
                    pygame.draw.line(self.screen, Graphics2D._get_random_color(),
                                     node.lines[0].coords[0], node.lines[0].coords[1], 5)
                draw_all_lines = False

            pygame.display.flip()
            self.fpsClock.tick(self.fps)

    def update_camera_location(self, dx: int, dy: int) -> None:
        cx, cy = self.camera_location.coords[0]
        self.camera_location = Point((cx + dx, cy + dy))
        print(self.camera_location)

    @staticmethod
    def _get_random_color() -> Tuple[int, int, int]:
        return randint(0, 255), randint(0, 255), randint(0, 255)
