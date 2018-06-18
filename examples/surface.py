
import sys
sys.path.append('../')

import time

from phauxgl.stl import LoadSTL
from phauxgl.vector import V
from phauxgl.util import Radians
from phauxgl.context import NewContext
from phauxgl.matrix import LookAt
from phauxgl.color import Black, Gray, Color
from phauxgl.shader import NewPhongShader, NewSolidColorShader, NewTextureShader
from phauxgl.mesh import Mesh
from phauxgl.texture import NewImageTexture


scale  = 1
width  = 324
height = 324
fovy   = 30
near   = 1
far    = 10


def grid2mesh(grid, zscale=1):
    from phauxgl.triangle import Triangle
    from phauxgl.vertex import Vertex
    from phauxgl.vector import Vector
    
    w = len(grid[0])
    h = len(grid)
    
    triangles = []
    for row in range(0, h-1):
        for col in range(0, w-1):
            corners = [(col,row),
                        (col+1,row),
                        (col+1,row+1),
                        (col,row+1),
                        ]
            
            t1 = corners[0],corners[1],corners[2]
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
                
            t2 = corners[2],corners[3],corners[0]
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


if __name__ == '__main__':
    # load a mesh
    print 'loading mesh...'

    center = V(0, 0, 0)
    up     = V(0, 0, 1)
    #light = V(0.75, 0.25, 1).Normalize()
    light = V(-2, -3, 3)

##    import gc
##    import math
##    import pythongis as pg
##    #fullrast = pg.RasterData(r"C:\Users\kimok\Downloads\MSR_50M\MSR_50M\MSR_50M.tif")
##    #focus = pg.VectorData("C:\Users\kimok\Downloads\cshapes\cshapes.shp", select=lambda f: f['CNTRY_NAME']=='United States')
##    #poprast = fullrast.manage.crop([44,25,64,40])
##    #poprast = fullrast.manage.clip(focus, bbox=focus.bbox)
##    #poprast.save('USA elevation.tif')
##
####    eye    = V(-2, -2, 2) # 4, 3
####    poprast = pg.RasterData('AFG elevation.tif')
####    zscale = 0.1
##
##    eye    = V(-2, -2, 2) # 4, 3
##    poprast = pg.RasterData('NOR elevation.tif')
##    zscale = 0.1
##    
####    eye    = V(2, -3, 1) # 4, 3
####    light = eye
####    poprast = pg.RasterData('USA elevation.tif')
####    zscale = 0.2
##
####    eye    = V(-100, 50, 50) # 4, 3
####    center = V(38, -77, 5)
####    up     = V(0, 90, 0)
####    light = eye
####    poprast = pg.RasterData('USA elevation.tif')
####    zscale = 1 #0.2
##    
##    poprast = poprast.manage.resample(width=90, height=90, bbox=poprast.bbox)
##
####    import PIL, PIL.Image
####    im = poprast.bands[0].img.convert('RGBA')
####    texture = NewImageTexture(im)
##
##    print poprast
##
##    grid = []
##    for row in range(0, poprast.height):
##        grow = []
##        for col in range(0, poprast.width):
##            cell = poprast.bands[0].get(col,row)
##            x,y,z = cell.x, cell.y, cell.value
##            z = math.log(z+1)
##            grow.append((x,y,z))
##        grid.append(grow)
##
##    print 'del'
##    del poprast.bands[0].img, poprast
##    gc.collect()

    eye    = V(2, 2, 1) # 4, 3
    center = V(0, 0, 0)
    up     = V(0, 0, 1)
    light = V(0.75, 0.25, 1).Normalize()

    import math
    grid = []
    for row in range(0, 100):
        grow = []
        for col in range(0, 100):
            val = math.cos(col) + math.sin(row)
            x,y,z = col, row, val
            grow.append((x,y,z))
        grid.append(grow)
    zscale = 0.3

##    import PIL, PIL.Image
##    im = PIL.Image.new('RGBA', (100,100))
##    px = im.load()
##    for y,row in enumerate(grid):
##        for x,(_,_,z) in enumerate(row):
##            #print x,y,map(int,(155*z, 0, 155-155*z, 155))
##            px[x,y] = tuple(map(int,(155*z, 0, 155-155*z, 155)))
##    texture = NewImageTexture(im)

##    eye    = V(2, 5, 4) # 4, 3
##    center = V(0, 0, 0)
##    up     = V(0, 0, 1)
##    light = V(0.75, 0.25, 1).Normalize()
##
##    import math
##    grid = []
##    for row in range(-500, 500, 25):
##        row /= 100.0
##        grow = []
##        for col in range(-500, 500, 25):
##            col /= 100.0
##            val = math.sin(math.sqrt(col**2 + row**2))
##            x,y,z = col, row, val
##            grow.append((x,y,z))
##        grid.append(grow)
##    zscale = 4

    mesh = grid2mesh(grid, zscale=zscale)
    print mesh.BoundingBox()
    print mesh

    # fit mesh in a bi-unit cube centered at the origin
    print 'prepping mesh...'
    mesh.BiUnitCube()
    mesh.box = mesh.BoundingBox()

    # smooth the normals
    mesh.SmoothNormalsThreshold(Radians(30))

    # create a rendering context
    print 'setting up context...'
    context = NewContext(width*scale, height*scale)
    context.ClearColorBufferWith(Black)

    # create transformation matrix
    print 'setting up matrix...'
    aspect = float(width) / float(height)
    matrix = LookAt(eye, center, up).Perspective(fovy, aspect, near, far)

    # render
    print 'setting up shader...'
    shader = NewPhongShader(matrix, light, eye)
    shader.ObjectColor = Color(0, 0.8, 0, 1) # HexColor("FFD34E")
    shader.DiffuseColor = Gray(0.9)
    shader.SpecularColor = Gray(0.25)
    shader.SpecularPower = 100
    context.Shader = shader
    #context.Shader = NewSolidColorShader(matrix, Color(0, 0.8, 0, 1))
    #context.Shader = NewTextureShader(matrix, texture)

    print 'rendering...'
    start = time.time()
    info = context.DrawMesh(mesh)
    
    print 'rendered in', time.time() - start, 'seconds'
    print info

    # save image
    image = context.Image()
    if scale != 1:
        # supersampling
        image = image.resize((width, height)) #, PIL.Image.BILINEAR)
    image.save("surface.png")
    
