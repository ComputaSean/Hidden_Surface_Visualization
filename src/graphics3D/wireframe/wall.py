from graphics3D.wireframe.wireframe import Wireframe


class Wall(Wireframe):

    def __init__(self, nodes, edges, meshes, base, normal):
        super().__init__(nodes, edges, meshes)
        self.base = base
        self.normal = normal
