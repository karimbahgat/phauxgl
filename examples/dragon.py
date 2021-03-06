
import sys
sys.path.append('../')

import time

from phauxgl.stl import LoadSTL
from phauxgl.vector import V
from phauxgl.util import Radians
from phauxgl.context import NewContext
from phauxgl.matrix import LookAt
from phauxgl.color import Black, Gray, Color
from phauxgl.shader import NewPhongShader


scale  = 1
width  = 1920/4
height = 1920/4
fovy   = 30
near   = 1
far    = 10


eye    = V(-2, -4, 1)
center = V(0, -0.1, 0)
up     = V(0, 0, 1)


if __name__ == '__main__':
    # load a mesh
    print 'loading mesh...'
    #eye    = V(0, -5, 1.5)
    #mesh = LoadSTL("bunny.stl")
    #mesh = LoadSTL("boat.stl")
    mesh = LoadSTL("stanford_dragon.stl")
    #mesh = LoadSTL("bowser.stl")

    # fit mesh in a bi-unit cube centered at the origin
    print 'prepping mesh...'
    mesh.BiUnitCube()

    # smooth the normals
    #mesh.SmoothNormalsThreshold(Radians(30))

    # create a rendering context
    print 'setting up context...'
    context = NewContext(width*scale, height*scale)
    context.ClearColorBufferWith(Black)
    context.Cull = 4
    #context.Wireframe = True
    #context.LineWidth = 1

    # create transformation matrix and light direction
    print 'setting up matrix...'
    aspect = float(width) / float(height)
    matrix = LookAt(eye, center, up).Perspective(fovy, aspect, near, far)
    light = V(-0.7, -0.7, 0.2)

    # render
    print 'setting up shader...'
    shader = NewPhongShader(matrix, light, eye)
    shader.ObjectColor = Color(0, 0.8, 0, 1) # HexColor("FFD34E")
    shader.DiffuseColor = Gray(0.9)
    shader.SpecularColor = Gray(0.25)
    shader.SpecularPower = 100
    context.Shader = shader

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
    image.save("dragon.png")
    
