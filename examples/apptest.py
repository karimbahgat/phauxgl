
import sys
sys.path.append('../')

import time

from phauxgl.stl import LoadSTL
from phauxgl.vector import V
from phauxgl.util import Radians
from phauxgl.context import NewContext
from phauxgl.matrix import LookAt
from phauxgl.color import Black, Gray, Color
from phauxgl.shader import NewPhongShader, NewTextureShader
from phauxgl.mesh import Mesh
from phauxgl.image import Image
from phauxgl.texture import NewImageTexture


scale  = 1
width  = 324
height = 324
fovy   = 30
near   = 1
far    = 10


eye    = V(3, 1, 0.5)
center = V(0, -0.1, 0)
up     = V(0, 0, 1)
light = V(0.75, 0.25, 1).Normalize()


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


def grid2texture(grid, gradient, zmin=None, zmax=None):
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



if __name__ == '__main__':
    # load a mesh
    print 'loading mesh...'
    #mesh = LoadSTL("bunny.stl")
    #mesh = LoadSTL("boat.stl")
    #mesh = LoadSTL("stanford_dragon.stl")
    #mesh = LoadSTL("bowser.stl")

    meshes = []
    
    for i,fil in enumerate(("bowser.stl",)):
        print fil
        m = LoadSTL(fil)
        print m
        m.BiUnitCube()
        #m.MoveTo(V(0.5+i*2, 0.5+i*2, 0.5), anchor=V(0.5, 0.5, 0.5))
        meshes.append(m)

##    import pythongis as pg
##    import math
##    poprast = pg.RasterData('AFG elevation.tif')
##    #poprast = pg.RasterData('NOR elevation.tif')
##    #poprast = pg.RasterData('USA elevation.tif')
##    #zscale = 1.5 #0.4
##
##    poprast = poprast.manage.resample(width=200, height=200, bbox=poprast.bbox)
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
##    m = grid2mesh(grid, 1.5)
##    m.BiUnitCube()
##    meshes.append(m)
##
##    texture = grid2texture(grid,
##                           gradient=[Color(0,0,1,1), # blue
##                                     Color(0,0.7,0,1), # green
##                                     Color(0.2,0.8,0,1), # green
##                                     Color(0.8,0.8,0,1), # yellow
##                                     #Color(0.8,0.2,0,1), # orange
##                                     Color(199/255.0,111/255.0,75/255.0,1), # brown
##                                     Gray(0.5),
##                                     Gray(1)],
##                           zmin=5) #, zmax=5.5)
##    print texture, texture.Image.data
        
    # floor grid
##    grid = [[(x,y,-0.8+x/2.0) for x in range(-10, 10, 1)]
##            for y in range(-10, 10, 1)]
##    floor = grid2mesh(grid)
##    meshes.append(floor)

    # create a rendering context
    print 'setting up context...'
    context = NewContext(width*scale, height*scale)
    context.ClearColor = Black
    #context.Wireframe = True
    #context.LineWidth = 1

    # render
    print 'setting up shader...'
    shader = NewPhongShader(None, light, eye)
    shader.ObjectColor = Color(0, 0.8, 0, 1) # HexColor("FFD34E")
    shader.DiffuseColor = Gray(0.9)
    shader.SpecularColor = Gray(0.25)
    shader.SpecularPower = 5
    #shader.Texture = texture
    context.Shader = shader
    #context.Shader = NewTextureShader(None, texture)

    print 'starting app...'
    from phauxgl.app import App
    app = App(context)
    app.define_scene(eye, center, up, light)
    for m in meshes:
        app.add_mesh(m)
    app.run()
    
