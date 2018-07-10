
from __future__ import division

import sys
import math
import array
import multiprocessing

from .color import Color, Transparent, Discard
from .shader import NewSolidColorShader, PhongShader
from .matrix import Matrix, Identity, Screen
from .vector import Vector, VectorW
from .vertex import InterpolateVertexes, Vertex
from .clipping import ClipTriangle
from .triangle import NewTriangle, Triangle
from .image import Image


Face = 1
FaceCW = 2
FaceCCW = 3

Cull = 1
CullNone = 2
CullFront = 3
CullBack = 4



def edge(a, b, c):
    return (b.X-c.X)*(a.Y-c.Y) - (b.Y-c.Y)*(a.X-c.X)


##def func(indexes):
##    # necessary for multiprocessing, func accessible from top-level
##    result = RasterizeInfo()
##    print 'index %s to %s' % (indexes[0],indexes[-1])
##    #sys.stdout.flush()
##    for i in indexes:
##        t = triangles[i]
##        info = dc.DrawTriangle(t)
##        result = result.Add(info)
##    print 'cpu core finished'
##    #sys.stdout.flush()
##    return result.TotalPixels, result.UpdatedPixels

def pooled_draw_triangles(trindexes):
    # necessary for multiprocessing, func accessible from top-level
    print 'started'
    #print 'arr',len(dc['ColorBuffer']),min(dc['ColorBuffer']),max(dc['ColorBuffer'])
    dc = sharedData['dc'] #Context.FromDict(sharedData['dc'])

    #from random import random
    #dc.Shader.ObjectColor = Color(random(), random(), random(), 1)

    #print dc.Shader
    #print '\n'.join((repr([k,repr(v)[:100]]) for k,v in dc.Shader.__dict__.items()))
    #print 'found shared img', repr(dc.ColorBuffer)[:200]
    #print 'found shared dbuf', repr(dc.DepthBuffer)[:200]
##    #dc = Context.FromDict(dc)
##    print dc

##    dcpickle = sharedData['dc']
##    print dcpickle.keys()
##    for k in dcpickle.keys():
##        print k,getattr(dc,k),dcpickle[k]
##    print dc.screenMatrix.__dict__
##    print dc.Shader.Matrix.__dict__
##    print dcpickle['screenMatrix']
##    print 999,dcpickle['Shader']['Matrix']
    
    result = RasterizeInfo()
    #sys.stdout.flush()
    print 'loading and rendering triangles',len(trindexes) #type(picklable),len(picklable),repr(picklable)[:100]
##    import random
##    rancol = tuple((random.randrange(255) for _ in range(4)))
##    for _ in range(10000):
##        i = random.randrange(len(sharedImage)) // 4
##        sharedImage[i:i+4] = rancol

##    for pdict in picklable:
##        pass #t = Triangle.FromDict(pdict)
##        #info = dc.DrawTriangle(t)
##        #result = result.Add(info)

##    vectors = sharedData['vectors']
##    #print 'found shared vectors', repr(vectors)[:200]
##    step = 3+6+8
##    tris = []
##    #print ['NOW',len(trindexes),trindexes[0:len(trindexes):3]]
##    for ti in trindexes:
##        vi = ti*3 # first vertex of triangle
##        verts = []
##        try:
##            for vi in range(vi, vi+3):
##                vci = vi*step
##                #print ['hmm',len(vectors),vi,vci]
##                p1,p2,p3, n1,n2,n3, t1,t2,t3, c1,c2,c3,c4, o1,o2,o3,o4 = vectors[vci:vci+step]
##                pos = Vector(p1,p2,p3)
##                norm = Vector(n1,n2,n3)
##                tex = Vector(t1,t2,t3)
##                col = Color(c1,c2,c3,c4)
##                out = VectorW(o1,o2,o3,o4)
##                v = Vertex(Position=pos,
##                              Normal=norm,
##                              Texture=tex,
##                              Color=col,
##                              Output=out)
##                verts.append(v)
##            tri = Triangle(*verts)
##            dc.DrawTriangle(tri)
##            tris.append(tri)
##        except:
##            # NEED TO FIX
##            print '!!! skipped triangle'

    tris = sharedData['triangles']
    for ti in trindexes:
        try:
            tri = tris[ti]
            dc.DrawTriangle(tri)
        except:
            print '!!! skipped triangle'
            
    print 'reconstructed',len(tris)

    print 'drawing'
    
    print 'cpu core finished'
    #print 'changed',result.TotalPixels, result.UpdatedPixels
    #sys.stdout.flush()
    #return dc.Picklable() #result.TotalPixels, result.UpdatedPixels


