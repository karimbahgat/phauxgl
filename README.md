# PhauxGL

*3D software rendering in pure Python. No OpenGL, no C extensions, no nothin'*

This is a straight Python port of [Michael Fogleman's excellent FauxGL library](https://github.com/fogleman/fauxgl) for the Go language. 
I know little to nothing about 3D rasterization, so all credit goes to Michael Fogleman. 

![3D Rendering of Multiple Objects](/examples/multi.png)

## The Python Version

### Adaptions for Python

Since FauxGL was orignally written for Go, which is quite a bit faster than Python, it has been necessary to adapt the
code to the peculiarities of the Python language, to make it as fast and memory efficient as possible. 
Better Python-specific documentation, examples, and image renderings to be included later. For now, just look in the "/examples/" folder. 

- It works, and is fun to play around with, but does not work at all for real-time rendering. 
  For instance, the Stanford Dragon takes about 11 seconds to render on a 500*500 image with no supersampling and 8 cores. Bowser however takes about 2 seconds. 
- Features include solid color and phong shading, textures with or without phong shading, wireframes, etc. 
- Includes a very basic Tkinter app for interactively navigating the scene (work-in-progress). 
- Some additional convenience tools for creating triangle meshes and textures from surface xyz grid values. 

### Current limitations:

- Support for parallel processing is currently only implemented for rasterizing triangles, not lines, or file reading. 
- Only .stl files are currently supported, not yet .obj, .ply, or .3ds. 
- Line class and drawing not yet ported. 
- Shape creation and vox rendering not yet ported. 
- Mesh simplification not yet supported (https://github.com/fogleman/simplify). 
- Added some arbitrary handling of rare zerodivision errors in rasterizating(), but not sure if this was the correct way to do it. 
- Parallel processing writes each pixel to a single shared array, but I have not yet implemented any write-locks. Thus you may see 
  strange artifacts for areas that have triangles behind other triangles. 

### Future optimizations:

- Add parallel processing for Mesh.Transform() (moving or shifting all vectors in a mesh, a common operation). 
- Add parallel processing for Mesh.SmoothNormals/Threshold(), since calculating normals can be computationally expensive. 
- Probably the best optimization that can be done is reorganizing the data structures. Throughout the code, 
  what takes the most time (and memory) is creating individual class instances for each vector, vertex, and triangle.
  - One way could be to switch class methods to functions, and just operate on pure Python values and tuples. 
  - Another way could be to store all mesh data in a flat memory efficient array.array's data structure, 
    only creating class instances when needed, having them reference the array structure and update when changed.
	This would also avoid storing duplicates of shared vertexes between neighbouring triangles, resulting in significant reduction of memory
    usage, faster data transfers to parallel processes, and fewer computations. 
    It remains to be seen if the on-demand instance creations and repeated array getting/setting will cause too much overhead. 
  - A third way could be to create arrays of C-type structures. E.g.: "from multiprocessing.sharedctypes import Value, Array"
    and "class Point(Structure): _fields_ = [('x', c_double), ('y', c_double)]". 
- Add parallel processing when reading files? Maybe not necessary, the actual file reading takes almost no time, it is the creation of objects and 
  calculating normals that take time. 
  
### Credits
  
Original code and logic by Michael Fogleman.
Porting to Python by Karim Bahgat.  

__________________________________________________________

## The original FauxGL documentation by Michael Fogleman.

### About

It's like OpenGL, but it's not. It's FauxGL.

It doesn't use your graphics card, only your CPU. So it's slow and unsuitable for realtime rendering. But it's still pretty fast. It works the same way OpenGL works - rasterizing.

### Features

- STL, OBJ, PLY, 3DS file formats
- triangle rasterization
- vertex and fragment "shaders"
- view volume clipping
- face culling
- alpha blending
- textures
- triangle & line meshes
- depth biasing
- wireframe rendering
- built-in shapes (plane, sphere, cube, cylinder, cone)
- anti-aliasing (via supersampling)
- voxel rendering
- parallel processing

### Performance

FauxGL uses all of your CPU cores. But none of your GPU.

Rendering the Stanford Dragon shown above (871306 triangles) at 1920x1080px takes about 150 milliseconds on my machine. With 4x4=16x supersampling, it takes about 950 milliseconds. This is the time to render a frame and does not include loading the mesh from disk.

### Go Get

    go get -u github.com/fogleman/fauxgl

### Go Run

    cd go/src/github.com/fogleman/fauxgl
    go run examples/hello.go

### Go Doc

https://godoc.org/github.com/fogleman/fauxgl

### Complete Example

```go
package main

import (
	. "github.com/fogleman/fauxgl"
	"github.com/nfnt/resize"
)

const (
	scale  = 1    // optional supersampling
	width  = 1920 // output width in pixels
	height = 1080 // output height in pixels
	fovy   = 30   // vertical field of view in degrees
	near   = 1    // near clipping plane
	far    = 10   // far clipping plane
)

var (
	eye    = V(-3, 1, -0.75)               // camera position
	center = V(0, -0.07, 0)                // view center position
	up     = V(0, 1, 0)                    // up vector
	light  = V(-0.75, 1, 0.25).Normalize() // light direction
	color  = HexColor("#468966")           // object color
)

func main() {
	// load a mesh
	mesh, err := LoadOBJ("examples/dragon.obj")
	if err != nil {
		panic(err)
	}

	// fit mesh in a bi-unit cube centered at the origin
	mesh.BiUnitCube()

	// smooth the normals
	mesh.SmoothNormalsThreshold(Radians(30))

	// create a rendering context
	context := NewContext(width*scale, height*scale)
	context.ClearColorBufferWith(HexColor("#FFF8E3"))

	// create transformation matrix and light direction
	aspect := float64(width) / float64(height)
	matrix := LookAt(eye, center, up).Perspective(fovy, aspect, near, far)

	// use builtin phong shader
	shader := NewPhongShader(matrix, light, eye)
	shader.ObjectColor = color
	context.Shader = shader

	// render
	context.DrawMesh(mesh)

	// downsample image for antialiasing
	image := context.Image()
	image = resize.Resize(width, height, image, resize.Bilinear)

	// save image
	SavePNG("out.png", image)
}
```

![Teapot](http://i.imgur.com/DaqbkLR.png)
