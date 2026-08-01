# ℤøŋεş
####################
from scene_builder import *
####################
# Tiles
#NOPATH=-2
#EMPTY=-1
#ENTRY=1
#EXIT=2
#PATH=3
# Zone 1- Town
TOWN=[[3,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],\
      [3,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],\
      [3,3,3,-1,-1,-1,-1,-1,-1,-1,-1,-1],\
      [-1,-1,3,1,3,3,-1,-1,-1,-1,-1,-1],\
      [-1,-1,-1,-1,-1,3,-1,-1,-1,-1,-1,-1],\
      [-1,-1,-1,-1,-1,3,-1,-1,-1,-1,-1,-1],\
      [-1,-1,-1,-1,-1,3,-1,-1,-1,-1,-1,-1],\
      [-1,-1,-1,-1,3,3,-1,-1,-1,-1,-1,-1],\
      [-1,-1,-1,-1,3,-1,-1,-1,-1,-1,-1,-1],\
      [-1,-1,-1,-1,3,3,3,3,3,3,-1,-1],\
      [-1,-1,-1,-1,-1,-1,-1,-1,-1,3,3,3],\
      [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,3,2]]

class Zone:
  def __init__(self,zone,x=0,y=0,cSz=30):
    self.x=x
    self.y=y
    self.rows=len(zone)
    self.columns=len(zone[0])
    self.cellSz=cSz
    self.height=self.rows*self.cellSz
    self.width=self.columns*self.cellSz
    self.grid=matrixToGrid(zone,self.cellSz,\
           self.x,self.y,[EMPTY,[0,110,0],\
           PATH,[80,80,80],ENTRY,[0,220,0],\
           EXIT,[220,0,0]])
    self.draw_data=gridToImage(splitPathVtcs(\
                getCritVertices(zone,self.grid),\
                self.grid),self.grid)
    self._entry=[]
    self._exit=[]
  
  def draw(self):
    for line in self.draw_data:
      eval(line)
  
  @property
  def entry(self): 
    return self._entry
  @entry.getter 
  def entry(self):
    for row in self.grid:
      for cell in row:
        if cell["type"]==ENTRY:
          return cell
    return  
  @property
  def exit(self): 
    return self._exit
  @exit.getter 
  def exit(self):
    for row in self.grid:
      for cell in row:
        if cell["type"]==EXIT:
          return cell
    return
