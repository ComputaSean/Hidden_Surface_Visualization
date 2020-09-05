from typing import Tuple, List, Union

from numpy import ndarray

color = Tuple[int, int, int]
edge = Tuple[Tuple[int, int], color]
mesh = Tuple[Union[Tuple[int, ...], List[int]], color]

node_pair = Tuple[ndarray, ndarray]
nodes_many = List[ndarray]
