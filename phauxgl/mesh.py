
from __future__ import division

import math

from .triangle import Triangle
from .vector import Vector
from .box import Box, EmptyBox
from .matrix import Identity, Translate


def NewEmptyMesh():
    return Mesh()

def NewMesh(triangles, lines):
    return Mesh(triangles, lines, None)

def NewTriangleMesh(triangles):
    return Mesh(triangles, None, None)

def NewLineMesh(lines):
    return Mesh(None, lines, None)

def smoothNormalsThreshold(normal, normals, threshold):
    result = Vector()
    for x in normals:
        if x.Dot(normal) >= threshold:
            result = result.Add(x)
    return result.Normalize()


class Mesh:
    def __init__(self, triangles=None, lines=None, box=None):
        self.Triangles = triangles or []
        self.Lines = lines or []
        self.box = box

    def __repr__(self):
        return 'Mesh \n Triangles: {} \n Lines: {} \n Box: {}'.format(len(self.Triangles), len(self.Lines), self.box)

    def dirty(m):
        m.box = None

    def Copy(m):
        return NewMesh(list(triangles), list(lines))

    def Add(a, b):
        a.Triangles.extend(b.Triangles)
        a.Lines.extend(b.Lines)
        a.dirty()

    def SetColor(m, c):
        for t in m.Triangles:
            t.SetColor(c)

    def Volume(m):
        v = 0
        for t in m.Triangles:
            p1 = t.V1.Position
            p2 = t.V2.Position
            p3 = t.V3.Position
            v += p1.X*(p2.Y*p3.Z-p3.Y*p2.Z) - p2.X*(p1.Y*p3.Z-p3.Y*p1.Z) + p3.X*(p1.Y*p2.Z-p2.Y*p1.Z)
        return abs(v / 6)

    def SurfaceArea(m):
        a = 0
        for t in m.Triangles:
            a += t.Area()
        return a

    def SmoothNormalsThreshold(m, radians):
        threshold = math.cos(radians)
        lookup = dict()
        for t in m.Triangles:
            for v in [t.V1, t.V2, t.V3]:
                if v.Position in lookup:
                    lookup[v.Position].append(v.Normal)
                else:
                    lookup[v.Position] = [v.Normal]
        for t in m.Triangles:
            t.V1.Normal = smoothNormalsThreshold(t.V1.Normal, lookup[t.V1.Position], threshold)
            t.V2.Normal = smoothNormalsThreshold(t.V2.Normal, lookup[t.V2.Position], threshold)
            t.V3.Normal = smoothNormalsThreshold(t.V3.Normal, lookup[t.V3.Position], threshold)

    def SmoothNormals(m):
        lookup = dict()
        for t in m.Triangles:
            for v in [t.V1, t.V2, t.V3]:
                if v.Position in lookup:
                    lookup[v.Position] = lookup[v.Position].Add(v.Normal)
                else:
                    lookup[v.Position] = v.Normal

        for k,v in lookup.items():
            lookup[k] = v.Normalize()
            
        for t in m.Triangles:
            t.V1.Normal = lookup[t.V1.Position]
            t.V2.Normal = lookup[t.V2.Position]
            t.V3.Normal = lookup[t.V3.Position]

    def UnitCube(m):
        r = 0.5
        return m.FitInside(Box(Vector(-r, -r, -r), Vector(r, r, r)), Vector(0.5, 0.5, 0.5))

    def BiUnitCube(m):
        r = 1
        return m.FitInside(Box(Vector(-r, -r, -r), Vector(r, r, r)), Vector(0.5, 0.5, 0.5))

    def MoveTo(m, position, anchor):
        matrix = Translate(position.Sub(m.BoundingBox().Anchor(anchor)))
        m.Transform(matrix)
        return matrix

    def Center(m):
        return m.MoveTo(Vector(), Vector(0.5, 0.5, 0.5))

    def FitInside(m, box, anchor):
        scale = box.Size().Div(m.BoundingBox().Size()).MinComponent()
        extra = box.Size().Sub(m.BoundingBox().Size().MulScalar(scale))
        matrix = Identity()
        matrix = matrix.Translate(m.BoundingBox().Min.Negate())
        matrix = matrix.Scale(Vector(scale, scale, scale))
        matrix = matrix.Translate(box.Min.Add(extra.Mul(anchor)))
        m.Transform(matrix)
        return matrix

    def BoundingBox(m):
        if m.box == None:
            box = EmptyBox
            for t in m.Triangles:
                box = box.Extend(t.BoundingBox())
            for l in m.Lines:
                box = box.Extend(l.BoundingBox())
            m.box = box
        return m.box

    def Transform(m, matrix):
        for t in m.Triangles:
            t.Transform(matrix)
        for t in m.Lines:
            l.Transform(matrix)
        m.dirty()

    def ReverseWinding(m):
        for t in m.Triangles:
            t.ReverseWinding()

##func (m *Mesh) Simplify(factor float64) {
##      st := make([]*simplify.Triangle, len(m.Triangles))
##      for i, t := range m.Triangles {
##              v1 := simplify.Vector(t.V1.Position)
##              v2 := simplify.Vector(t.V2.Position)
##              v3 := simplify.Vector(t.V3.Position)
##              st[i] = simplify.NewTriangle(v1, v2, v3)
##      }
##      sm := simplify.NewMesh(st)
##      sm = sm.Simplify(factor)
##      m.Triangles = make([]*Triangle, len(sm.Triangles))
##      for i, t := range sm.Triangles {
##              v1 := Vector(t.V1)
##              v2 := Vector(t.V2)
##              v3 := Vector(t.V3)
##              m.Triangles[i] = NewTriangleForPoints(v1, v2, v3)
##      }
##      m.dirty()
##}
##
##func (m *Mesh) SaveSTL(path string) error {
##      return SaveSTL(path, m)
##}
