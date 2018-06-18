
from __future__ import division

import math

from .util import Clamp

def MakeColor(c):
    if len(c) != 4:
        raise Exception('Color input must be RGBA tuple')
    r, g, b, a = c
    d = 256
    return Color(float(r) / d, float(g) / d, float(b) / d, float(a) / d)

##func HexColor(x string) Color {
##      x = strings.Trim(x, "#")
##      var r, g, b, a int
##      a = 255
##      switch len(x) {
##      case 3:
##              fmt.Sscanf(x, "%1x%1x%1x", &r, &g, &b)
##              r = (r << 4) | r
##              g = (g << 4) | g
##              b = (b << 4) | b
##      case 4:
##              fmt.Sscanf(x, "%1x%1x%1x%1x", &r, &g, &b, &a)
##              r = (r << 4) | r
##              g = (g << 4) | g
##              b = (b << 4) | b
##              a = (a << 4) | a
##      case 6:
##              fmt.Sscanf(x, "%02x%02x%02x", &r, &g, &b)
##      case 8:
##              fmt.Sscanf(x, "%02x%02x%02x%02x", &r, &g, &b, &a)
##      }
##      const d = 0xff
##      return Color{float64(r) / d, float64(g) / d, float64(b) / d, float64(a) / d}
##}


class Color:
    def __init__(self, r=0, g=0, b=0, a=0):
        self.R = r
        self.G = g
        self.B = b
        self.A = a

    def __repr__(self):
        return 'Color ({} {} {} {})'.format(self.R, self.G, self.B, self.A)

    def Picklable(self):
        return {'R': self.R,
                'G': self.G,
                'B': self.B,
                'A': self.A}

    def NRGBA(c):
        d = 255
        r = Clamp(c.R, 0, 1)
        g = Clamp(c.G, 0, 1)
        b = Clamp(c.B, 0, 1)
        a = Clamp(c.A, 0, 1)
        return int(r * d), int(g * d), int(b * d), int(a * d)

    def Opaque(a):
        return Color(a.R, a.G, a.B, 1)

    def Alpha(a, alpha):
        return Color(a.R, a.G, a.B, alpha)

    def Lerp(a, b, t):
        return a.Add(b.Sub(a).MulScalar(t))

    def Add(a, b):
        return Color(a.R + b.R, a.G + b.G, a.B + b.B, a.A + b.A)

    def Sub(a, b):
        return Color(a.R - b.R, a.G - b.G, a.B - b.B, a.A - b.A)

    def Mul(a, b):
        return Color(a.R * b.R, a.G * b.G, a.B * b.B, a.A * b.A)

    def Div(a, b):
        return Color(a.R / b.R, a.G / b.G, a.B / b.B, a.A / b.A)

    def AddScalar(a, b):
        return Color(a.R + b, a.G + b, a.B + b, a.A + b)

    def SubScalar(a, b):
        return Color(a.R - b, a.G - b, a.B - b, a.A - b)

    def MulScalar(a, b):
        return Color(a.R * b, a.G * b, a.B * b, a.A * b)

    def DivScalar(a, b):
        return Color(a.R / b, a.G / b, a.B / b, a.A / b)

    def Pow(a, b):
        return Color(math.pow(a.R, b), math.pow(a.G, b), math.pow(a.B, b), math.pow(a.A, b))

    def Min(a, b):
        return Color(min(a.R, b.R), min(a.G, b.G), min(a.B, b.B), min(a.A, b.A))

    def Max(a, b):
        return Color(max(a.R, b.R), max(a.G, b.G), max(a.B, b.B), max(a.A, b.A))


Discard = Color()
Transparent = Color()
Black = Color(0, 0, 0, 1)
White = Color(1, 1, 1, 1)


def Gray(x):
    return Color(x, x, x, 1)


