
from __future__ import division

from .vertex import Vertex
from .vector import Vector,VectorW
from .color import Color
from .box import Box

from ctypes import Structure

import array


def NewTriangle(v1, v2, v3):
    t = Triangle(v1, v2, v3)
    t.FixNormals()
    return t

def NewTriangleForPoints(p1, p2, p3):
    v1 = Vertex(Position=p1)
    v2 = Vertex(Position=p2)
    v3 = Vertex(Position=p3)
    return NewTriangle(v1, v2, v3)


class Vertexes:
    def __init__(self):
        self._xyz_lookup = dict()
        
##        self._xs = array.array('f')
##        self._ys = array.array('f')
##        self._zs = array.array('f')

        self._data = array.array('f')

##        self._n1 = array.array('f')
##        self._n2 = array.array('f')
##        self._n3 = array.array('f')
##
##        self._t1 = array.array('f')
##        self._t2 = array.array('f')
##        self._t3 = array.array('f')
##
##        self._c1 = array.array('f')
##        self._c2 = array.array('f')
##        self._c3 = array.array('f')
##        self._c4 = array.array('f')
##
##        self._o1 = array.array('f')
##        self._o2 = array.array('f')
##        self._o3 = array.array('f')
##        self._o4 = array.array('f')

    def __len__(self):
        return len(self._xyz_lookup)
        
    def __iter__(self):
##        for i in range(len(self)):
##            yield self[i]
        step = 9+8
        for di in range(0, len(self), step):
            print di
            p1,p2,p3, n1,n2,n3, t1,t2,t3, c1,c2,c3,c4, o1,o2,o3,o4 = self._data[di:di+step]
            pos = Vector(p1,p2,p3)
            norm = Vector(n1,n2,n3)
            tex = Vector(t1,t2,t3)
            col = Color(c1,c2,c3,c4)
            out = VectorW(o1,o2,o3,o4)
            return Vertex(Position=pos,
                          Normal=norm,
                          Texture=tex,
                          Color=col,
                          Output=out)

    def __getitem__(self, i):
##        pos = Vector(*self._xyz[i]) #self._xs[i],self._ys[i],self._zs[i])
##        norm = Vector(self._n1[i],self._n2[i],self._n3[i])
##        tex = Vector(self._t1[i],self._t2[i],self._t3[i])
##        col = Color(self._c1[i],self._c2[i],self._c3[i],self._c4[i])
##        out = VectorW(self._o1[i],self._o2[i],self._o3[i],self._o4[i])
        step = 9+8
        di = i * step
        p1,p2,p3, n1,n2,n3, t1,t2,t3, c1,c2,c3,c4, o1,o2,o3,o4 = self._data[di:di+step]
        pos = Vector(p1,p2,p3)
        norm = Vector(n1,n2,n3)
        tex = Vector(t1,t2,t3)
        col = Color(c1,c2,c3,c4)
        out = VectorW(o1,o2,o3,o4)
        return Vertex(Position=pos,
                      Normal=norm,
                      Texture=tex,
                      Color=col,
                      Output=out)

    def flat(self):
        return self._data

    def index(self, v):
        pos = (v.Position.X, v.Position.Y, v.Position.Z)
        return self._xyz_lookup.get(pos, -1)

    def append(self, v):
        pos = (v.Position.X, v.Position.Y, v.Position.Z)
        self._xyz_lookup[pos] = len(self._xyz_lookup)
        
##        self._xs.append(v.Position.X)
##        self._ys.append(v.Position.Y)
##        self._zs.append(v.Position.Z)

##        self._n1.append(v.Normal.X)
##        self._n2.append(v.Normal.Y)
##        self._n3.append(v.Normal.Z)
##
##        self._t1.append(v.Texture.X)
##        self._t2.append(v.Texture.Y)
##        self._t3.append(v.Texture.Z)
##
##        self._c1.append(v.Color.R)
##        self._c2.append(v.Color.G)
##        self._c3.append(v.Color.B)
##        self._c4.append(v.Color.A)
##
##        self._o1.append(v.Output.X)
##        self._o2.append(v.Output.Y)
##        self._o3.append(v.Output.Z)
##        self._o4.append(v.Output.W)

        self._data.extend([v.Position.X, v.Position.Y, v.Position.Z,
                           v.Normal.X, v.Normal.Y, v.Normal.Z,
                          v.Texture.X, v.Texture.Y, v.Texture.Z,
                          v.Color.R, v.Color.G, v.Color.B, v.Color.A,
                          v.Output.X, v.Output.Y, v.Output.Z, v.Output.W])

