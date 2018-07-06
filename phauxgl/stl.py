
import os
import math
import multiprocessing
from struct import unpack, calcsize
import array

from .vector import Vector
from .vertex import Vertex
from .mesh import NewTriangleMesh
from .util import ParseFloats
from .triangle import Triangle, Triangles
from .box import Box, EmptyBox



def pooled_prep_triangles(flat):
    print 'started'
    _min = Vector()
    _max = Vector()
    #triangles = [] #Triangles()
    triangledata = [] #array.array('f')
    for i in range(0, len(flat), 9):
        v1 = Vector(*flat[i:i+3]) #flat[i], flat[i+1], flat[i+2])
        v2 = Vector(*flat[i+3:i+6]) #flat[i+3], flat[i+4], flat[i+5])
        v3 = Vector(*flat[i+6:i+9]) #flat[i+6], flat[i+7], flat[i+8])
        t = Triangle()
        t.V1.Position = v1
        t.V2.Position = v2
        t.V3.Position = v3
        n = t.Normal()
        #t.V1.Normal = n
        #t.V2.Normal = n
        #t.V3.Normal = n
        #triangles.append(t)
        tridata = [v1.X,v1.Y,v1.Z, v2.X,v2.Y,v2.Z, v3.X,v3.Y,v3.Z, n.X,n.Y,n.Z]
        triangledata.extend(tridata)

        xmin = min(v1.X, v2.X, v3.X)
        xmax = max(v1.X, v2.X, v3.X)
        ymin = min(v1.Y, v2.Y, v3.Y)
        ymax = max(v1.Y, v2.Y, v3.Y)
        zmin = min(v1.Z, v2.Z, v3.Z)
        zmax = max(v1.Z, v2.Z, v3.Z)

        if i == 0:
            _min.X = xmin
            _min.Y = ymin
            _min.Z = zmin
            _max.X = xmax
            _max.Y = ymax
            _max.Z = zmax
        else:
            _min.X = min(_min.X, xmin)
            _min.Y = min(_min.Y, ymin)
            _min.Z = min(_min.Z, zmin)
            _max.X = max(_max.X, xmax)
            _max.Y = max(_max.Y, ymax)
            _max.Z = max(_max.Z, zmax)

    print 'triangles done, returning'
    return triangledata, _min, _max



class STLHeader:
    _ = '<80B' #uint8
    Count = '<L' #uint32

    def read_from(self, file):
        for name in '_ Count'.split():
            fmt = getattr(self, name)
            size = calcsize(fmt)
            val = unpack(fmt, file.read(size))[0]
            setattr(self, name, val)

class STLTriangle:
    N = '3f'
    V1 = '3f'
    V2 = '3f'
    V3 = '3f'
    _ = 'H' #uint16
    
    def read_from(self, file):
        for name in 'N V1 V2 V3 _'.split():
            fmt = getattr(self, name)
            size = calcsize(fmt)
            val = unpack(fmt, file.read(size))[0]
            setattr(self, name, val)

def LoadSTL(path):
    # open file
    with open(path, 'rb') as file:

        # get file size
        size = os.path.getsize(path)

        # read header, get expected binary size
        header = STLHeader()
        header.read_from(file)
        expectedSize = int(header.Count)*50 + 84

        # rewind to start of file
        file.seek(0, 0)

        # parse ascii or binary stl
        if size == expectedSize:
            return loadSTLB(file)
        else:
            return loadSTLA(file)

def loadSTLA(file):
    #print 'STLA'
    normals = []
    vertexes = []
    for line in file:
        fields = line.split()
        if len(fields) == 4 and fields[0] == "vertex":
            f = ParseFloats(fields[1:])
            vertexes.append(Vector(*f[0:3])) #f[0], f[1], f[2]))
        elif len(fields) == 5 and fields[1] == "normal":
            n = ParseFloats(fields[2:])
            normals.append(n)
            
    triangles = [] #Triangles()
    for i in range(0, len(vertexes), 3):
        t = Triangle()
        t.V1.Position = vertexes[i+0]
        t.V2.Position = vertexes[i+1]
        t.V3.Position = vertexes[i+2]
        t.V1.Normal = normals[i+0]
        t.V2.Normal = normals[i+1]
        t.V3.Normal = normals[i+2]
        triangles.append(t)
    return NewTriangleMesh(triangles)

