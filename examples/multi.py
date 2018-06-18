
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
from phauxgl.mesh import NewEmptyMesh


scale  = 1
width  = 1000
height = 400
fovy   = 30
near   = 1
far    = 10


eye    = V(1, -2, 0.5)
center = V(0, -0.1, 0)
up     = V(0, 0, 1)
light = V(0.75, 0.25, 1).Normalize()


if __name__ == '__main__':
    # load mesh 1
    print 'loading mesh...'
    mesh = NewEmptyMesh()
    for i,fil in enumerate(("bowser.stl","bunny.stl","boat.stl")):
        print fil
        m = LoadSTL(fil)
        print m
        print repr(m.Triangles)[:100]
        m.BiUnitCube()
        m.MoveTo(V(0.5+i*2, 0.5+i*2, 0.5), anchor=V(0.5, 0.5, 0.5))
        mesh.Add( m )
    print 'prepping mesh...'
    mesh.BiUnitCube()

    # create a rendering context
    print 'setting up context...'
    context = NewContext(width*scale, height*scale)
    context.ClearColorBufferWith(Black)

    # create transformation matrix and light direction
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
    image.save("multi.png")
    
