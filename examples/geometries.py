
import sys
sys.path.append('../')

import time

from phauxgl.stl import LoadSTL
from phauxgl.vector import V
from phauxgl.util import Radians
from phauxgl.context import NewContext
from phauxgl.matrix import LookAt, Translate
from phauxgl.color import Black, Gray, Color
from phauxgl.shader import NewPhongShader

from phauxgl import shapes


scale  = 1
width  = 824
height = 424
fovy   = 30
near   = 1
far    = 10


eye    = V(2*0.8*0, 3*0.8, 1*0.8*0.5)
center = V(0, -0.1, 0)
up     = V(0, 0, 1)
light = V(1.95, 1.25, 1).Normalize()


if __name__ == '__main__':
    # load a mesh
    print 'loading mesh...'
    # bbox
    cube = shapes.NewCube()
    cube.BiUnitCube()
    mesh = cube

    # plane
    #mesh.MoveTo(V(2, 0, 0.5), anchor=V(0.5, 0.5, 0.5))
    #mesh.Add( shapes.NewPlane() )

    # globe
    mesh.MoveTo(V(3, 0, 0.5), anchor=V(0.5, 0.5, 0.5))
    globe = shapes.NewLatLngSphere(10, 10)
    globe.BiUnitCube()
    mesh.Add( globe )

    # cylinder
    mesh.MoveTo(V(5, 0, 0.5), anchor=V(0.5, 0.5, 0.5))
    cylin = shapes.NewCylinder(10, True)
    cylin.BiUnitCube()
    mesh.Add( cylin )

    # cone
    mesh.MoveTo(V(7, 0, 0.5), anchor=V(0.5, 0.5, 0.5))
    cone = shapes.NewCone(10, True)
    cone.BiUnitCube()
    mesh.Add( cone )

    # fit mesh in a bi-unit cube centered at the origin
    print 'prepping mesh...'
    mesh.BiUnitCube()
    print mesh.BoundingBox()

    # and a plane underneath
    plane = shapes.NewPlane()
    plane.BiUnitCube()
    plane.MoveTo(V(0, 0, -0.19), anchor=V(0.5, 0.5, 0.5))
    mesh.Add( plane )
    
    # smooth the normals
    mesh.FixNormals()
    #mesh.SmoothNormalsThreshold(Radians(30))

    # create a rendering context
    print 'setting up context...'
    context = NewContext(width*scale, height*scale)
    context.ClearColorBufferWith(Black)
    #context.FrontFace = 2
    #context.Wireframe = True
    #context.LineWidth = 1

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
    image.save("geometries.png")
    
