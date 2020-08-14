import sys
from random import randint

import pygame
from pygame.locals import *
from shapely.geometry import Point

from src.sptree.sp_tree import Perspective


class PyGameGraphics:

    def __init__(self, sptree):
        pygame.init()
        self.fps = 120
        self.fpsClock = pygame.time.Clock()
        minx, miny, maxx, maxy = sptree.bounding_box.bounds  # sptree bounding box will be the screen's dimension
        self.width = maxx
        self.height = maxy
        self.screen = pygame.display.set_mode((int(maxx), int(maxy)))
        self.sptree = sptree
        self.camera_location = Point((maxx // 2, maxy // 2))  # Camera starts centered

    def run(self):

        render_order = []  # Order of lines to be drawn
        r_index = 0  # Index of next line to be drawn in render order
        moved = True  # Flag for when the camera has moved
        clear_screen = True  # Flag for when the screen should be wiped
        draw_all_lines = False  # Flag for when all remaining lines should be drawn
        draw_next_line = False  # Flag to drawn the next line to render

        # Flags indicating whether their respective key is being pressed down
        w_down = False
        s_down = False
        a_down = False
        d_down = False

        pygame.key.set_repeat(10, 10)  # Required for continuous motion when key is held down

        # Game loop
        while True:

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
                    if event.key == K_w:
                        w_down = True
                    if event.key == K_s:
                        s_down = True
                    if event.key == K_a:
                        a_down = True
                    if event.key == K_d:
                        d_down = True

                if event.type == pygame.KEYUP:
                    # Set moved flag only when a movement key is released,
                    # otherwise pressing any key would update the render order
                    # even if no change is required
                    if event.key == K_w:
                        w_down = False
                        moved = True
                    if event.key == K_s:
                        s_down = False
                        moved = True
                    if event.key == K_a:
                        a_down = False
                        moved = True
                    if event.key == K_d:
                        d_down = False
                        moved = True

                # Move camera if there's a movement key pressed
                if w_down or s_down or a_down or d_down:
                    self.__update_camera_location(w_down, s_down, a_down, d_down)
                    clear_screen = True  # Update camera dot on screen

            # Update

            # Only need to update render order if the camera moved
            if moved:
                render_order = PyGameGraphics.__get_render_order(self.sptree, self.camera_location)
                moved = False

            # Render

            if clear_screen:
                self.screen.fill((255, 255, 255))  # Whiteout screen
                pygame.draw.rect(self.screen, (0, 0, 0), Rect(0, 0, self.width, self.height), 5)  # Draw bounding box
                pygame.draw.circle(self.screen, (255, 0, 0),
                                   tuple(map(int, self.camera_location.coords[0])), 5)  # Draw camera dot
                r_index = 0  # Prepare drawing of first line
                clear_screen = False

            if draw_next_line:
                # Only draw when there are more lines to be drawn
                if r_index < len(render_order):
                    line = render_order[r_index]
                    pygame.draw.line(self.screen, PyGameGraphics.__get_random_color(),
                                     line.coords[0], line.coords[1], 5)
                    r_index += 1
                draw_next_line = False

            if draw_all_lines:
                # Draw remaining lines (if any)
                for i in range(r_index, len(render_order)):
                    line = render_order[i]
                    pygame.draw.line(self.screen, PyGameGraphics.__get_random_color(),
                                     line.coords[0], line.coords[1], 5)
                draw_all_lines = False
                r_index = len(render_order)  # No more lines left to draw

            pygame.display.flip()
            self.fpsClock.tick(self.fps)

    @staticmethod
    def __get_render_order(sptree, camera_location):
        return PyGameGraphics.__get_render_order_helper(sptree.root, sptree.bounding_box, camera_location)

    @staticmethod
    def __get_render_order_helper(cur_node, bounding_box, camera_location):
        render_order = []

        if cur_node is None:
            pass

        elif cur_node.is_leaf():
            render_order.extend(PyGameGraphics.__get_lines_at_node(cur_node))

        elif Perspective.classify(camera_location, cur_node.lines[0], bounding_box) == Perspective.FRONT:
            render_order.extend(PyGameGraphics.__get_render_order_helper(cur_node.right, bounding_box, camera_location))
            render_order.extend(PyGameGraphics.__get_lines_at_node(cur_node))
            render_order.extend(PyGameGraphics.__get_render_order_helper(cur_node.left, bounding_box, camera_location))

        elif Perspective.classify(camera_location, cur_node.lines[0], bounding_box) == Perspective.BACK:
            render_order.extend(PyGameGraphics.__get_render_order_helper(cur_node.left, bounding_box, camera_location))
            render_order.extend(PyGameGraphics.__get_lines_at_node(cur_node))
            render_order.extend(PyGameGraphics.__get_render_order_helper(cur_node.right, bounding_box, camera_location))

        else:
            render_order.extend(PyGameGraphics.__get_render_order_helper(cur_node.left, bounding_box, camera_location))
            render_order.extend(PyGameGraphics.__get_render_order_helper(cur_node.right, bounding_box, camera_location))

        return render_order

    @staticmethod
    def __get_lines_at_node(node):
        render_order = []
        for line in node.lines:
            render_order.append(line)
        return render_order

    def __update_camera_location(self, w_down, s_down, a_down, d_down):
        cx, cy = self.camera_location.coords[0]
        if w_down:
            self.camera_location = Point((cx, cy - 1))
        if s_down:
            self.camera_location = Point((cx, cy + 1))
        if a_down:
            self.camera_location = Point((cx - 1, cy))
        if d_down:
            self.camera_location = Point((cx + 1, cy))

    @staticmethod
    def __get_random_color():
        return randint(0, 255), randint(0, 255), randint(0, 255)
