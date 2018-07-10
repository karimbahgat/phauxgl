
from __future__ import division

from .vector import Vector

import math
import os

# TODO: Find a way to ensure grid tools use correct face winding orientation,
# based on axes directions.

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

def GridMesh(grid, zscale=1):
    from .triangle import Triangle
    from .vertex import Vertex
    from .vector import Vector
    from .mesh import Mesh
    
    w = len(grid[0])
    h = len(grid)
    
    triangles = [] #Triangles()
    for row in range(0, h-1):
        for col in range(0, w-1):
            corners = [(col,row),
                        (col+1,row),
                        (col+1,row+1),
                        (col,row+1),
                        ]
            
            t1 = corners[0],corners[3],corners[2]
            vx = []
            for c,r in t1:
                x,y,z = grid[r][c]
                z *= zscale
                xf,yf = col/float(w), row/float(h)
                vx.append( Vertex(Position=Vector(x,y,z), Texture=Vector(xf,yf,0)) )
            t = Triangle(*vx)
            n = t.Normal()
            t.V1.Normal = n
            t.V2.Normal = n
            t.V3.Normal = n
            triangles.append( t )
                
            t2 = corners[0],corners[2],corners[1]
            vx = []
            for c,r in t2:
                x,y,z = grid[r][c]
                z *= zscale
                xf,yf = col/float(w), row/float(h)
                vx.append( Vertex(Position=Vector(x,y,z), Texture=Vector(xf,yf,0)) )
            t = Triangle(*vx)
            n = t.Normal()
            t.V1.Normal = n
            t.V2.Normal = n
            t.V3.Normal = n
            triangles.append( t )

    mesh = Mesh(triangles, None, None)
    return mesh

def GridTexture(grid, gradient, zmin=None, zmax=None):
    from .image import Image
    from .texture import NewImageTexture
    import math
    im = Image(len(grid[0]),len(grid))
    zmin = min((tup[2] for row in grid for tup in row)) if zmin is None else zmin
    zmax = max((tup[2] for row in grid for tup in row)) if zmax is None else zmax
    colors = gradient
    for y,row in enumerate(grid):
        for x,(_,_,z) in enumerate(row):
            #print x,y,map(int,(155*z, 0, 155-155*z, 155))
            zfac = (z-zmin) / float(zmax-zmin)
            zfac = 0 if zfac < 0 else zfac
            zfac = 1 if zfac > 1 else zfac
            #px[x,y] = tuple(map(int,(255*zfac, 0, 255-255*zfac, 255)))
            colidx = (len(colors)-1)*zfac
            #print zfac,colidx
            bwfac = colidx - int(colidx)
            #print bwfac
            c1,c2 = colors[int(math.floor(colidx))], colors[int(math.ceil(colidx))]
            #print c1.Lerp(c2, bwfac).NRGBA()
            im[x,len(grid)-y-1] = c1.Lerp(c2, bwfac).NRGBA()
    #im.show()
    texture = NewImageTexture(im)
    return texture

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