def makeFloat(b):
    return unpack('<f', b) #float64(math.Float32frombits(binary.LittleEndian.Uint32(b)))

def loadSTLB(file):
    #print 'STLB'
    r = file
    header = STLHeader()
    header.read_from(r)
    count = int(header.Count)

    #arr = array.array('f')
    #arr.fromfile(file, count*3*3)

    b = r.read(count*50)
    flat = unpack('<' + '12f2x'*count, b)
    print len(b),count,len(flat)

    # multiprocessing approach
    # NOTE: Maybe not worth it, creating the empty triangle is what takes most time
    # ...bc recreating each triangle creates 5 vertexes, each with a combined 9+8=17 floats, 5*17*8=680 bytes at least.
    # ...Have tried recreating in each process, but sending back the triangle objects requires pickling/un and is slow.
    # ...Maybe the solution is to keep all as triangles simple wrappers pointing to datalists throughout the library.
    # ...Also, making triangle instances, even simple ones with no methods, can triple the time, eg 2-3ses to 8-9 secs.
##    cpus = multiprocessing.cpu_count()
##    trinum = len(flat) / 9
##    chunksize = trinum // cpus
##    chunksize += 1
##    step = 9
##    pool = multiprocessing.Pool(cpus)
##    tasks = [pool.apply_async(pooled_prep_triangles, args=(flat[ti*step:ti*step+chunksize*step],))
##             for ti in range(0, trinum, chunksize)]
##    for task in tasks:
##        print task
##        task.get()
##    results = [task.get() for task in tasks]
##    print 'retrieved'
##    triangledatas,mins,maxs = zip(*results)
##    triangles = []
##    import array
##    
##    class FlatVertex:
##        def __init__(self,
##                     data=None
##                 ):
##            self.data = data or array.array('f', [0 for _ in range(9+8)])
##
####        @property
####        def Position(self):
####            self.Position = Vector(*data[0:3])
####            self.Normal = Normal or Vector()
####            self.Texture = Texture or []#Vector()
####            self.Color = Color or []#Vector() # name conflict
####            self.Output = Output or []#Vector()
##
####    class Triangle:
####        def __init__(self,v1,v2,v3):
####            self.v1=v1
####            self.v2=v2
####            self.v3=v3
##            
##    for tridata in triangledatas:
##        for i in range(0, len(tridata), 12):
####            n = Vector(*tridata[i+9:i+12])
####            v1 = Vector(*tridata[i:i+3]) #flat[i], flat[i+1], flat[i+2])
####            v2 = Vector(*tridata[i+3:i+6]) #flat[i+3], flat[i+4], flat[i+5])
####            v3 = Vector(*tridata[i+6:i+9]) #flat[i+6], flat[i+7], flat[i+8])
##
##            # loading each triangle w flat list
####            p1 = tridata[i:i+12] # pos
####            p2 = tridata[i+3:i+6]
####            p3 = tridata[i+6:i+9]
####            n = tridata[i+9:i+12] # norm
####            fill = [0 for _ in range(3+8)] # add fillers for texture,color,output
####            data = p1+n+fill+p2+n+fill+p3+n+fill
##
##            # loading each vertex w flat list
####            d1 = tridata[i:i+3] # pos
####            d2 = tridata[i+3:i+6]
####            d3 = tridata[i+6:i+9]
####            n = tridata[i+9:i+12] # norm
####            d1.extend(n)
####            d2.extend(n)
####            d3.extend(n)
####            fill = [0 for _ in range(3+8)] # add fillers for texture,color,output
####            d1.extend(fill)
####            d2.extend(fill)
####            d3.extend(fill)
####            v1 = FlatVertex(d1)
####            v2 = FlatVertex(d2)
####            v3 = FlatVertex(d3)
####            t = Triangle(v1,v2,v3)
##
##            # pure tuples approach
####            p1 = tridata[i:i+3] # pos
####            p2 = tridata[i+3:i+6]
####            p3 = tridata[i+6:i+9]
####            n = tridata[i+9:i+12] # norm
####            v1 = Vertex(Position=p1,Normal=n,Texture=(0,0,0),Color=(0,0,0,0),Output=(0,0,0,0)) #flat[i], flat[i+1], flat[i+2])
####            v2 = Vertex(Position=p2,Normal=n,Texture=(0,0,0),Color=(0,0,0,0),Output=(0,0,0,0)) #flat[i+3], flat[i+4], flat[i+5])
####            v3 = Vertex(Position=p3,Normal=n,Texture=(0,0,0),Color=(0,0,0,0),Output=(0,0,0,0)) #flat[i+6], flat[i+7], flat[i+8])
####            t = Triangle(v1,v2,v3)
##
##            # normal approach
##            # ...(still faster than non-paralell approach,
##            # ...since we avoid initiating empty vertexes and thus avoid creating useless temporary vectors)
##            p1 = Vector(*tridata[i:i+3]) # pos
##            p2 = Vector(*tridata[i+3:i+6])
##            p3 = Vector(*tridata[i+6:i+9])
##            n = Vector(*tridata[i+9:i+12]) # norm
##            v1 = Vertex(Position=p1,Normal=n) #flat[i], flat[i+1], flat[i+2])
##            v2 = Vertex(Position=p2,Normal=n) #flat[i+3], flat[i+4], flat[i+5])
##            v3 = Vertex(Position=p3,Normal=n) #flat[i+6], flat[i+7], flat[i+8])
##            t = Triangle(v1,v2,v3)
##            
##            triangles.append(t)
##    print 'reconstructed'
##
##    xmins = [v.X for v in mins]
##    ymins = [v.Y for v in mins]
##    zmins = [v.Z for v in mins]
##    _min = Vector(min(xmins), min(ymins), min(zmins))
##    xmaxs = [v.X for v in maxs]
##    ymaxs = [v.Y for v in maxs]
##    zmaxs = [v.Z for v in maxs]
##    _max = Vector(max(xmaxs), max(ymaxs), max(zmaxs))


    # experiments with faster data structures
