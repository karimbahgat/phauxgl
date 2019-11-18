
from ..vertex import Vertex

def NewFace(v1, v2, v3):
    return Face(v1, v2, v3, false)

class Face:
    def __init__(self, V1, V2, V3, Removed):
        self.V1 = V1
        self.V2 = V2
        self.V3 = V3
	Removed = Removed

    def Degenerate(f):
	v1 = f.V1.Vector
	v2 = f.V2.Vector
	v3 = f.V3.Vector
	return v1 == v2 or v1 == v3 or v2 == v3

    def Normal(f):
	e1 = f.V2.Sub(f.V1.Vector)
	e2 = f.V3.Sub(f.V1.Vector)
	return e1.Cross(e2).Normalize()

