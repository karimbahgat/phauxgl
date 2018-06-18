
from __future__ import division

from .color import Color, MakeColor
from .image import Image

import math

# from .color import Color, MakeColor


def LoadTexture(path):
    im = Image.open(path)
    return NewImageTexture(im)

def NewImageTexture(im):
    return ImageTexture(im.Width, im.Height, im)


class ImageTexture:
    def __init__(self, width, height, image):
        self.Width = width
        self.Height = height
        self.Image = image

    def Sample(t, u, v):
        v = 1 - v
        u -= math.floor(u)
        v -= math.floor(v)
        x = int(u * float(t.Width))
        y = int(v * float(t.Height))
        return MakeColor(t.Image[x, y])

    def BilinearSample(t, u, v):
        v = 1 - v
        u -= math.floor(u)
        v -= math.floor(v)
        x = u * float(t.Width)
        y = v * float(t.Height)
        x0 = int(x)
        y0 = int(y)
        x1 = x0 + 1
        y1 = y0 + 1
        x -= float(x0)
        y -= float(y0)
        try:
            c00 = MakeColor(t.Image[x0, y0])
            c01 = MakeColor(t.Image[x0, y1])
            c10 = MakeColor(t.Image[x1, y0])
            c11 = MakeColor(t.Image[x1, y1])
            c = Color()
            c = c.Add(c00.MulScalar((1 - x) * (1 - y)))
            c = c.Add(c10.MulScalar(x * (1 - y)))
            c = c.Add(c01.MulScalar((1 - x) * y))
            c = c.Add(c11.MulScalar(x * y))
        except IndexError:
            return Color()
        return c