####    def itr():
####        zeros = tuple([0.0 for _ in range(3+4+4)])
####        for i in range(0, len(flat), 12):
####            n = flat[i:i+3]
####            v1 = flat[i+3:i+6] + n + zeros
####            v2 = flat[i+6:i+9] + n + zeros
####            v3 = flat[i+9:i+12] + n + zeros
####            yield v1 + v2 + v3
####
####    import itertools
####    init = itertools.chain(*itr())
####    data = array.array('f', init)
####    sfsd
##
##    data = array.array('f')
##    zeros = tuple([0.0 for _ in range(3+4+4)])
##    for i in range(0, len(flat), 12):
##        n = flat[i:i+3]
##        data.extend(flat[i+3:i+6] + n + zeros)
##        data.extend(flat[i+6:i+9] + n + zeros)
##        data.extend(flat[i+9:i+12] + n + zeros)
##    print 'arrays built'
##    for i in xrange(len(data)):
##        data[i]
##    print 'all array values read'
##    for i in xrange(len(data)):
##        data[i] = 3.3
##    print 'all array values reassigned'
##    for i in xrange(0, len(data), 9+8):
##        vx1 = ((data[i:i+3]),(data[i+3:i+6]),(data[i+6:i+9]),
##                     (data[i+9:i+12]),(data[i+12:i+15]))
##        i += 9+8
##        vx2 = ((data[i:i+3]),(data[i+3:i+6]),(data[i+6:i+9]),
##                     (data[i+9:i+12]),(data[i+12:i+15]))
##        i += 9+8
##        vx3 = ((data[i:i+3]),(data[i+3:i+6]),(data[i+6:i+9]),
##                     (data[i+9:i+12]),(data[i+12:i+15]))
##        # NOTE: creating all the vector instances below is the main bottleneck
##        # ...of storing data in array. But maybe can just read on-demand, and
##        # ...maybe can reduce overhead of Vector creation, or maybe just drop
##        # ...Vector class alltogether, as this is the smallest possible unit,
##        # ...instead using tuples 3+ floats.
####        vx1 = (Vector(data[i:i+3]),Vector(data[i+3:i+6]),Vector(data[i+6:i+9]),
####                     Vector(data[i+9:i+12]),Vector(data[i+12:i+15]))
####        i += 9+8
####        vx2 = (Vector(data[i:i+3]),Vector(data[i+3:i+6]),Vector(data[i+6:i+9]),
####                     Vector(data[i+9:i+12]),Vector(data[i+12:i+15]))
####        i += 9+8
####        vx3 = (Vector(data[i:i+3]),Vector(data[i+3:i+6]),Vector(data[i+6:i+9]),
####                     Vector(data[i+9:i+12]),Vector(data[i+12:i+15]))
##        Triangle(vx1,vx2,vx3)
##    fdsfs

    # struct approach
