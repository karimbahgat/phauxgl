
from __future__ import division

import math

from .color import Color, Discard, White
from .matrix import Matrix
from .vector import V

# SolidColorShader renders with a single, solid color.
def NewSolidColorShader(matrix, color):
    return SolidColorShader(matrix, color)

class SolidColorShader:
    def __init__(self, Matrix, Color):
        self.Matrix = Matrix
        self.Color = Color

    def Vertex(shader, v):
        v.Output = shader.Matrix.MulPositionW(v.Position)
        return v

    def Fragment(shader, v):
        return shader.Color

# TextureShader renders with a texture and no lighting.
def NewTextureShader(matrix, texture):
    return TextureShader(matrix, texture)

class TextureShader:
    def __init__(self, Matrix, Texture):
        self.Matrix = Matrix
        self.Texture = Texture
        
    def Vertex(shader, v):
        v.Output = shader.Matrix.MulPositionW(v.Position)
        return v

    def Fragment(shader, v):
        return shader.Texture.BilinearSample(v.Texture.X, v.Texture.Y)

# PhongShader implements Phong shading with an optional texture.

def NewPhongShader(matrix, lightDirection, cameraPosition):
      ambient = Color(0.2, 0.2, 0.2, 1)
      diffuse = Color(0.8, 0.8, 0.8, 1)
      specular = Color(1, 1, 1, 1)
      return PhongShader(
              matrix, lightDirection, cameraPosition,
              Discard, ambient, diffuse, specular, None, 32)
    
class PhongShader:
    def __init__(self,
                  Matrix,
                  LightDirection,
                  CameraPosition,
                  ObjectColor,
                  AmbientColor,
                  DiffuseColor,
                  SpecularColor,
                  Texture,
                  SpecularPower):
                
        self.Matrix = Matrix
        self.LightDirection = LightDirection
        self.CameraPosition = CameraPosition 
        self.ObjectColor = ObjectColor
        self.AmbientColor = AmbientColor
        self.DiffuseColor = DiffuseColor
        self.SpecularColor = SpecularColor
        self.Texture = Texture
        self.SpecularPower = SpecularPower

##    def Picklable(shader):
##        sh = shader
##        LightDirection,CameraPosition,ObjectColor,AmbientColor,DiffuseColor,SpecularColor,Texture,SpecularPower = sh.LightDirection,sh.CameraPosition,sh.ObjectColor,sh.AmbientColor,sh.DiffuseColor,sh.SpecularColor,sh.Texture,sh.SpecularPower
##        pdict = dict(
##                    Matrix = dict([(k,getattr(shader.Matrix,k))
##                                for k in 'X00 X01 X02 X03 X10 X11 X12 X13 X20 X21 X22 X23 X30 X31 X32 X33'.split() ]),
##                    LightDirection = LightDirection.Picklable() if LightDirection else None,
##                    CameraPosition = CameraPosition.Picklable() if CameraPosition else None,
##                    ObjectColor = (ObjectColor.R, ObjectColor.G, ObjectColor.B, ObjectColor.A),
##                    AmbientColor = (AmbientColor.R, AmbientColor.G, AmbientColor.B, AmbientColor.A),
##                    DiffuseColor = (DiffuseColor.R, DiffuseColor.G, DiffuseColor.B, DiffuseColor.A),
##                    SpecularColor = (SpecularColor.R, SpecularColor.G, SpecularColor.B, SpecularColor.A),
##                    Texture = None,#shader.Texture
##                    SpecularPower = SpecularPower
##                    )
##        return pdict
##
##    @staticmethod
##    def FromDict(pdict):
##        pdict.update(    LightDirection = V(**pdict['LightDirection']),
##                          CameraPosition = V(**pdict['CameraPosition']),
##                          ObjectColor = Color(*pdict['ObjectColor']),
##                          AmbientColor = Color(*pdict['AmbientColor']),
##                          DiffuseColor = Color(*pdict['DiffuseColor']),
##                          SpecularColor = Color(*pdict['SpecularColor']),
##                          #Texture...
##                          SpecularPower = pdict['SpecularPower'],
##                          )
##        pdict['Matrix'] = Matrix(*[pdict['Matrix'][k]
##                                         for k in 'X00 X01 X02 X03 X10 X11 X12 X13 X20 X21 X22 X23 X30 X31 X32 X33'.split() ])
##        shader = PhongShader(**pdict)
##        return shader

    def Vertex(shader, v):
        v.Output = shader.Matrix.MulPositionW(v.Position)
        return v

    def Fragment(shader, v):
        light = shader.AmbientColor
        color = v.Color
        if shader.ObjectColor != Discard:
            color = shader.ObjectColor
        if shader.Texture != None:
            color = shader.Texture.BilinearSample(v.Texture.X, v.Texture.Y)
        diffuse = max(v.Normal.Dot(shader.LightDirection), 0)
        light = light.Add(shader.DiffuseColor.MulScalar(diffuse))
        if diffuse > 0 and shader.SpecularPower > 0:
            camera = shader.CameraPosition.Sub(v.Position).Normalize()
            reflected = shader.LightDirection.Negate().Reflect(v.Normal)
            specular = max(camera.Dot(reflected), 0)
            if specular > 0:
                specular = math.pow(specular, shader.SpecularPower)
                light = light.Add(shader.SpecularColor.MulScalar(specular))
        return color.Mul(light).Min(White).Alpha(color.A)