class Triangles:
    def __init__(self):
        self._v1s = array.array('H')
        self._v2s = array.array('H')
        self._v3s = array.array('H')
        self._vertexes = Vertexes()

    def __repr__(self):
        return 'Triangles( \n Triangles: {} \n Vertexes: {} )'.format(len(self), len(self._vertexes))
        
    def __iter__(self):
        for i1,i2,i3 in zip(self._v1s, self._v2s, self._v3s):
            v1 = self._vertexes[i1]
            v2 = self._vertexes[i2]
            v3 = self._vertexes[i3]
            yield Triangle(v1, v2, v3)

    def __len__(self):
        return len(self._v1s)

    def __getitem__(self, i):
        i1,i2,i3 = self._v1s[i], self._v2s[i], self._v3s[i]
        v1 = self._vertexes[i1]
        v2 = self._vertexes[i2]
        v3 = self._vertexes[i3]
        return Triangle(v1, v2, v3)

    def flat_vertexes(self):
        return self._vertexes.flat()
        
    def append(self, tri):
        vindexes = []
        for v in (tri.V1, tri.V2, tri.V3):
            # to avoid duplicate vertexes, but gets very slow
            i = self._vertexes.index(v)
            if i < 0:
                # doesnt yet exist in the index list
                self._vertexes.append(v)
                i = len(self._vertexes) - 1 # 0-based
                
##            self._vertexes.append(v)
##            i = len(self._vertexes) - 1 # 0-based
                
            vindexes.append(i)
        i1,i2,i3 = vindexes
        try:
            self._v1s.append(i1)
            self._v2s.append(i2)
            self._v3s.append(i3)
        except OverflowError:
            self._v1s = array.array('L', self._v1s)
            self._v2s = array.array('L', self._v2s)
            self._v3s = array.array('L', self._v3s)
            self._v1s.append(i1)
            self._v2s.append(i2)
            self._v3s.append(i3)
                
    def extend(self, tris):
        for tri in tris:
            self.append(tri)


class Triangle(Structure):
    _fields_ = [('V1',Vertex),
                ('V2',Vertex),
                ('V3',Vertex)]
##    def __init__(self, v1=None, v2=None, v3=None):
##        self.V1 = v1 or Vertex()
##        self.V2 = v2 or Vertex()
##        self.V3 = v3 or Vertex()

    def __repr__(self):
        return 'Triangle( \n {} \n {} \n {} )'.format(self.V1, self.V2, self.V3)

##    def Picklable(self):
##        return {'v1': self.V1.Picklable(),
##                'v2': self.V2.Picklable(),
##                'v3': self.V3.Picklable()}
##
##    @staticmethod
##    def FromDict(pdict):
##        kwargs = {'v1': Vertex.FromDict(pdict['v1']),
##                  'v2': Vertex.FromDict(pdict['v2']),
##                  'v3': Vertex.FromDict(pdict['v3']),
##                  }
##        return Triangle(**kwargs)

    def IsDegenerate(t):
        p1 = t.V1.Position
        p2 = t.V2.Position
        p3 = t.V3.Position
        if p1 == p2 or p1 == p3 or p2 == p3:
            return True
        if p1.IsDegenerate() or p2.IsDegenerate() or p3.IsDegenerate():
            return True
        return False

    def Normal(t):
        e1 = t.V2.Position.Sub(t.V1.Position)
        e2 = t.V3.Position.Sub(t.V1.Position)
        return e1.Cross(e2).Normalize()

    def Area(t):
        e1 = t.V2.Position.Sub(t.V1.Position)
        e2 = t.V3.Position.Sub(t.V1.Position)
        n = e1.Cross(e2)
        return n.Length() / 2

    def FixNormals(t):
        n = t.Normal()
        zero = Vector()
        if t.V1.Normal == zero:
            t.V1.Normal = n
        if t.V2.Normal == zero:
            t.V2.Normal = n
        if t.V3.Normal == zero:
            t.V3.Normal = n

    def BoundingBox(t):
        min = t.V1.Position.Min(t.V2.Position).Min(t.V3.Position)
        max = t.V1.Position.Max(t.V2.Position).Max(t.V3.Position)
        return Box(min, max)

    def Transform(t, matrix):
        t.V1.Position = matrix.MulPosition(t.V1.Position)
        t.V2.Position = matrix.MulPosition(t.V2.Position)
        t.V3.Position = matrix.MulPosition(t.V3.Position)
        t.V1.Normal = matrix.MulDirection(t.V1.Normal)
        t.V2.Normal = matrix.MulDirection(t.V2.Normal)
        t.V3.Normal = matrix.MulDirection(t.V3.Normal)

    def ReverseWinding(t):
        t.V1, t.V2, t.V3 = t.V3, t.V2, t.V1
        t.V1.Normal = t.V1.Normal.Negate()
        t.V2.Normal = t.V2.Normal.Negate()
        t.V3.Normal = t.V3.Normal.Negate()

    def SetColor(t, c):
        t.V1.Color = c
        t.V2.Color = c
        t.V3.Color = c

##// func (t *Triangle) RandomPoint() Vector {
##//    v1 := t.V1.Position
##//    v2 := t.V2.Position.Sub(v1)
##//    v3 := t.V3.Position.Sub(v1)
##//    for {
##//            a := rand.Float64()
##//            b := rand.Float64()
##//            if a+b <= 1 {
##//                    return v1.Add(v2.MulScalar(a)).Add(v3.MulScalar(b))
##//            }
##//    }
##// }
##
##// func (t *Triangle) Area() float64 {
##//    e1 := t.V2.Position.Sub(t.V1.Position)
##//    e2 := t.V3.Position.Sub(t.V1.Position)
##//    return e1.Cross(e2).Length() / 2
##// }