##    from ctypes import Structure,c_float
##    class Vector(Structure):
##        _fields_ = [('X',c_float),
##                    ('Y',c_float),
##                    ('Z',c_float)]
##    class VectorW(Structure):
##        _fields_ = [('X',c_float),
##                    ('Y',c_float),
##                    ('Z',c_float),
##                    ('W',c_float)]
##    class Vertex(Structure):
##        _fields_ = [('Position',Vector),
##                    ('Normal',Vector),
##                    ('Texture',Vector),
##                    ('Color',VectorW),
##                    ('Output',VectorW)]
##    class Triangle(Structure):
##        _fields_ = [('V1',Vertex),
##                    ('V2',Vertex),
##                    ('V3',Vertex)]
##    _min = Vector()
##    _max = Vector()
##    from multiprocessing import Array
##    triangles = Array(Triangle, count) #[] #Triangles()
##    for i in range(0, len(flat), 12):
##        n = Vector(*flat[i:i+3]) #flat[i], flat[i+1], flat[i+2])
##        v1 = Vector(*flat[i+3:i+6]) #flat[i+3], flat[i+4], flat[i+5])
##        v2 = Vector(*flat[i+6:i+9]) #flat[i+6], flat[i+7], flat[i+8])
##        v3 = Vector(*flat[i+9:i+12])
##        t = Triangle()
##        t.V1.Position = v1
##        t.V2.Position = v2
##        t.V3.Position = v3
##        #n = t.Normal()
##        t.V1.Normal = n
##        t.V2.Normal = n
##        t.V3.Normal = n
##        triangles[i//12] = t
##
##        xmin = min(v1.X, v2.X, v3.X)
##        xmax = max(v1.X, v2.X, v3.X)
##        ymin = min(v1.Y, v2.Y, v3.Y)
##        ymax = max(v1.Y, v2.Y, v3.Y)
##        zmin = min(v1.Z, v2.Z, v3.Z)
##        zmax = max(v1.Z, v2.Z, v3.Z)
##
##        if i == 0:
##            _min.X = xmin
##            _min.Y = ymin
##            _min.Z = zmin
##            _max.X = xmax
##            _max.Y = ymax
##            _max.Z = zmax
##        else:
##            _min.X = min(_min.X, xmin)
##            _min.Y = min(_min.Y, ymin)
##            _min.Z = min(_min.Z, zmin)
##            _max.X = max(_max.X, xmax)
##            _max.Y = max(_max.Y, ymax)
##            _max.Z = max(_max.Z, zmax)

    # triangles approach
