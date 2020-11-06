from typing import Tuple

from shapely.geometry import LineString
from shapely.ops import split

from sptree.partitionable import Partitionable


class LineWrapper(Partitionable):
    """
    Wrapper class for a LineString to implement the Partitionable interface.
    """

    def __init__(self, line: LineString):
        self._line = line

    def split(self, splitting_part: Partitionable) -> Tuple[Partitionable, Partitionable]:
        first_half, second_half = split(self._line, splitting_part.get_base())
        return LineWrapper(LineString(first_half.coords)), LineWrapper(LineString(second_half.coords))

    def get_base(self) -> LineString:
        return self._line