def initSharedData(datadict):
    print 'initfunc'
    global sharedData
    sharedData = datadict


class RasterizeInfo:
    def __init__(self, TotalPixels=0, UpdatedPixels=0):
        self.TotalPixels = TotalPixels
        self.UpdatedPixels = UpdatedPixels

    def Add(info, other):
        return RasterizeInfo(
                info.TotalPixels + other.TotalPixels,
                info.UpdatedPixels + other.UpdatedPixels,
        )



def NewContext(width, height):
    dc = Context()
    dc.Width = width
    dc.Height = height
    dc.ColorBuffer = Image(width,height) #PIL.Image.new('RGBA', (width, height))
    #dc.ColorBuffer.pixels = dc.ColorBuffer.load()
    dc.DepthBuffer = multiprocessing.RawArray('f', [0 for _ in range(width*height)])
    dc.ClearColor = Transparent
    dc.Shader = NewSolidColorShader(Identity(), Color(1, 0, 1, 1))
    dc.ReadDepth = True
    dc.WriteDepth = True
    dc.WriteColor = True
    dc.AlphaBlend = True
    dc.Wireframe = False
    dc.FrontFace = FaceCCW
    dc.Cull = CullBack
    dc.LineWidth = 2
    dc.DepthBias = 0
    dc.screenMatrix = Screen(width, height)
    #dc.locks = None #??? #make([]sync.Mutex, 256)
    dc.ClearDepthBuffer()
    return dc


class Context:
    def __init__(self,
                Width=None,
                Height=None,
                ColorBuffer=None, #*image.NRGBA
                DepthBuffer=None, #[]float64
                ClearColor=None,
                Shader=None,
                ReadDepth=None, #bool
                WriteDepth=None, #bool
                WriteColor=None, #bool
                AlphaBlend=None, #bool
                Wireframe=None, #bool
                FrontFace=None, 
                Cull=CullBack,
                LineWidth=None,
                DepthBias=None,
                screenMatrix=None,
                locks=None, #[]sync.Mutex
                 ):
        self.Width = Width
        self.Height = Height
        self.ColorBuffer = ColorBuffer
        self.DepthBuffer = DepthBuffer
        self.ClearColor = ClearColor
        self.Shader = Shader
        self.ReadDepth = ReadDepth
        self.WriteDepth = WriteDepth
        self.WriteColor = WriteColor
        self.AlphaBlend = AlphaBlend
        self.Wireframe = Wireframe
        self.FrontFace = FrontFace
        self.Cull = Cull
        self.LineWidth = LineWidth
        self.DepthBias = DepthBias
        self.screenMatrix = screenMatrix
        #self.locks = locks

