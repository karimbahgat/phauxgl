
from __future__ import division

from .vector import Vector, VectorW
from .color import Color
from .color import Color as NewColor

from ctypes import Structure


class Vertex(Structure):
    _fields_ = [('Position',Vector),
                ('Normal',Vector),
                ('Texture',Vector),
                ('Color',NewColor),
                ('Output',VectorW)]
##    def __init__(self,
##                 Position = None, #Vector
##                Normal = None, #Vector
##                Texture = None, #Vector
##                Color = None, #Color
##                Output = None, #VectorW
##                # Vectors  []Vector
##                # Colors   []Color
##                # Floats   []float64
##             ):
##        self.Position = Position or Vector()
##        self.Normal = Normal or Vector()
##        self.Texture = Texture or Vector()
##        self.Color = Color or NewColor() # name conflict
##        self.Output = Output or VectorW()

    def __repr__(self):
        return 'Vertex( {} )'.format(self.Position)

##    def Picklable(self):
##        return {'Position': self.Position.Picklable() if self.Position else None,
##                'Normal': self.Normal.Picklable() if self.Normal else None,
##                'Texture': self.Texture.Picklable() if self.Texture else None,
##                'Color': self.Color.Picklable() if self.Color else None,
##                'Output': self.Output.Picklable() if self.Output else None,
##                }
##
##    @staticmethod
##    def FromDict(pdict):
##        kwargs = {'Position': Vector(**pdict['Position']) if pdict['Position'] else None,
##                    'Normal': Vector(**pdict['Normal']) if pdict['Normal'] else None,
##                    'Texture': Vector(**pdict['Texture']) if pdict['Texture'] else None,
##                    'Color': Color(*pdict['Color']) if pdict['Color'] else None,
##                    'Output': VectorW(**pdict['Output']) if pdict['Output'] else None,
##                    }
##        return Vertex(**kwargs)

    def Outside(a):
        return a.Output.Outside()

def InterpolateVertexes(v1, v2, v3, b):
    v = Vertex()
    v.Position = InterpolateVectors(v1.Position, v2.Position, v3.Position, b)
    v.Normal = InterpolateVectors(v1.Normal, v2.Normal, v3.Normal, b).Normalize()
    v.Texture = InterpolateVectors(v1.Texture, v2.Texture, v3.Texture, b)
    v.Color = InterpolateColors(v1.Color, v2.Color, v3.Color, b)
    v.Output = InterpolateVectorWs(v1.Output, v2.Output, v3.Output, b)
##      // if v1.Vectors != nil {
##      //      v.Vectors = make([]Vector, len(v1.Vectors))
##      //      for i := range v.Vectors {
##      //              v.Vectors[i] = InterpolateVectors(
##      //                      v1.Vectors[i], v2.Vectors[i], v3.Vectors[i], b)
##      //      }
##      // }
##      // if v1.Colors != nil {
##      //      v.Colors = make([]Color, len(v1.Colors))
##      //      for i := range v.Colors {
##      //              v.Colors[i] = InterpolateColors(
##      //                      v1.Colors[i], v2.Colors[i], v3.Colors[i], b)
##      //      }
##      // }
##      // if v1.Floats != nil {
##      //      v.Floats = make([]float64, len(v1.Floats))
##      //      for i := range v.Floats {
##      //              v.Floats[i] = InterpolateFloats(
##      //                      v1.Floats[i], v2.Floats[i], v3.Floats[i], b)
##      //      }
##      // }
    return v

def InterpolateFloats(v1, v2, v3, b):
    n = 0
    n += v1 * b.X
    n += v2 * b.Y
    n += v3 * b.Z
    return n * b.W

def InterpolateColors(v1, v2, v3, b):
    n = Color()
    n = n.Add(v1.MulScalar(b.X))
    n = n.Add(v2.MulScalar(b.Y))
    n = n.Add(v3.MulScalar(b.Z))
    return n.MulScalar(b.W)

def InterpolateVectors(v1, v2, v3, b):
    n = Vector()
    n = n.Add(v1.MulScalar(b.X))
    n = n.Add(v2.MulScalar(b.Y))
    n = n.Add(v3.MulScalar(b.Z))
    return n.MulScalar(b.W)

def InterpolateVectorWs(v1, v2, v3, b):
    n = VectorW()
    n = n.Add(v1.MulScalar(b.X))
    n = n.Add(v2.MulScalar(b.Y))
    n = n.Add(v3.MulScalar(b.Z))
    return n.MulScalar(b.W)

def Barycentric(p1, p2, p3, p):
    v0 = p2.Sub(p1)
    v1 = p3.Sub(p1)
    v2 = p.Sub(p1)
    d00 = v0.Dot(v0)
    d01 = v0.Dot(v1)
    d11 = v1.Dot(v1)
    d20 = v2.Dot(v0)
    d21 = v2.Dot(v1)
    d = d00*d11 - d01*d01
    v = (d11*d20 - d01*d21) / d
    w = (d00*d21 - d01*d20) / d
    u = 1 - v - w
    return VectorW(u, v, w, 1)

