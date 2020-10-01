class object:
    def __init__(self, name, mesh, translation = [0, 0, 0], rotation = [0, 0, 0], scale = [1, 1, 1]):
        self.name = name
        self.mesh = mesh
        self.translation = translation[:]
        self.rotation    = rotation[:]
        self.scale       = scale[:]
    
    def getMesh(self):
        return self.mesh

class tri:
    def __init__(self, p1, p2, p3):
        self.triangle = [p1, p2, p3]
    
    def getCo(self):
        return self.triangle

class mesh:
    def __init__(self, tris):
        self.tris = tris
    
    def getTri(self, i):
        return self.tris[i]
    
    def getTris(self):
        return self.tris[:]

class example:
    def createCube(self):
        return object("Cube", mesh([
            #South
            tri([0, 0, 0], [0, 1, 0], [1, 1, 0]),
            tri([0, 0, 0], [1, 1, 0], [1, 0, 0]),
            #East
            tri([1, 0, 0], [1, 1, 0], [1, 1, 1]),
            tri([1, 0, 0], [1, 1, 1], [1, 0, 1]),
            #North
            tri([1, 0, 1], [1, 1, 1], [0, 1, 1]),
            tri([1, 0, 1], [0, 1, 1], [0, 0, 1]),
            #West
            tri([0, 0, 1], [0, 1, 1], [0, 1, 0]),
            tri([0, 0, 1], [0, 1, 0], [0, 0, 0]),
            #Top
            tri([0, 1, 0], [0, 1, 1], [1, 1, 1]),
            tri([0, 1, 0], [1, 1, 0], [1, 1, 0]),
            #Bottom
            tri([1, 0, 1], [0, 0, 1], [0, 0, 0]),
            tri([1, 0, 1], [0, 0, 0], [1, 0, 0]),
        ]))