##    def Picklable(dc):
##        pdict = dict(Width = dc.Width,
##                    Height = dc.Height,
##                    ColorBuffer = dc.ColorBuffer.data, #list(dc.ColorBuffer.getdata()), #array.array('B', (val for tup in dc.ColorBuffer.getdata() for val in tup)),
##                    DepthBuffer = dc.DepthBuffer,
##                    ClearColor = (dc.ClearColor.R, dc.ClearColor.G, dc.ClearColor.B, dc.ClearColor.A),
##                    Shader = dc.Shader.Picklable(),
##                    ReadDepth = dc.ReadDepth,
##                    WriteDepth = dc.WriteDepth,
##                    WriteColor = dc.WriteColor,
##                    AlphaBlend = dc.AlphaBlend,
##                    Wireframe = None, #dc.Wireframe
##                    FrontFace = dc.FrontFace,
##                    Cull = dc.Cull,
##                    LineWidth = dc.LineWidth,
##                    DepthBias = dc.DepthBias,
##                    screenMatrix = dict([(k,getattr(dc.screenMatrix,k))
##                                         for k in 'X00 X01 X02 X03 X10 X11 X12 X13 X20 X21 X22 X23 X30 X31 X32 X33'.split() ])
##                     )
##        return pdict
##
##    @staticmethod
##    def FromDict(pdict):
##        dc = Context()
##        for k,v in pdict.items():
##            setattr(dc, k, v)
##        newim = Image(dc.Width, dc.Height) #PIL.Image.new('RGBA', (dc.Width, dc.Height))
##        newim.data = dc.ColorBuffer #.putdata(dc.ColorBuffer),
##        dc.ColorBuffer = newim
##        #dc.ColorBuffer.pixels = newim.load()
##        dc.ClearColor = Color(*pdict['ClearColor'])
##        dc.WireFrame = None
##        dc.screenMatrix = Matrix(*[dc.screenMatrix[k]
##                                         for k in 'X00 X01 X02 X03 X10 X11 X12 X13 X20 X21 X22 X23 X30 X31 X32 X33'.split() ])
##        dc.Shader = PhongShader.FromDict(dc.Shader) #NewSolidColorShader(dc.screenMatrix, Color(1,0,0,1))
##        return dc

    def Image(dc):
        return dc.ColorBuffer

    def ClearColorBufferWith(dc, color):
        c = color.NRGBA() # CHANGE???
        dc.ColorBuffer.clear(c) #paste(c)

    def ClearColorBuffer(dc):
        dc.ClearColorBufferWith(dc.ClearColor)

    def ClearDepthBufferWith(dc, value):
        for i in range(len(dc.DepthBuffer)):
            dc.DepthBuffer[i] = value

    def ClearDepthBuffer(dc):
        dc.ClearDepthBufferWith(float('inf'))

    def rasterize(dc, v0, v1, v2, s0, s1, s2):
        info = RasterizeInfo()

        # integer bounding box
        min = s0.Min(s1.Min(s2)).Floor()
        max = s0.Max(s1.Max(s2)).Ceil()
        x0 = int(min.X)
        x1 = int(max.X)
        y0 = int(min.Y)
        y1 = int(max.Y)

        # forward differencing variables
        p = Vector(float(x0) + 0.5, float(y0) + 0.5, 0)
        w00 = edge(s1, s2, p)
        w01 = edge(s2, s0, p)
        w02 = edge(s0, s1, p)
        a01 = s1.Y - s0.Y
        b01 = s0.X - s1.X
        a12 = s2.Y - s1.Y
        b12 = s1.X - s2.X
        a20 = s0.Y - s2.Y
        b20 = s2.X - s0.X

        # reciprocals
        # NOTE: arbitrarily set to 0 to handle zerodivisionerror, maybe issue warning? 
        try: ra = 1 / edge(s0, s1, s2)
        except ZeroDivisionError: ra = 0
        try: r0 = 1 / v0.Output.W
        except ZeroDivisionError: r0 = 0
        try: r1 = 1 / v1.Output.W
        except ZeroDivisionError: r1 = 0
        try: r2 = 1 / v2.Output.W
        except ZeroDivisionError: r2 = 0
        try: ra12 = 1 / a12
        except ZeroDivisionError: ra12 = 0
        try: ra20 = 1 / a20
        except ZeroDivisionError: ra20 = 0
        try: ra01 = 1 / a01 if a01 else 0
        except ZeroDivisionError: ra01 = 0

        # iterate over all pixels in bounding box
        for y in range(y0, y1):
            d = 0.0 # var d float64
            d0 = -w00 * ra12
            d1 = -w01 * ra20
            d2 = -w02 * ra01
            if w00 < 0 and d0 > d:
                d = d0
            if w01 < 0 and d1 > d:
                d = d1
            if w02 < 0 and d2 > d:
                d = d2
            d = float(int(d))
            if d < 0:
                # occurs in pathological cases
                d = 0
            w0 = w00 + a12*d
            w1 = w01 + a20*d
            w2 = w02 + a01*d
            wasInside = False
            for x in range(x0+int(d), x1):
                b0 = w0 * ra
                b1 = w1 * ra
                b2 = w2 * ra
                w0 += a12
                w1 += a20
                w2 += a01
                # check if inside triangle
                if b0 < 0 or b1 < 0 or b2 < 0:
                    if wasInside:
                        break
                    continue
                wasInside = True
                # check depth buffer for early abort
                i = y*dc.Width + x
                if i < 0 or i >= len(dc.DepthBuffer):
                    # TODO: clipping roundoff error; fix
                    # TODO: could also be from fat lines going off screen
                    continue
                #info.TotalPixels += 1
                z = b0*s0.Z + b1*s1.Z + b2*s2.Z
                bz = z + dc.DepthBias
                if dc.ReadDepth and bz > dc.DepthBuffer[i]: # safe w/out lock?
                    continue
                # perspective-correct interpolation of vertex data
                b = VectorW(b0 * r0, b1 * r1, b2 * r2, 0)
                try: b.W = 1 / (b.X + b.Y + b.Z)
                except ZeroDivisionError: b.W = 0
                v = InterpolateVertexes(v0, v1, v2, b)
                # invoke fragment shader
                color = dc.Shader.Fragment(v)
                #print v,v.Texture,color.__dict__
                if color == Discard:
                    continue
                # update buffers atomically
                #lock = dc.locks[(x+y)&255]
                #lock.Lock()
                # check depth buffer again
                if bz <= dc.DepthBuffer[i] or not dc.ReadDepth:
                    info.UpdatedPixels += 1
                    if dc.WriteDepth:
                        # update depth buffer
                        dc.DepthBuffer[i] = z
                    if dc.WriteColor:
                        # update color buffer
                        #print color.NRGBA(), dc.AlphaBlend
                        if dc.AlphaBlend and color.A < 1:
                            sr, sg, sb, sa = color.NRGBA()
                            a = (255 - sa)
                            dr,dg,db,da = dc.ColorBuffer[x, y]
                            dr = int(dr*a/255.0 + sr)
                            dg = int(dg*a/255.0 + sg)
                            db = int(db*a/255.0 + sb)
                            da = int(da*a/255.0 + sa)
                            dc.ColorBuffer[x, y] = (dr,dg,db,da)
