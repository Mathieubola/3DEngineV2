from tkinter import Tk, Canvas
from objects import *
import math, time, threading

printed_shape = []

objects = []

ftheta = 0

class window:
    def __init__(self, title, size, fov = 90):
        self.x = int(size.split('x')[0])
        self.y = int(size.split('x')[1])

        # Projection matrice
        self.zfar = 1000 # Distance de rendu max
        self.znear = 0.1 # Distance de rendu min
        self.fov = fov # FOV

        self.a = self.y / self.x # Aspect ratio
        self.t = 2 * ( self.x / 2 ) / self.zfar #Theta
        self.fovRad = 1 / math.tan( self.fov * 0.5 / 180 * math.pi )
        # self.q = zmax / ( zmax - zmin )

        self.projMat = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.projMat[0][0] = self.a * self.fovRad
        self.projMat[1][1] = self.fovRad
        self.projMat[2][2] = self.zfar / ( self.zfar - self.znear)
        self.projMat[3][2] = ( -self.zfar * self.znear ) / ( self.zfar - self.znear )
        self.projMat[2][3] = 1

        self.fen = Tk()
        self.fen.geometry(size)
        self.fen.title(title)

        self.can = Canvas(self.fen, width=self.x, height=self.y, bg='white')
        self.can.pack()
    
    def update(self):
        global ftheta

        while 1:
            #Delete all
            for i in printed_shape:
                self.can.delete(i)
            
            ftheta += 0.1
            
            # Draw triangles
            for i in objects:
                mesh = i.getMesh()
                for trisOrigin in mesh.getTris():

                    trisOrigin = trisOrigin.getCo()
                    trisRotX = []
                    trisRotZ = []
                    trisTrans = []
                    tri = []

                    trisRotZ.append( self.matrixMult( trisOrigin[0], self.matRotZ(ftheta) ) )
                    trisRotZ.append( self.matrixMult( trisOrigin[1], self.matRotZ(ftheta) ) )
                    trisRotZ.append( self.matrixMult( trisOrigin[2], self.matRotZ(ftheta) ) )

                    trisRotX.append( self.matrixMult( trisRotZ[0], self.matRotX(ftheta * 0.5) ) )
                    trisRotX.append( self.matrixMult( trisRotZ[1], self.matRotX(ftheta * 0.5) ) )
                    trisRotX.append( self.matrixMult( trisRotZ[2], self.matRotX(ftheta * 0.5) ) )

                    trisTrans = trisRotX
                    #Translate by 3 on the Z axis
                    trisTrans[0][2] += 3
                    trisTrans[1][2] += 3
                    trisTrans[2][2] += 3

                    #Projection
                    tri.append( self.matrixMult( trisTrans[0], self.projMat ) )
                    tri.append( self.matrixMult( trisTrans[1], self.projMat ) )
                    tri.append( self.matrixMult( trisTrans[2], self.projMat ) )

                    #Arrengment for the windows coordonate
                    tri[0][0] += 1
                    tri[0][1] += 1
                    tri[1][0] += 1
                    tri[1][1] += 1
                    tri[2][0] += 1
                    tri[2][1] += 1

                    tri[0][0] *= 0.5 * self.x
                    tri[0][1] *= 0.5 * self.y
                    tri[1][0] *= 0.5 * self.x
                    tri[1][1] *= 0.5 * self.y
                    tri[2][0] *= 0.5 * self.x
                    tri[2][1] *= 0.5 * self.y

                    self.printTris(tri)
            
            time.sleep(0.016)
    
    def loop(self):
        threading.Thread(target=self.update).start()
            
    def add3DObj(self, obj):
        objects.append(obj)
    
    def addCube(self):
        objects.append(
            object("Cube", mesh([
                #South
                tri([0, 0, 0], [0, 1, 0], [1, 1, 0]),
                tri([0, 0, 0], [1, 1, 0], [1, 0, 0]),
                #East
                tri([1, 0, 0], [1, 1, 0], [1, 1, 1]),
                tri([1, 0, 0], [1, 1, 1], [1, 0, 1]),
                #North
                tri([1, 0, 1], [1, 1, 1], [0, 1, 1]),
                tri([1, 0, 1], [0, 1, 1], [0, 0, 1]),
                #West
                tri([0, 0, 1], [0, 1, 1], [0, 1, 0]),
                tri([0, 0, 1], [0, 1, 0], [0, 0, 0]),
                #Top
                tri([0, 1, 0], [0, 1, 1], [1, 1, 1]),
                tri([0, 1, 0], [1, 1, 0], [1, 1, 0]),
                #Bottom
                tri([1, 0, 1], [0, 0, 1], [0, 0, 0]),
                tri([1, 0, 1], [0, 0, 0], [1, 0, 0]),
            ]))
        )
    
    def matrixMult(self, i, m):
        mat = [0, 0, 0]

        mat[0] = i[0] * m[0][0] + i[1] * m[1][0] + i[2] * m[2][0] + m[3][0]
        mat[1] = i[0] * m[0][1] + i[1] * m[1][1] + i[2] * m[2][1] + m[3][1]
        mat[2] = i[0] * m[0][2] + i[1] * m[1][2] + i[2] * m[2][2] + m[3][2]
        w      = i[0] * m[0][3] + i[1] * m[1][3] + i[2] * m[2][3] + m[3][3]

        if w != 0:
            mat[0] /= w
            mat[1] /= w
            mat[2] /= w
        
        return mat
    
    def matRotZ(self, theta):
        #Matrice de rotation
        return [[math.cos(theta) , math.sin(theta), 0, 0],
                [-math.sin(theta), math.cos(theta), 0, 0],
                [0               , 0              , 1, 0],
                [0               , 0              , 0, 1]]
    
    def matRotX(self, theta):
        return [[1, 0, 0, 0],
                [0, math.cos(theta), math.sin(theta), 0],
                [0, -math.sin(theta), math.cos(theta), 0],
                [0, 0, 0, 1]]
    
    def printTris(self, co):
        printed_shape.append(self.can.create_line(co[0][0], co[0][1], co[1][0], co[1][1], fill='black'))
        printed_shape.append(self.can.create_line(co[1][0], co[1][1], co[2][0], co[2][1], fill='black'))
        printed_shape.append(self.can.create_line(co[2][0], co[2][1], co[0][0], co[0][1], fill='black'))

    def mainLoop(self):
        self.can.mainloop()
