
from __future__ import division

import math


def BoxForBoxes(boxes):
    if len(boxes) == 0:
        return EmptyBox
    x0 = boxes[0].Min.X
    y0 = boxes[0].Min.Y
    z0 = boxes[0].Min.Z
    x1 = boxes[0].Max.X
    y1 = boxes[0].Max.Y
    z1 = boxes[0].Max.Z
    for _, box in enumerate(boxes):
        x0 = min(x0, box.Min.X)
        y0 = min(y0, box.Min.Y)
        z0 = min(z0, box.Min.Z)
        x1 = max(x1, box.Max.X)
        y1 = max(y1, box.Max.Y)
        z1 = max(z1, box.Max.Z)
    return Box(Vector(x0, y0, z0), Vector(x1, y1, z1))



class Box:
    def __init__(self, min=None, max=None):
        self.Min = min
        self.Max = max

    def __repr__(self):
        return 'Box( {} \n {} )'.format(self.Min, self.Max)

    def Volume(a):
        s = a.Size()
        return s.X * s.Y * s.Z

    def Anchor(a, anchor):
        return a.Min.Add(a.Size().Mul(anchor))

    def Center(a):
        return a.Anchor(Vector(0.5, 0.5, 0.5))

    def Size(a):
        return a.Max.Sub(a.Min)

    def Extend(a, b):
        if a == EmptyBox:
            return b
        return Box(a.Min.Min(b.Min), a.Max.Max(b.Max))

    def Offset(a, x):
        return Box(a.Min.SubScalar(x), a.Max.AddScalar(x))

    def Translate(a, v):
        return Box(a.Min.Add(v), a.Max.Add(v))

    def Contains(a, b):
        return a.Min.X <= b.X and a.Max.X >= b.X and \
                a.Min.Y <= b.Y and a.Max.Y >= b.Y and \
                a.Min.Z <= b.Z and a.Max.Z >= b.Z

    def ContainsBox(a, b):
        return a.Min.X <= b.Min.X and a.Max.X >= b.Max.X and \
                a.Min.Y <= b.Min.Y and a.Max.Y >= b.Max.Y and \
                a.Min.Z <= b.Min.Z and a.Max.Z >= b.Max.Z

    def Intersects(a, b):
        return not (a.Min.X > b.Max.X or a.Max.X < b.Min.X or a.Min.Y > b.Max.Y or \
                a.Max.Y < b.Min.Y or a.Min.Z > b.Max.Z or a.Max.Z < b.Min.Z)

    def Intersection(a, b):
        if not a.Intersects(b):
            return EmptyBox
        min = a.Min.Max(b.Min)
        max = a.Max.Min(b.Max)
        min, max = min.Min(max), min.Max(max)
        return Box(min, max)

    def Transform(a, m):
        return m.MulBox(a)


EmptyBox = Box()



