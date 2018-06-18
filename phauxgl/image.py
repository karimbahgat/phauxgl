
import multiprocessing

import PIL, PIL.Image



class Image:
    def __init__(self, width, height):
        self.Width = width
        self.Height = height
        self.data = multiprocessing.RawArray('B', width*height*4)

    def __getitem__(self, xy):
        x,y = xy
        i = (self.Width * y + x) * 4
        i = int(i)
        return self.data[i:i+4]

    def __setitem__(self, xy, val):
        x,y = xy
        i = (self.Width * y + x) * 4
        i = int(i)
        self.data[i:i+4] = val

    @staticmethod
    def open(filepath):
        pim = PIL.Image.open(filepath)
        im = Image(*pim.size)
        im.data = multiprocessing.RawArray('B', [v for rgb in pim.getdata() for val in rgb])
        return im

    def clear(self, color):
        assert len(color) == 4
        data = self.data
        for i in range(0, len(data), 4):
            data[i:i+4] = color

    def PIL(self):
        data = self.data
        im = PIL.Image.new('RGBA', (self.Width,self.Height))
        im.putdata([tuple(data[i:i+4]) for i in range(0, len(data), 4)])
        return im

    def save(self, filepath):
        im = self.PIL()
        im.save(filepath)