##                            with dc.ColorBuffer.data.get_lock():
##                                dc.ColorBuffer[x, y] = (dr,dg,db,da)
                        else:
                            dc.ColorBuffer[x, y] = color.NRGBA()
##                            with dc.ColorBuffer.data.get_lock():
##                                dc.ColorBuffer[x, y] = color.NRGBA()
                #lock.Unlock()
            w00 += b12
            w01 += b20
            w02 += b01
        return info

    def line(dc, v0, v1, s0, s1):
        n = s1.Sub(s0).Perpendicular().MulScalar(dc.LineWidth / 2)
        s0 = s0.Add(s0.Sub(s1).Normalize().MulScalar(dc.LineWidth / 2))
        s1 = s1.Add(s1.Sub(s0).Normalize().MulScalar(dc.LineWidth / 2))
        s00 = s0.Add(n)
        s01 = s0.Sub(n)
        s10 = s1.Add(n)
        s11 = s1.Sub(n)
        info1 = dc.rasterize(v1, v0, v0, s11, s01, s00)
        info2 = dc.rasterize(v1, v1, v0, s10, s11, s00)
        return info1.Add(info2)

    def wireframe(dc, v0, v1, v2, s0, s1, s2):
        info1 = dc.line(v0, v1, s0, s1)
        info2 = dc.line(v1, v2, s1, s2)
        info3 = dc.line(v2, v0, s2, s0)
        return info1.Add(info2).Add(info3)

    def drawClippedLine(dc, v0, v1):
        # normalized device coordinates
        ndc0 = v0.Output.DivScalar(v0.Output.W).Vector()
        ndc1 = v1.Output.DivScalar(v1.Output.W).Vector()

        # screen coordinates
        s0 = dc.screenMatrix.MulPosition(ndc0)
        s1 = dc.screenMatrix.MulPosition(ndc1)

        # rasterize
        return dc.line(v0, v1, s0, s1)

    def drawClippedTriangle(dc, v0, v1, v2):
        # normalized device coordinates
        ndc0 = v0.Output.DivScalar(v0.Output.W).Vector()
        ndc1 = v1.Output.DivScalar(v1.Output.W).Vector()
        ndc2 = v2.Output.DivScalar(v2.Output.W).Vector()

        # back face culling
        a = (ndc1.X-ndc0.X)*(ndc2.Y-ndc0.Y) - (ndc2.X-ndc0.X)*(ndc1.Y-ndc0.Y)
        if a < 0:
            v0, v1, v2 = v2, v1, v0
            ndc0, ndc1, ndc2 = ndc2, ndc1, ndc0
        if dc.Cull == CullFront:
            a = -a
        if dc.FrontFace == FaceCW:
            a = -a
        if dc.Cull != CullNone and a <= 0:
            return RasterizeInfo()

        # screen coordinates
        s0 = dc.screenMatrix.MulPosition(ndc0)
        s1 = dc.screenMatrix.MulPosition(ndc1)
        s2 = dc.screenMatrix.MulPosition(ndc2)

        # rasterize
        if dc.Wireframe:
            return dc.wireframe(v0, v1, v2, s0, s1, s2)
        else:
            return dc.rasterize(v0, v1, v2, s0, s1, s2)

    def DrawLine(dc, t):
        # invoke vertex shader
        v1 = dc.Shader.Vertex(t.V1)
        v2 = dc.Shader.Vertex(t.V2)

        if v1.Outside() or v2.Outside():
            # clip to viewing volume
            line = ClipLine(NewLine(v1, v2))
            if line != None:
                return dc.drawClippedLine(line.V1, line.V2)
            else:
                return RasterizeInfo()
        else:
            # no need to clip
            return dc.drawClippedLine(v1, v2)

    def DrawTriangle(dc, t):
        # invoke vertex shader
        v1 = dc.Shader.Vertex(t.V1)
        v2 = dc.Shader.Vertex(t.V2)
        v3 = dc.Shader.Vertex(t.V3)

        if v1.Outside() or v2.Outside() or v3.Outside():
            # clip to viewing volume
            triangles = ClipTriangle(NewTriangle(v1, v2, v3))
            result = RasterizeInfo()
            for t in triangles:
                info = dc.drawClippedTriangle(t.V1, t.V2, t.V3)
                result = result.Add(info)
            return result
        else:
            # no need to clip
            return dc.drawClippedTriangle(v1, v2, v3)

    def DrawLines(dc, lines):
        # normal way (one process)
        result = RasterizeInfo()
        thresh = 1000
        for i,t in enumerate(lines):
            if i>thresh:
                print 'line',i
                thresh += 1000
            info = dc.DrawLine(t)
            result = result.Add(info)

        print 'finished'
        
        return result

    def DrawTriangles(dc, triangles):



        
        cpus = multiprocessing.cpu_count()
        chunksize = len(triangles) // cpus
        chunksize += 1

        print 'processing a total of {} triangles across {} cpu cores, in chunks of {}...'.format(len(triangles), cpus, chunksize)

        #print 'pickling items for multiprocessing...'
        #picklable = [t.Picklable() for t in triangles]
