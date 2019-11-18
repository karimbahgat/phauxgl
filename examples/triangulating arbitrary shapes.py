import pytess
import itertools

# Triangulating polygonal shapes from arbitrary series of 3D points.
# NOTE: This is a hacky apprach that will only work on smooth surfaces.
# ...Performs the triangulation on the xy plane, keeping z as is.
# ...This means it will not render faces as going over or under each other,
# ...but will rather alternate between them jaggedly. 

# Define data

import random
def random_n(low, high, n, onlyints=False):
    if onlyints: randfunc = random.randrange
    else: randfunc = random.uniform
    return list(( randfunc(low,high) for _ in xrange(n) ))

test_random = [random_n(10,490,2)+random_n(0,100,1,onlyints=True)
               for _ in xrange(100)]

def midpoint(coords):
    xs,ys,zs = zip(*coords)
    xmid = sum(xs) / len(xs)
    ymid = sum(ys) / len(ys)
    zmid = sum(zs) / len(zs)
    return (xmid,ymid,zmid)

points = test_random
#points = [(0,0,20),(5,5,1),(10,5,3),(10,10,2),(15,5,0),(5,0,10)]

def test_triangulate(points):
    
    # Run test
    triangles = pytess.triangulate(points)

    # Visualize

    import sys
    sys.path.append("/Volumes/karim/Desktop/Python Programming/site_packages")
    import pydraw
    img = pydraw.Image(500,500)

    for triangle in triangles:
        if len(triangle) != 3: print "warning: returned non-triangle"
        triangle_xy = [map(int,point[:2]) for point in triangle]
        xmid,ymid,zmid = midpoint(triangle)
        img.drawpolygon(triangle_xy, fillcolor=(0,zmid,zmid),
                        outlinecolor=None )

    #for point in points:
    #    img.drawsquare(*point[:2], fillsize=2, fillcolor=(0,222,0))

    #img.save("test.png")
    #img.view()
    return triangles

# Run test

if __name__ == "__main__":

    tris = test_triangulate(points)

    from phauxgl import vector,vertex,triangle,context,shader,app,mesh,color,stl

    scale  = 1
    width  = 324
    height = 324
    fovy   = 30
    near   = 1
    far    = 10

    eye    = vector.Vector(3, 1, 0.5)
    center = vector.Vector(0, -0.1, 0)
    up     = vector.Vector(0, 0, 1)
    light = vector.Vector(1, -1, 1)

    triobjs = []
    for tri in tris:
        tri = list(reversed(tri)) # wrong direction gets interpreted as the backside i think
        vx1 = vertex.Vertex(Position=vector.Vector(*tri[0]))
        vx2 = vertex.Vertex(Position=vector.Vector(*tri[1]))
        vx3 = vertex.Vertex(Position=vector.Vector(*tri[2]))
        tobj = triangle.Triangle(vx1,vx2,vx3)
        n = tobj.Normal()
        tobj.V1.Normal = n
        tobj.V2.Normal = n
        tobj.V3.Normal = n
        triobjs.append(tobj)

    #mesh = stl.LoadSTL(r"C:\Users\kimok\OneDrive\Documents\GitHub\phauxgl\examples\bowser.stl")
    mesh = mesh.Mesh(triobjs, None, None)
    mesh.BiUnitCube()
    #mesh.SmoothNormals()

    cx = context
    context = cx.NewContext(width*scale, height*scale)
    context.ClearColor = color.Black
    context.FrontFace = cx.Face # ?
    #context.Wireframe = True

    shader = shader.NewPhongShader(None, light, eye)
    shader.ObjectColor = color.Color(0, 0.8, 0, 1) # HexColor("FFD34E")
    shader.DiffuseColor = color.Gray(0.9)
    shader.SpecularColor = color.Gray(0.25)
    shader.SpecularPower = 5
    context.Shader = shader

    app = app.App(context)
    app.define_scene(eye, center, up, light)
    app.add_mesh(mesh)
    app.run()



