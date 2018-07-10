
import sys
sys.path.append('../')

import time

from phauxgl.stl import LoadSTL
from phauxgl.vector import V
from phauxgl.util import Radians, GridMesh, GridTexture
from phauxgl.context import NewContext
from phauxgl.matrix import LookAt
from phauxgl.color import Black, Gray, Color
from phauxgl.shader import NewPhongShader, NewSolidColorShader, NewTextureShader
from phauxgl.mesh import Mesh
from phauxgl.texture import NewImageTexture
from phauxgl.image import Image

# TODO: WEIRD 'bad file descriptor' error, but only when in IDLE, not in commandline

scale  = 1
width  = 1000
height = 800
fovy   = 30
near   = 1
far    = 10



if __name__ == '__main__':
    # load a mesh
    print 'loading mesh...'
   
    import gc
    import math
    import pythongis as pg
    #fullrast = pg.RasterData(r"C:\Users\kimok\Downloads\MSR_50M\MSR_50M\MSR_50M.tif")
    #focus = pg.VectorData("C:\Users\kimok\Downloads\cshapes\cshapes.shp", select=lambda f: f['CNTRY_NAME']=='United States')
    #poprast = fullrast.manage.crop(focus.bbox)
    #poprast.save('USA elevation.tif')

    eye    = V(-0.2, -2.5, 4) # 4, 3
    center = V(0, 0.4, 0)
    up     = V(0, 0, 1)
    light = V(-3, 0, 2)

    poprast = pg.RasterData('AFG elevation.tif')
    #poprast = pg.RasterData('NOR elevation.tif')
    #poprast = pg.RasterData('USA elevation.tif')
    zscale = 1.5 #0.4

##    eye    = V(-100, 50, 50) # 4, 3
##    center = V(38, -77, 5)
##    up     = V(0, 90, 0)
##    light = eye
##    poprast = pg.RasterData('USA elevation.tif')
##    zscale = 1 #0.2
    
    poprast = poprast.manage.resample(width=300, height=300, bbox=poprast.bbox)

    print poprast

    grid = []
    for row in range(0, poprast.height):
        grow = []
        for col in range(0, poprast.width):
            cell = poprast.bands[0].get(col,row)
            x,y,z = cell.x, cell.y, cell.value
            z = math.log(z+1)
            grow.append((x,y,z))
        grid.append(grow)

    print 'del'
    del poprast.bands[0].img, poprast
    gc.collect()

    mesh = GridMesh(grid, zscale=zscale)
    print mesh.BoundingBox()
    print mesh

    texture = GridTexture(grid,
                           gradient=[Color(0,0,1,1), # blue
                                     Color(0,0.7,0,1), # green
                                     Color(0.2,0.8,0,1), # green
                                     Color(0.8,0.8,0,1), # yellow
                                     #Color(0.8,0.2,0,1), # orange
                                     Color(199/255.0,111/255.0,75/255.0,1), # brown
                                     Gray(0.5),
                                     Gray(1)],
                           zmin=5) #, zmax=5.5)
    print texture, texture.Image.data

    # fit mesh in a bi-unit cube centered at the origin
    print 'prepping mesh...'
    mesh.BiUnitCube()
    mesh.box = mesh.BoundingBox()

    # smooth the normals
    #mesh.SmoothNormalsThreshold(Radians(30))
    #mesh.SmoothNormals()

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
    context.Shader = NewTextureShader(matrix, texture)

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
    image.save("landscape.png")
    
