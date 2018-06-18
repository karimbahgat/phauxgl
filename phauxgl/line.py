
from .box import Box
from .vertex import Vertex

def NewLine(v1, v2):
    return Line(v1, v2)

def NewLineForPoints(p1, p2):
    v1 = Vertex(Position=p1)
    v2 = Vertex(Position=p2)
    return NewLine(v1, v2)

class Line:
    def __init__(self, v1, v2):
        self.V1 = v1
        self.V2 = v2

    def __repr__(self):
        return 'Line( \n {} \n {} )'.format(self.V1, self.V2)

##    def Picklable(self):
##        return {'v1': self.V1.Picklable(),
##                'v2': self.V2.Picklable()}
##
##    @staticmethod
##    def FromDict(self, pdict):
##        kwargs = {'v1': Vertex(**pdict['v1']),
##                  'v2': Vertex(**pdict['v2']),
##                  }
##        return Line(**kwargs)

    def BoundingBox(l):
        min = l.V1.Position.Min(l.V2.Position)
        max = l.V1.Position.Max(l.V2.Position)
        return Box(min, max)

    def Transform(l, matrix):
        l.V1.Position = matrix.MulPosition(l.V1.Position)
        l.V2.Position = matrix.MulPosition(l.V2.Position)
        l.V1.Normal = matrix.MulDirection(l.V1.Normal)
        l.V2.Normal = matrix.MulDirection(l.V2.Normal)
