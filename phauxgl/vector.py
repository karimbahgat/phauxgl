
from __future__ import division

import math
import random



def V(x, y, z):
    return Vector(x, y, z)

def RandomUnitVector():
    while True:
        x = random.random()*2 - 1
        y = random.random()*2 - 1
        z = random.random()*2 - 1
        if x*x+y*y+z*z > 1:
            continue
        return Vector(x, y, z).Normalize()

class Vector:
    def __init__(self, x=0, y=0, z=0):
        self.X = x
        self.Y = y
        self.Z = z

    def __repr__(self):
        return 'Vector( {} {} {} )'.format(self.X, self.Y, self.Z)

##    def Picklable(self):
##        return {'x': self.X,
##                'y': self.Y,
##                'z': self.Z}

    def VectorW(a): 
        return VectorW(a.X, a.Y, a.Z, 1)

    def IsDegenerate(a):
        nan = math.isnan(a.X) or math.isnan(a.Y) or math.isnan(a.Z)
        inf = math.isinf(a.X) or math.isinf(a.Y) or math.isinf(a.Z)
        return nan or inf

    def Length(a):
        return math.sqrt(a.X*a.X + a.Y*a.Y + a.Z*a.Z)

    def Less(a, b):
        if a.X != b.X:
            return a.X < b.X
        if a.Y != b.Y:
            return a.Y < b.Y
        return a.Z < b.Z

    def Distance(a, b):
        return a.Sub(b).Length()

    def LengthSquared(a):
        return a.X*a.X + a.Y*a.Y + a.Z*a.Z

    def DistanceSquared(a, b):
        return a.Sub(b).LengthSquared()

    def Lerp(a, b, t):
        return a.Add(b.Sub(a).MulScalar(t))

    def LerpDistance(a, b, d):
        return a.Add(b.Sub(a).Normalize().MulScalar(d))

    def Dot(a, b):
        return a.X*b.X + a.Y*b.Y + a.Z*b.Z

    def Cross(a, b):
        x = a.Y*b.Z - a.Z*b.Y
        y = a.Z*b.X - a.X*b.Z
        z = a.X*b.Y - a.Y*b.X
        return Vector(x, y, z)

    def Normalize(a):
        try:
            #r = (a.X*a.X+a.Y*a.Y+a.Z*a.Z)**-0.5 # approximate fast inverse square root
            r = 1 / math.sqrt(a.X*a.X+a.Y*a.Y+a.Z*a.Z)
        except ZeroDivisionError:
            return a
        return Vector(a.X * r, a.Y * r, a.Z * r)

    def Negate(a):
        return Vector(-a.X, -a.Y, -a.Z)

    def Abs(a):
        return Vector(abs(a.X), abs(a.Y), abs(a.Z))

    def Add(a, b):
        return Vector(a.X + b.X, a.Y + b.Y, a.Z + b.Z)

    def Sub(a, b):
        return Vector(a.X - b.X, a.Y - b.Y, a.Z - b.Z)

    def Mul(a, b):
        return Vector(a.X * b.X, a.Y * b.Y, a.Z * b.Z)

    def Div(a, b):
        try:
            return Vector(a.X / b.X, a.Y / b.Y, a.Z / b.Z)
        except ZeroDivisionError:
            x,y,z = b.X, b.Y, b.Z
            x = a.X / x if x else a.X
            y = a.Y / y if y else a.Y
            z = a.Z / z if z else a.Z
            return Vector(x, y, z)

    def Mod(a, b):
        #// as implemented in GLSL
        x = a.X - b.X*math.floor(a.X/b.X)
        y = a.Y - b.Y*math.floor(a.Y/b.Y)
        z = a.Z - b.Z*math.floor(a.Z/b.Z)
        return Vector(x, y, z)

    def AddScalar(a, b):
        return Vector(a.X + b, a.Y + b, a.Z + b)

    def SubScalar(a, b):
        return Vector(a.X - b, a.Y - b, a.Z - b)

    def MulScalar(a, b):
        return Vector(a.X * b, a.Y * b, a.Z * b)

    def DivScalar(a, b):
        try:
            return Vector(a.X / b, a.Y / b, a.Z / b)
        except ZeroDivisionError:
            return a

    def Min(a, b):
        return Vector(min(a.X, b.X), min(a.Y, b.Y), min(a.Z, b.Z))

    def Max(a, b):
        return Vector(max(a.X, b.X), max(a.Y, b.Y), max(a.Z, b.Z))

    def Floor(a):
        return Vector(math.floor(a.X), math.floor(a.Y), math.floor(a.Z))

    def Ceil(a):
        return Vector(math.ceil(a.X), math.ceil(a.Y), math.ceil(a.Z))

    def Round(a):
        return a.RoundPlaces(0)

    def RoundPlaces(a, n):
        x = RoundPlaces(a.X, n)
        y = RoundPlaces(a.Y, n)
        z = RoundPlaces(a.Z, n)
        return Vector(x, y, z)

    def MinComponent(a):
        return min(min(a.X, a.Y), a.Z)

    def MaxComponent(a):
        return max(max(a.X, a.Y), a.Z)

    def Reflect(i, n):
        return i.Sub(n.MulScalar(2 * n.Dot(i)))

    def Perpendicular(a):
        if a.X == 0 and a.Y == 0:
            if a.Z == 0:
                return Vector()
            return Vector(0, 1, 0)
        return Vector(-a.Y, a.X, 0).Normalize()

    def SegmentDistance(p, v, w):
        l2 = v.DistanceSquared(w)
        if l2 == 0:
            return p.Distance(v)
        t = p.Sub(v).Dot(w.Sub(v)) / l2
        if t < 0:
            return p.Distance(v)
        if t > 1:
            return p.Distance(w)
        return v.Add(w.Sub(v).MulScalar(t)).Distance(p)


class VectorW:
    def __init__(self, x=0, y=0, z=0, w=0):
        self.X = x
        self.Y = y
        self.Z = z
        self.W = w

##    def Picklable(self):
##        return {'x': self.X,
##                'y': self.Y,
##                'z': self.Z,
##                'w': self.W}

    def Vector(a):
        return Vector(a.X, a.Y, a.Z)

    def Outside(a):
        x, y, z, w = a.X, a.Y, a.Z, a.W
        return x < -w or x > w or y < -w or y > w or z < -w or z > w

    def Dot(a, b):
        return a.X*b.X + a.Y*b.Y + a.Z*b.Z + a.W*b.W

    def Add(a, b):
        return VectorW(a.X + b.X, a.Y + b.Y, a.Z + b.Z, a.W + b.W)

    def Sub(a, b):
        return VectorW(a.X - b.X, a.Y - b.Y, a.Z - b.Z, a.W - b.W)

    def MulScalar(a, b):
        return VectorW(a.X * b, a.Y * b, a.Z * b, a.W * b)

    def DivScalar(a, b):
        try:
            return VectorW(a.X / b, a.Y / b, a.Z / b, a.W / b)
        except ZeroDivisionError:
            return a

