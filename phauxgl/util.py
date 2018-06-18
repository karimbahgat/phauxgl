
from __future__ import division

import math
import os

def Radians(degrees):
    return degrees * math.pi / 180.0

def Degrees(radians):
    return radians * 180 / math.pi

def LatLngToXYZ(lat, lng):
    lat, lng = Radians(lat), Radians(lng)
    x = math.cos(lat) * math.cos(lng)
    y = math.cos(lat) * math.sin(lng)
    z = math.sin(lat)
    return Vector(x, y, z)

##func LoadMesh(path string) (*Mesh, error) {
##      ext := strings.ToLower(filepath.Ext(path))
##      switch ext {
##      case ".stl":
##              return LoadSTL(path)
##      case ".obj":
##              return LoadOBJ(path)
##      case ".ply":
##              return LoadPLY(path)
##      case ".3ds":
##              return Load3DS(path)
##      }
##      return nil, fmt.Errorf("unrecognized mesh extension: %s", ext)
##}
##
##func LoadImage(path string) (image.Image, error) {
##      file, err := os.Open(path)
##      if err != nil {
##              return nil, err
##      }
##      defer file.Close()
##      im, _, err := image.Decode(file)
##      return im, err
##}
##
##func SavePNG(path string, im image.Image) error {
##      file, err := os.Create(path)
##      if err != nil {
##              return err
##      }
##      defer file.Close()
##      return png.Encode(file, im)
##}

def ParseFloats(items):
    result = []
    for i, item in enumerate(items):
        result[i] = float(item)
    return result

def Clamp(x, lo, hi):
    if x < lo:
        return lo
    if x > hi:
        return hi
    return x

def ClampInt(x, lo, hi):
        if x < lo:
            return lo
        if x > hi:
            return hi
        return x

def AbsInt(x):
    if x < 0:
        return -x
    return x

def Round(a):
    if a < 0:
        return int(math.ceil(a - 0.5))
    else:
        return int(math.floor(a + 0.5))

def RoundPlaces(a, places):
    return round(a, places)