##        dcpickle = dc.Picklable()
####        print dcpickle.keys()
####        for k in dcpickle.keys():
####            print k,getattr(dc,k),dcpickle[k]
####        print dc.screenMatrix.__dict__
####        print dc.Shader.Matrix.__dict__
####        print dcpickle['screenMatrix']
####        print dcpickle['Shader']['Matrix']
##        #dcpickle['ColorBuffer'] = [val for rgba in dcpickle['ColorBuffer'] for val in rgba]
##        print type(dcpickle['ColorBuffer']), repr(dcpickle['ColorBuffer'])[:100]
        #imarray = multiprocessing.Array('B', dcpickle['ColorBuffer']) # efficient sharable array of flattened 1-byte 255 color values
        #dcpickle['ColorBuffer'] = imarray
        
##        vectors = multiprocessing.sharedctypes.RawArray('f', [val for t in triangles for v in (t.V1,t.V2,t.V3) for val in [v.Position.X,v.Position.Y,v.Position.Z,
##                                                                                                                           v.Normal.X,v.Normal.Y,v.Normal.Z,
##                                                                                                                           v.Texture.X,v.Texture.Y,v.Texture.Z,
##                                                                                                                           v.Color.R,v.Color.G,v.Color.B,v.Color.A,
##                                                                                                                           v.Output.X,v.Output.Y,v.Output.Z,v.Output.W,
##                                                                                                                           ]] )
##        print 'flat',len(vectors)
        
        triangles = multiprocessing.sharedctypes.RawArray(Triangle, triangles)
        
