from __future__ import annotations

from typing import List, Optional

from sptree.partitionable import Partitionable


class Node:
    """
    Node of an SPTree. Stores the splitting line, corresponding wall, and any children nodes
    that further subdivide the space.
    """

    def __init__(self, lines: List[Partitionable], left: Optional[Node] = None, right: Optional[Node] = None) -> None:
        self.lines = lines  # Contains splitting line and any coincident lines
        self.left = left  # Nodes with lines in front of this node's splitting line
        self.right = right  # Nodes with lines behind this node's splitting line

    def is_leaf(self) -> bool:
        """
        :return: whether this node is a leaf node
        """
        return self.left is None and self.right is None
