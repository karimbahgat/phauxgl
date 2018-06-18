
from __future__ import division

import math

from .vector import Vector, VectorW


def Identity():
    return Matrix(
            1, 0, 0, 0,
            0, 1, 0, 0,
            0, 0, 1, 0,
            0, 0, 0, 1)

def Translate(v):
    return Matrix(
            1, 0, 0, v.X,
            0, 1, 0, v.Y,
            0, 0, 1, v.Z,
            0, 0, 0, 1)

def Scale(v):
    return Matrix(
            v.X, 0, 0, 0,
            0, v.Y, 0, 0,
            0, 0, v.Z, 0,
            0, 0, 0, 1)

def Rotate(v, a):
    v = v.Normalize()
    s = math.sin(a)
    c = math.cos(a)
    m = 1 - c
    return Matrix(
            m*v.X*v.X + c, m*v.X*v.Y + v.Z*s, m*v.Z*v.X - v.Y*s, 0,
            m*v.X*v.Y - v.Z*s, m*v.Y*v.Y + c, m*v.Y*v.Z + v.X*s, 0,
            m*v.Z*v.X + v.Y*s, m*v.Y*v.Z - v.X*s, m*v.Z*v.Z + c, 0,
            0, 0, 0, 1)

def RotateTo(a, b):
    dot = b.Dot(a)
    if dot == 1:
        return Identity()
    elif dot == -1:
        return Rotate(a.Perpendicular(), math.pi)
    else:
        angle = math.acos(dot)
        v = b.Cross(a).Normalize()
        return Rotate(v, angle)

def Orient(position, size, up, rotation):
    m = Rotate(Vector(0, 0, 1), rotation)
    m = m.Scale(size)
    m = m.RotateTo(Vector(0, 0, 1), up)
    m = m.Translate(position)
    return m

def Frustum(l, r, b, t, n, f):
    t1 = 2 * n
    t2 = r - l
    t3 = t - b
    t4 = f - n
    return Matrix(
                t1 / t2, 0, (r + l) / t2, 0,
                0, t1 / t3, (t + b) / t3, 0,
                0, 0, (-f - n) / t4, (-t1 * f) / t4,
                0, 0, -1, 0)

def Orthographic(l, r, b, t, n, f):
    return Matrix(
            2 / (r - l), 0, 0, -(r + l) / (r - l),
            0, 2 / (t - b), 0, -(t + b) / (t - b),
            0, 0, -2 / (f - n), -(f + n) / (f - n),
            0, 0, 0, 1)

def Perspective(fovy, aspect, near, far):
    ymax = near * math.tan(fovy*math.pi/360)
    xmax = ymax * aspect
    return Frustum(-xmax, xmax, -ymax, ymax, near, far)

def LookAt(eye, center, up):
    z = eye.Sub(center).Normalize()
    x = up.Cross(z).Normalize()
    y = z.Cross(x)
    return Matrix(
            x.X, x.Y, x.Z, -x.Dot(eye),
            y.X, y.Y, y.Z, -y.Dot(eye),
            z.X, z.Y, z.Z, -z.Dot(eye),
            0, 0, 0, 1)

def LookAtDirection(forward, up):
    z = forward.Normalize()
    x = up.Cross(z).Normalize()
    y = z.Cross(x)
    return Matrix(
            x.X, x.Y, x.Z, 0,
            y.X, y.Y, y.Z, 0,
            z.X, z.Y, z.Z, 0,
            0, 0, 0, 1)

def Screen(w, h):
        w2 = float(w) / 2
        h2 = float(h) / 2
        return Matrix(
                w2, 0, 0, w2,
                0, -h2, 0, h2,
                0, 0, 0.5, 0.5,
                0, 0, 0, 1)

def Viewport(x, y, w, h):
    l = x
    b = y
    r = x + w
    t = y + h
    return Matrix(
            (r - l) / 2, 0, 0, (r + l) / 2,
            0, (t - b) / 2, 0, (t + b) / 2,
            0, 0, 0.5, 0.5,
            0, 0, 0, 1)