##        for k,v in dcpickle.items():
##            print k,repr(v)[:100]
##        print dcpickle['Shader']
        #dcpickle.pop('DepthBuffer')
        sharedData = dict(dc=dc, triangles=triangles) #,picklable=picklable)
        pool = multiprocessing.Pool(cpus, initSharedData, (sharedData,) )
##        tasks = pool.map(pooled_draw_triangles, picklable, chunksize=chunksize)
##        print tasks
##        tasks = [multiprocessing.Process(target=pooled_draw_triangles, args=(dcpickle, picklable[i:i+chunksize]))
##                 for i in range(0, len(triangles), chunksize)]
        tasks = [pool.apply_async(pooled_draw_triangles, args=(range(ti, ti+chunksize),))#picklable[i:i+chunksize],))
                 for ti in range(0, len(triangles), chunksize)]
        
##        for task in tasks:
##            print 'starting',task
##            task.daemon = True
##            task.start()
##            print 'hmmm'
        
        result = RasterizeInfo()

##        pool.close()
##        pool.join()
        
##        while tasks:
##            for t in tasks:
##                if t.ready():
##                    print '%s finished' % t
##                    tasks.pop(tasks.index(t))
                    
        for task in tasks:
            resdc = task.get()
            #resdc = Context.FromDict(resdc)
            #resdc.Image().show()
            print 'finished',task
            #tot,updated = task
            #res = RasterizeInfo(tot, updated)
            #result = result.Add(res)



            

##        import PIL.Image
##        im = PIL.Image.new('RGBA', (dc.Width,dc.Height))
##        rgbs = [tuple(imarray[i:i+4]) for i in range(0, len(imarray), 4)]
##        im.putdata(rgbs)
##        im.show()

##        global func
##        def func(indexes):
##            # necessary for multiprocessing, func accessible from top-level
##            result = RasterizeInfo()
##            print 'index %s to %s' % (indexes[0],indexes[-1])
##            #sys.stdout.flush()
##            for i in indexes:
##                t = triangles[i]
##                info = dc.DrawTriangle(t)
##                result = result.Add(info)
##            print 'cpu core finished'
##            #sys.stdout.flush()
##            return result.TotalPixels, result.UpdatedPixels
##
##        indexes = range(len(triangles))
##        print indexes[:10], indexes[-10:]
##
##        pool = multiprocessing.Pool(cpus)
##        tasks = pool.map(func, indexes, chunksize=chunksize)
##        print tasks
##        tasks = [multiprocessing.Process(target=func, args=(indexes[i:i+chunksize],))
##                 for i in indexes[::chunksize]]
##        for task in tasks:
##            print task
##            task.daemon = True
##            task.start()
##        
##        result = RasterizeInfo()
##        for task in tasks:
##            task.join()
##            print task
##            #tot,updated = task
##            #res = RasterizeInfo(tot, updated)
##            #result = result.Add(res)





        # normal way (one process)
##        result = RasterizeInfo()
##        thresh = 1000
##        for i,t in enumerate(triangles):
##            if i>thresh:
##                print 'tri',i
##                thresh += 1000
##            info = dc.DrawTriangle(t)
##            result = result.Add(info)



            
        print 'finished'
        
        return result

    def DrawMesh(dc, mesh):
        info1 = dc.DrawTriangles(mesh.Triangles)
        info2 = dc.DrawLines(mesh.Lines)
        return info1.Add(info2)