##    import array
##    _min = Vector()
##    _max = Vector()
##    
##    class Triangles:
##        def __init__(self):
##            self.points = array.array('f')
##            self.points_lookup = dict()
##            self.faces = array.array('I')
##            self.extra = array.array('f')
##            
##        def append(self, p1, p2, p3):
##            indexes = []
##            for p in (p1,p2,p3):
##                i = self.points_lookup.get(p, -1)
##                if i < 0:
##                    self.points.extend(p)
##                    i = len(self.points_lookup)
##                    self.points_lookup[p] = i
##                indexes.append(i)
##            self.faces.extend(indexes)
##            zeros = array.array('f', [0]*(3+3+4+4))
##            self.extra.extend(zeros+zeros+zeros) # SO SLOW...
##
##        def __len__(self):
##            return len(self.faces)//3
##
##        def __iter__(self):
##            for ti in xrange(len(self)):
##                yield self[ti]
##
##        def __getitem__(self, i):
##            flati = i * 3
##            i1,i2,i3 = self.faces[flati:flati+3]
##            pi1,pi2,pi3 = i1*3,i2*3,i3*3
##            p1,p2,p3 = self.points[pi1:pi1+3], self.points[pi2:pi2+3], self.points[pi3:pi3+3]
####            tri = Triangle(Vertex(Position=Vector(*p1)),
####                           Vertex(Position=Vector(*p2)),
####                           Vertex(Position=Vector(*p3)))
##
####            arr = array.array
####            zeros = arr('f', [0]*(3+3+4+4))
####            tri = arr('f', p1+zeros+p2+zeros+p3+zeros)
####            print len(tri), tri
##
##            tri = Triangle(p1, p2, p3)
##
##            return tri
##
##    class Triangle:
##        def __init__(self, p1, p2, p3):
##            arr = array.array
##            zeros = arr('f', [0]*(3+3+4+4))
##            self._data = arr('f', p1+zeros+p2+zeros+p3+zeros)
####            self._data1 = arr('f', p1+zeros)
####            self._data2 = arr('f', p2+zeros)
####            self._data3 = arr('f', p3+zeros)
##
####    class Vertex:
####        def __init__(self, Position, Normal=None, Texture=None, Color=None, Output=None):
####            self.P
##                    
##    triangles = Triangles()
##    for i in range(0, len(flat), 12):
####        n = Vector(*flat[i:i+3]) #flat[i], flat[i+1], flat[i+2])
####        v1 = Vector(*flat[i+3:i+6]) #flat[i+3], flat[i+4], flat[i+5])
####        v2 = Vector(*flat[i+6:i+9]) #flat[i+6], flat[i+7], flat[i+8])
####        v3 = Vector(*flat[i+9:i+12])
####        t = Triangle()
####        t.V1.Position = v1
####        t.V2.Position = v2
####        t.V3.Position = v3
####        #n = t.Normal()
####        t.V1.Normal = n
####        t.V2.Normal = n
####        t.V3.Normal = n
####        triangles.append(t)
##        p1 = flat[i+3:i+6]
##        p2 = flat[i+6:i+9]
##        p3 = flat[i+9:i+12]
##        triangles.append(p1, p2, p3)
##        continue
##
##        xmin = min(v1.X, v2.X, v3.X)
##        xmax = max(v1.X, v2.X, v3.X)
##        ymin = min(v1.Y, v2.Y, v3.Y)
##        ymax = max(v1.Y, v2.Y, v3.Y)
##        zmin = min(v1.Z, v2.Z, v3.Z)
##        zmax = max(v1.Z, v2.Z, v3.Z)
##
##        if i == 0:
##            _min.X = xmin
##            _min.Y = ymin
##            _min.Z = zmin
##            _max.X = xmax
##            _max.Y = ymax
##            _max.Z = zmax
##        else:
##            _min.X = min(_min.X, xmin)
##            _min.Y = min(_min.Y, ymin)
##            _min.Z = min(_min.Z, zmin)
##            _max.X = max(_max.X, xmax)
##            _max.Y = max(_max.Y, ymax)
##            _max.Z = max(_max.Z, zmax)

    # normal approach
    _min = Vector()
    _max = Vector()
    triangles = [] #Triangles()
    for i in range(0, len(flat), 12):
        n = Vector(*flat[i:i+3]) #flat[i], flat[i+1], flat[i+2])
        v1 = Vector(*flat[i+3:i+6]) #flat[i+3], flat[i+4], flat[i+5])
        v2 = Vector(*flat[i+6:i+9]) #flat[i+6], flat[i+7], flat[i+8])
        v3 = Vector(*flat[i+9:i+12])
        t = Triangle()
        t.V1.Position = v1
        t.V2.Position = v2
        t.V3.Position = v3
        #n = t.Normal()
        t.V1.Normal = n
        t.V2.Normal = n
        t.V3.Normal = n
        triangles.append(t)

        xmin = min(v1.X, v2.X, v3.X)
        xmax = max(v1.X, v2.X, v3.X)
        ymin = min(v1.Y, v2.Y, v3.Y)
        ymax = max(v1.Y, v2.Y, v3.Y)
        zmin = min(v1.Z, v2.Z, v3.Z)
        zmax = max(v1.Z, v2.Z, v3.Z)

        if i == 0:
            _min.X = xmin
            _min.Y = ymin
            _min.Z = zmin
            _max.X = xmax
            _max.Y = ymax
            _max.Z = zmax
        else:
            _min.X = min(_min.X, xmin)
            _min.Y = min(_min.Y, ymin)
            _min.Z = min(_min.Z, zmin)
            _max.X = max(_max.X, xmax)
            _max.Y = max(_max.Y, ymax)
            _max.Z = max(_max.Z, zmax)

    
        # OLD