class Matrix:
    def __init__(self,
                 X00=None, X01=None, X02=None, X03=None,
                 X10=None, X11=None, X12=None, X13=None,
                 X20=None, X21=None, X22=None, X23=None,
                 X30=None, X31=None, X32=None, X33=None,
                 ):
        self.X00, self.X01, self.X02, self.X03 = X00, X01, X02, X03
        self.X10, self.X11, self.X12, self.X13 = X10, X11, X12, X13
        self.X20, self.X21, self.X22, self.X23 = X20, X21, X22, X23
        self.X30, self.X31, self.X32, self.X33 = X30, X31, X32, X33

    def Translate(m, v):
        return Translate(v).Mul(m)

    def Scale(m, v):
        return Scale(v).Mul(m)

    def Rotate(v, a):
        return Rotate(v, a).Mul(m)

    def RotateTo(m, a, b):
        return RotateTo(a, b).Mul(m)

    def Frustum(m, l, r, b, t, n, f):
        return Frustum(l, r, b, t, n, f).Mul(m)

    def Orthographic(m, l, r, b, t, n, f):
        return Orthographic(l, r, b, t, n, f).Mul(m)

    def Perspective(m, fovy, aspect, near, far):
        return Perspective(fovy, aspect, near, far).Mul(m)

    def LookAt(m, eye, center, up):
        return LookAt(eye, center, up).Mul(m)

    def Viewport(m, x, y, w, h):
        return Viewport(x, y, w, h).Mul(m)

    def MulScalar(a, b):
        return Matrix(
                a.X00 * b, a.X01 * b, a.X02 * b, a.X03 * b,
                a.X10 * b, a.X11 * b, a.X12 * b, a.X13 * b,
                a.X20 * b, a.X21 * b, a.X22 * b, a.X23 * b,
                a.X30 * b, a.X31 * b, a.X32 * b, a.X33 * b,
        )

    def Mul(a, b):
        m = Matrix()
        m.X00 = a.X00*b.X00 + a.X01*b.X10 + a.X02*b.X20 + a.X03*b.X30
        m.X10 = a.X10*b.X00 + a.X11*b.X10 + a.X12*b.X20 + a.X13*b.X30
        m.X20 = a.X20*b.X00 + a.X21*b.X10 + a.X22*b.X20 + a.X23*b.X30
        m.X30 = a.X30*b.X00 + a.X31*b.X10 + a.X32*b.X20 + a.X33*b.X30
        m.X01 = a.X00*b.X01 + a.X01*b.X11 + a.X02*b.X21 + a.X03*b.X31
        m.X11 = a.X10*b.X01 + a.X11*b.X11 + a.X12*b.X21 + a.X13*b.X31
        m.X21 = a.X20*b.X01 + a.X21*b.X11 + a.X22*b.X21 + a.X23*b.X31
        m.X31 = a.X30*b.X01 + a.X31*b.X11 + a.X32*b.X21 + a.X33*b.X31
        m.X02 = a.X00*b.X02 + a.X01*b.X12 + a.X02*b.X22 + a.X03*b.X32
        m.X12 = a.X10*b.X02 + a.X11*b.X12 + a.X12*b.X22 + a.X13*b.X32
        m.X22 = a.X20*b.X02 + a.X21*b.X12 + a.X22*b.X22 + a.X23*b.X32
        m.X32 = a.X30*b.X02 + a.X31*b.X12 + a.X32*b.X22 + a.X33*b.X32
        m.X03 = a.X00*b.X03 + a.X01*b.X13 + a.X02*b.X23 + a.X03*b.X33
        m.X13 = a.X10*b.X03 + a.X11*b.X13 + a.X12*b.X23 + a.X13*b.X33
        m.X23 = a.X20*b.X03 + a.X21*b.X13 + a.X22*b.X23 + a.X23*b.X33
        m.X33 = a.X30*b.X03 + a.X31*b.X13 + a.X32*b.X23 + a.X33*b.X33
        return m

    def MulPosition(a, b):
        x = a.X00*b.X + a.X01*b.Y + a.X02*b.Z + a.X03
        y = a.X10*b.X + a.X11*b.Y + a.X12*b.Z + a.X13
        z = a.X20*b.X + a.X21*b.Y + a.X22*b.Z + a.X23
        return Vector(x, y, z)

    def MulPositionW(a, b):
        x = a.X00*b.X + a.X01*b.Y + a.X02*b.Z + a.X03
        y = a.X10*b.X + a.X11*b.Y + a.X12*b.Z + a.X13
        z = a.X20*b.X + a.X21*b.Y + a.X22*b.Z + a.X23
        w = a.X30*b.X + a.X31*b.Y + a.X32*b.Z + a.X33
        return VectorW(x, y, z, w)

    def MulDirection(a, b):
        x = a.X00*b.X + a.X01*b.Y + a.X02*b.Z
        y = a.X10*b.X + a.X11*b.Y + a.X12*b.Z
        z = a.X20*b.X + a.X21*b.Y + a.X22*b.Z
        return Vector(x, y, z).Normalize()

    def MulBox(a, box):
        # http://dev.theomader.com/transform-bounding-boxes/
        r = Vector(a.X00, a.X10, a.X20)
        u = Vector(a.X01, a.X11, a.X21)
        b = Vector(a.X02, a.X12, a.X22)
        t = Vector(a.X03, a.X13, a.X23)
        xa = r.MulScalar(box.Min.X)
        xb = r.MulScalar(box.Max.X)
        ya = u.MulScalar(box.Min.Y)
        yb = u.MulScalar(box.Max.Y)
        za = b.MulScalar(box.Min.Z)
        zb = b.MulScalar(box.Max.Z)
        xa, xb = xa.Min(xb), xa.Max(xb)
        ya, yb = ya.Min(yb), ya.Max(yb)
        za, zb = za.Min(zb), za.Max(zb)
        min = xa.Add(ya).Add(za).Add(t)
        max = xb.Add(yb).Add(zb).Add(t)
        return Box(min, max)

    def Transpose(a):
        return Matrix(
                a.X00, a.X10, a.X20, a.X30,
                a.X01, a.X11, a.X21, a.X31,
                a.X02, a.X12, a.X22, a.X32,
                a.X03, a.X13, a.X23, a.X33)

    def Determinant(a):
        return (a.X00*a.X11*a.X22*a.X33 - a.X00*a.X11*a.X23*a.X32 + \
                a.X00*a.X12*a.X23*a.X31 - a.X00*a.X12*a.X21*a.X33 + \
                a.X00*a.X13*a.X21*a.X32 - a.X00*a.X13*a.X22*a.X31 - \
                a.X01*a.X12*a.X23*a.X30 + a.X01*a.X12*a.X20*a.X33 - \
                a.X01*a.X13*a.X20*a.X32 + a.X01*a.X13*a.X22*a.X30 - \
                a.X01*a.X10*a.X22*a.X33 + a.X01*a.X10*a.X23*a.X32 + \
                a.X02*a.X13*a.X20*a.X31 - a.X02*a.X13*a.X21*a.X30 + \
                a.X02*a.X10*a.X21*a.X33 - a.X02*a.X10*a.X23*a.X31 + \
                a.X02*a.X11*a.X23*a.X30 - a.X02*a.X11*a.X20*a.X33 - \
                a.X03*a.X10*a.X21*a.X32 + a.X03*a.X10*a.X22*a.X31 - \
                a.X03*a.X11*a.X22*a.X30 + a.X03*a.X11*a.X20*a.X32 - \
                a.X03*a.X12*a.X20*a.X31 + a.X03*a.X12*a.X21*a.X30)

    def Inverse(a):
        m = Matrix()
        d = a.Determinant()
        m.X00 = (a.X12*a.X23*a.X31 - a.X13*a.X22*a.X31 + a.X13*a.X21*a.X32 - a.X11*a.X23*a.X32 - a.X12*a.X21*a.X33 + a.X11*a.X22*a.X33) / d
        m.X01 = (a.X03*a.X22*a.X31 - a.X02*a.X23*a.X31 - a.X03*a.X21*a.X32 + a.X01*a.X23*a.X32 + a.X02*a.X21*a.X33 - a.X01*a.X22*a.X33) / d
        m.X02 = (a.X02*a.X13*a.X31 - a.X03*a.X12*a.X31 + a.X03*a.X11*a.X32 - a.X01*a.X13*a.X32 - a.X02*a.X11*a.X33 + a.X01*a.X12*a.X33) / d
        m.X03 = (a.X03*a.X12*a.X21 - a.X02*a.X13*a.X21 - a.X03*a.X11*a.X22 + a.X01*a.X13*a.X22 + a.X02*a.X11*a.X23 - a.X01*a.X12*a.X23) / d
        m.X10 = (a.X13*a.X22*a.X30 - a.X12*a.X23*a.X30 - a.X13*a.X20*a.X32 + a.X10*a.X23*a.X32 + a.X12*a.X20*a.X33 - a.X10*a.X22*a.X33) / d
        m.X11 = (a.X02*a.X23*a.X30 - a.X03*a.X22*a.X30 + a.X03*a.X20*a.X32 - a.X00*a.X23*a.X32 - a.X02*a.X20*a.X33 + a.X00*a.X22*a.X33) / d
        m.X12 = (a.X03*a.X12*a.X30 - a.X02*a.X13*a.X30 - a.X03*a.X10*a.X32 + a.X00*a.X13*a.X32 + a.X02*a.X10*a.X33 - a.X00*a.X12*a.X33) / d
        m.X13 = (a.X02*a.X13*a.X20 - a.X03*a.X12*a.X20 + a.X03*a.X10*a.X22 - a.X00*a.X13*a.X22 - a.X02*a.X10*a.X23 + a.X00*a.X12*a.X23) / d
        m.X20 = (a.X11*a.X23*a.X30 - a.X13*a.X21*a.X30 + a.X13*a.X20*a.X31 - a.X10*a.X23*a.X31 - a.X11*a.X20*a.X33 + a.X10*a.X21*a.X33) / d
        m.X21 = (a.X03*a.X21*a.X30 - a.X01*a.X23*a.X30 - a.X03*a.X20*a.X31 + a.X00*a.X23*a.X31 + a.X01*a.X20*a.X33 - a.X00*a.X21*a.X33) / d
        m.X22 = (a.X01*a.X13*a.X30 - a.X03*a.X11*a.X30 + a.X03*a.X10*a.X31 - a.X00*a.X13*a.X31 - a.X01*a.X10*a.X33 + a.X00*a.X11*a.X33) / d
        m.X23 = (a.X03*a.X11*a.X20 - a.X01*a.X13*a.X20 - a.X03*a.X10*a.X21 + a.X00*a.X13*a.X21 + a.X01*a.X10*a.X23 - a.X00*a.X11*a.X23) / d
        m.X30 = (a.X12*a.X21*a.X30 - a.X11*a.X22*a.X30 - a.X12*a.X20*a.X31 + a.X10*a.X22*a.X31 + a.X11*a.X20*a.X32 - a.X10*a.X21*a.X32) / d
        m.X31 = (a.X01*a.X22*a.X30 - a.X02*a.X21*a.X30 + a.X02*a.X20*a.X31 - a.X00*a.X22*a.X31 - a.X01*a.X20*a.X32 + a.X00*a.X21*a.X32) / d
        m.X32 = (a.X02*a.X11*a.X30 - a.X01*a.X12*a.X30 - a.X02*a.X10*a.X31 + a.X00*a.X12*a.X31 + a.X01*a.X10*a.X32 - a.X00*a.X11*a.X32) / d
        m.X33 = (a.X01*a.X12*a.X20 - a.X02*a.X11*a.X20 + a.X02*a.X10*a.X21 - a.X00*a.X12*a.X21 - a.X01*a.X10*a.X22 + a.X00*a.X11*a.X22) / d
        return m


