from objects import *
import math, time, threading, cv2
import numpy as np

printed_shape = []

objects = []

ftheta = 0

class window:
    def __init__(self, title, size, fov = 90):
        self.x = int(size.split('x')[0])
        self.y = int(size.split('x')[1])
        self.title = title
        self.fps = 60
        self.framedelay = 16

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
    
    def update(self):
        global ftheta
        previousTime = time.time()

        while 1:
            #Delete all
            self.drawMat = np.zeros((self.y, self.x, 3), dtype=np.uint8)
            
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
            
            cv2.imshow(self.title, self.drawMat)

            if cv2.waitKey(int(self.framedelay)) & 0xFF == ord('q'):
                break
        

    
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
        self.drawLine(co[0][0], co[0][1], co[1][0], co[1][1])
        self.drawLine(co[1][0], co[1][1], co[2][0], co[2][1])
        self.drawLine(co[2][0], co[2][1], co[0][0], co[0][1])

    def drawLine(self, x1, y1, x2, y2, size = 1, color = (255, 255, 255)):
        dx = x2 - x1
        dy = y2 - y1
        dx1 = abs(dx)
        dy1 = abs(dy)
        px = 2 * dy1 - dx1
        py = 2 * dx1 - dy1
        if (dy1 <= dx1):
            if (dx >= 0):
                x = x1
                y = y1
                xe = x2
            else:
                x = x2
                y = y2
                xe = x1
            self.drawMat[int(y)][int(x)] = color
            i = -1
            while (x < xe):
                i += 1
                x += 1
                if (px < 0):
                    px = px + 2 * dy1
                else:
                    if ((dx < 0 and dy < 0) or (dx > 0 and dy > 0)):
                        y += 1
                    else:
                        y -= 1
                    px = px + 2 * (dy1 - dx1)
                self.drawMat[int(y)][int(x)] = color
        else:
            if (dy >= 0):
                x = x1
                y = y1
                ye = y2
            else:
                x = x2
                y = y2
                ye = y1
            self.drawMat[int(y)][int(x)] = color
            i = -1
            while (y < ye):
                i += 1
                y += 1
                if (py < 0):
                    py = py + 2 * dx1
                else:
                    if ((dx < 0 and dy < 0) or (dx > 0 and dy > 0)):
                        x += 1
                    else:
                        x -= 1
                    py = py + 2 * (dx1 - dy1)
                self.drawMat[int(y)][int(x)] = color

