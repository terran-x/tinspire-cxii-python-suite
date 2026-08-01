# 3D Objects
#================================
from math import *
from ti_draw import *
from sys import *
from matrices import *
#================================
STR_HT=string_size("abc")[1]

class Polygon:
  def __init__(self,vertices,edges,position=[0,0,0],rotation=[0,0,0],colour=[0,0,0]):
    self.vertices=vertices
    self.vertices0=self.vertices.copy()
    self.edges=edges
    self.lXYZ=tpose([[1,0,0],[0,1,0],[0,0,1]])
    self.type=""
    self.colour=colour
    self.position=position
    self._rotation=rotation
    self._x=position[0]
    self._y=position[1]
    self._z=position[2]
    self._size=1
  
  # Handles intrinsic/extrinsic rotations.
  def rotate(self,direction,angle,extrinsic=True):
    c=cos(angle)
    s=sin(angle)
    tmpV=[]
    vrtcs=[]
    rX=[[1,0,0],[0,c,-s],[0,s,c]]
    rY=[[c,0,s],[0,1,0],[-s,0,c]]
    rZ=[[c,-s,0],[s,c,0],[0,0,1]]
    rDir=[rX,rY,rZ]
    if extrinsic:
      self.lXYZ=mtxMult(rDir[direction],self.lXYZ)
      self.vertices=tpose(mtxMult(rDir[direction],tpose(self.vertices)))
    else:
      self.lXYZ=tpose(mtxMult(rDir[direction],tpose(self.lXYZ)))
      for idx in range(len(self.vertices)):
        self.vertices[idx]=mtxMult(self.lXYZ,self.vertices0[idx])
  
  # Handles linear translation.
  def translate(self,disp,dir):
    self.position[dir]+=disp
  
  # Maps vertices to edge indexes.
  def map_edges(self):
    vertices=[]
    vrtcMap=[]
    for indexes in self.edges:
      for idx in indexes:
        vertices.append(self.vertices[idx-1])
      vrtcMap.append(vertices)
      vertices=[]
    return vrtcMap
  
  # Draw polygon
  def draw(self):
    xList=[]
    yList=[]
    for vertices in self.map_edges():
      for vertice in vertices:
        xList.append(vertice[0]+self.x)
        yList.append(vertice[1]+self.y)
      set_color(self.colour[0],self.colour[1],self.colour[2])
      draw_poly(xList,yList)
      xList.clear()
      yList.clear()
    if self.type=="axes":
      self.draw_lbls()
  
  # Rotation, size and position properties
  @property
  def rotation(self):
    return self._rotation
  @rotation.getter
  def rotation(self):
    # Direction tangents
    rX=atan2(round(self.lXYZ[1][2],8),round(self.lXYZ[1][1],6))#round(self.lXYZ[2][1],8),round(self.lXYZ[2][2],8))
    rY=-atan2(round(self.lXYZ[2][0],8),round(self.lXYZ[2][2],8))
    rZ=atan2(round(self.lXYZ[0][1],8),round(self.lXYZ[0][0],8))
    return [rX,rY,rZ]
  
  @property
  def size(self):
    return self._size
  @size.setter
  def size(self,size):
    for vtc in range(len(self.vertices)):
      for idx in range(len(self.vertices[vtc])):
        self.vertices[vtc][idx]*=size/self._size
        self.vertices0[vtc][idx]*=size/self._size
    self._size=size
    return self._size
  
  @property
  def x(self):
    return self._x
  @x.getter
  def x(self):
    return self.position[0]
  @property
  def y(self):
    return self._y
  @y.getter
  def y(self):
    return self.position[1]
  @property
  def z(self):
    return self._z
  @z.setter
  def z(self):
    return self.position[2]

class Cube(Polygon):
  def __init__(self,size,position=[0,0,0],rotation=[0,0,0],colour=[0,0,0]):
    Polygon.__init__(self,[[size*.5,size*.5,size*.5],[size*.5,size*.5,-size*.5],[-size*.5,size*.5,-size*.5],[-size*.5,size*.5,size*.5],[size*.5,-size*.5,size*.5],[size*.5,-size*.5,-size*.5],[-size*.5,-size*.5,-size*.5],[-size*.5,-size*.5,size*.5]]\
    ,[[1,2,3,4,1,5,6,7,8,5],[2,6],[3,7],[4,8]],position,rotation,colour)
    self._size=size
    self.scale=1
    self.type="cube"

class Axes(Polygon):
  def __init__(self,size=160,position=[0,0,0],rotation=[0,0,0],colour=[0,0,0],xlbl="x",ylbl="y",zlbl="z"):
    Polygon.__init__(self,[[size*.5,0,0],[-size*.5,0,0],[0,size*.5,0],[0,-size*.5,0],[0,0,size*.5],[0,0,-size*.5],[size*.5+size*0.05,0,0],[0,size*.5+size*0.05,0],[0,0,size*.5+size*0.05]],[[1,2],[3,4],[5,6]],position,rotation,colour)
    self._size=size
    self.xLbl=xlbl
    self.yLbl=ylbl
    self.zLbl=zlbl
    self.type="axes"
  
  def draw_lbls(self):
    set_color(255,0,0)
    draw_text(self.vertices[6][0]+self.x,self.vertices[6][1]+self.y-.5*STR_HT,self.xLbl)
    draw_text(self.vertices[7][0]+self.x,self.vertices[7][1]+self.y-.5*STR_HT,self.yLbl)
    draw_text(self.vertices[8][0]+self.x,self.vertices[8][1]+self.y-.5*STR_HT,self.zLbl)
    set_color(0,0,0)
