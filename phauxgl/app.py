
from .mesh import Mesh
from .matrix import LookAt
from .vector import V
import tk2
import Tkinter as tk
import pyagg as pa


class App(tk2.Tk):
    def __init__(self, context):
        tk2.Tk.__init__(self)
        self.context = context
        self.meshes = []

        self.scale  = 1
        self.fovy   = 30
        self.near   = 1
        self.far    = 10
    
        _top = tk2.Label(self, text="PhauxGL 3D Viewer")
        _top.pack(side="top", fill="x")

        _main = tk2.Frame(self)
        _main.pack(side="top", fill="x")

        self.canvas = canvas = tk.Canvas(_main,
                                          width=context.Width,
                                          height=context.Height)
        canvas.pack(side="left", fill="both")

        self._imgid = self.canvas.create_image((0,0), anchor='nw')

        self.right = tk2.Frame(_main, width="300")
        self.right.pack(side="right", fill="both")

        def move_eye(event):
            print event.x, event.y
            x,y = self.xyimg.pixel2coord(event.x, event.y)
            self.eye.X, self.eye.Y = x, y
            self.render()

        self.xymap = tk2.Label(self.right, text="XY Map:")
        self.xymap.pack()
        self.xymap.bind('<Button>', move_eye)

    def define_scene(self, eye, center, up, light=None):
        self.eye = eye
        self.center = center
        self.up = up
        self.light = light
        
    def add_mesh(self, mesh):
        self.meshes.append(mesh)

    def render(self):
        import PIL.Image, PIL.ImageTk

        # setup matrix
        aspect = float(self.context.Width) / float(self.context.Height)
        matrix = LookAt(self.eye, self.center, self.up).Perspective(self.fovy, aspect, self.near, self.far)
        self.context.Shader.Matrix = matrix

        # render
        self.context.ClearColorBuffer()
        self.context.ClearDepthBuffer()
        for mesh in self.meshes:
            self.context.DrawMesh(mesh)
        self._img = PIL.ImageTk.PhotoImage( self.context.Image().PIL() )
        self.canvas.itemconfig(self._imgid, image=self._img)

        # xy map
        mins = [m.BoundingBox().Min for m in self.meshes]
        mins = [(mn.X,mn.Y,mn.Z) for mn in mins]
        minxs,minys,minzs = zip(*mins)
        minxs = list(minxs) + [self.eye.X, self.center.X, self.light.X]
        minys = list(minys) + [self.eye.Y, self.center.Y, self.light.Y]
        xmin,ymin,zmin = min(minxs), min(minys), min(minzs)

        maxs = [m.BoundingBox().Max for m in self.meshes]
        maxs = [(mn.X,mn.Y,mn.Z) for mn in maxs]
        maxxs,maxys,maxzs = zip(*maxs)
        maxxs = list(maxxs) + [self.eye.X, self.center.X, self.light.X]
        maxys = list(maxys) + [self.eye.Y, self.center.Y, self.light.Y]
        xmax,ymax,zmax = max(maxxs), max(maxys), min(maxzs)

        self.xyimg = xyimg = pa.Canvas(300, 300)
        xyimg.custom_space(xmin,ymax,xmax,ymin, lock_ratio=True)
        xyimg.zoom_out(1.5)
        xmin,ymax,xmax,ymin = xyimg.coordspace_bbox
        xyimg.zoom_out(1.5)

        # objects
        for m in self.meshes:
            bbox = m.BoundingBox()
            bbox = [bbox.Min.X, bbox.Min.Y, bbox.Max.X, bbox.Max.Y]
            xyimg.draw_box(bbox=bbox, fillcolor=(0,255,0), outlinewidth="1px")

        # eye
        xyimg.draw_circle((self.eye.X,self.eye.Y), fillsize="5px", fillcolor=(0,0,0,255))

        # center
        xyimg.draw_circle((self.center.X,self.center.Y), fillsize="5px", fillcolor=(255,0,0))

        # light
        xyimg.draw_circle((self.light.X,self.light.Y), fillsize="5px", fillcolor=(255,255,0))

        xyimg.draw_axis('x', xmin, xmax, 0)
        xyimg.draw_axis('y', ymin, ymax, 0)
        
        self.xymap['image'] = self.xymap._img = xyimg.get_tkimage()

    def run(self):
        self.render()
        self.mainloop()