##    triangles = [Triangle() for _ in range(count)] 
##    _triangles = [Triangle() for _ in range(count)]
##    
##    b = r.read(count*50)
##
##    wn = multiprocessing.cpu_count()
##    pool = multiprocessing.Pool(wn)
##    results = []
##    for wi in range(0, wn):
##        def mapfunc(wi=wi):
##            for i in range(wi, count, wn):
##                j = i * 50
##                v1 = Vector(makeFloat(b[j+12 : j+16]), makeFloat(b[j+16 : j+20]), makeFloat(b[j+20 : j+24]))
##                v2 = Vector(makeFloat(b[j+24 : j+28]), makeFloat(b[j+28 : j+32]), makeFloat(b[j+32 : j+36]))
##                v3 = Vector(makeFloat(b[j+36 : j+40]), makeFloat(b[j+40 : j+44]), makeFloat(b[j+44 : j+48]))
##                t = _triangles[i]
##                t.V1.Position = v1
##                t.V2.Position = v2
##                t.V3.Position = v3
##                n = t.Normal()
##                t.V1.Normal = n
##                t.V2.Normal = n
##                t.V3.Normal = n
##                if i == wi:
##                    min = v1
##                    max = v1
##                for _, v in enumerate((Vector(v1, v2, v3) for _ in range(3))):
##                    if v.X < min.X:
##                        min.X = v.X
##                    if v.Y < min.Y:
##                        min.Y = v.Y
##                    if v.Z < min.Z:
##                        min.Z = v.Z
##                    if v.X > max.X:
##                        max.X = v.X
##                    if v.Y > max.Y:
##                        max.Y = v.Y
##                    if v.Z > max.Z:
##                        max.Z = v.Z
##                triangles[i] = t
##            return Box(min, max)
##        results.append( pool.apply_async(mapfunc) )
##
##    box = EmptyBox
##    pool.join()
##    for res in results:
##        box = box.Extend(res)

    box = Box(_min, _max)

##    print box
##    for t in triangles:
##        print t
        
    mesh = NewTriangleMesh(triangles)
    mesh.box = box
    return mesh

##func SaveSTL(path string, mesh *Mesh) error {
##      file, err := os.Create(path)
##      if err != nil {
##              return err
##      }
##      defer file.Close()
##      w := bufio.NewWriter(file)
##      header := STLHeader{}
##      header.Count = uint32(len(mesh.Triangles))
##      if err := binary.Write(w, binary.LittleEndian, &header); err != nil {
##              return err
##      }
##      for _, triangle := range mesh.Triangles {
##              n := triangle.Normal()
##              d := STLTriangle{}
##              d.N[0] = float32(n.X)
##              d.N[1] = float32(n.Y)
##              d.N[2] = float32(n.Z)
##              d.V1[0] = float32(triangle.V1.Position.X)
##              d.V1[1] = float32(triangle.V1.Position.Y)
##              d.V1[2] = float32(triangle.V1.Position.Z)
##              d.V2[0] = float32(triangle.V2.Position.X)
##              d.V2[1] = float32(triangle.V2.Position.Y)
##              d.V2[2] = float32(triangle.V2.Position.Z)
##              d.V3[0] = float32(triangle.V3.Position.X)
##              d.V3[1] = float32(triangle.V3.Position.Y)
##              d.V3[2] = float32(triangle.V3.Position.Z)
##              if err := binary.Write(w, binary.LittleEndian, &d); err != nil {
##                      return err
##              }
##      }
##      w.Flush()
##      return nil
##}
