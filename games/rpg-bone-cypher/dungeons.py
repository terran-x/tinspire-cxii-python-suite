# Ðμŋğεøŋş
####################
from scene_builder import *
####################
class Dungeon:
  def __init__(self,r,c,x=0,y=0,cSz=60):
    self.x=x
    self.y=y
    self.rows=r
    self.columns=c
    self.cellSz=cSz
    self.height=self.rows*self.cellSz
    self.width=self.columns*self.cellSz
    self.matrix=buildGridMtx(self.rows,self.columns)
    self.grid=matrixToGrid(self.matrix,self.cellSz,\
           self.x,self.y)
    self.draw_data=gridToImage(splitPathVtcs(\
                getCritVertices(self.matrix,self.grid),\
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
# 
