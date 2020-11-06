from __future__ import annotations

from typing import Tuple

from shapely.geometry import LineString


class Partitionable:
    """
    A 3D wall/2D line that is able to be split into two pieces given some partitioning line.
    Every Partitionable can be expressed looking from a top down perspective as some flat line.
    """

    def split(self, part: Partitionable) -> Tuple[Partitionable, Partitionable]:
        """
        Split this Partitionable using part.

        :param part: splitting line
        :return: split partitionable object
        """
        raise NotImplementedError

    def get_base(self) -> LineString:
        """
        :return: the line representing this Partitionable as seen from a top-down perspective
        """
        raise NotImplementedError
