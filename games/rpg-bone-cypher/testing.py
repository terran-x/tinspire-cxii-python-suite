####################
from ti_draw import *
from random import *
from time import *
####################

# Transposes grid data into an image and compiles
# the image drawing data into a list.
def gridToImage(grid,cellSz,x=0,y=0,tileClr={"empty":\
  [140,140,140],"entry":[0,220,0],"exit":[220,0,0]}):
  rows=len(grid)
  cols=len(grid[0])
  w=cellSz*cols # Grid width
  h=cellSz*rows # Grid height
  prevClr=[0,0,0]
  drawData=[]
  drawData.append("draw_rect("+str(x-w/2)+","+\
                 str(y-h/2)+","+str(w)+","+str(h)+")")
  for i in range(0,rows):
    for j in range(0,cols):
      if grid[i][j]==EMPTY:
        if prevClr!=tileClr["empty"]:
          drawData.append("set_color("+str(tileClr["empty"][0])\
          +","+str(tileClr["empty"][1])+","+str(tileClr["empty"][2])+")")
          prevClr=tileClr["empty"]
        drawData.append("fill_rect("+str((x-w/2)+j*cellSz)+","+\
                       str((y-h/2)+i*cellSz)+","+str(cellSz)+","+str(cellSz)+")")
      elif grid[i][j]==ENTRY:
        if prevClr!=tileClr["entry"]:
          drawData.append("set_color("+str(tileClr["entry"][0])\
          +","+str(tileClr["entry"][1])+","+str(tileClr["entry"][2])+")")
          prevClr=tileClr["entry"]
        drawData.append("fill_rect("+str((x-w/2)+j*cellSz)+","+\
                       str((y-h/2)+i*cellSz)+","+str(cellSz)+","+str(cellSz)+")")
      elif grid[i][j]==EXIT:
        if prevClr!=tileClr["exit"]:
          drawData.append("set_color("+str(tileClr["exit"][0])\
          +","+str(tileClr["exit"][1])+","+str(tileClr["exit"][2])+")")
          prevClr=tileClr["exit"]
        drawData.append("fill_rect("+str((x-w/2)+j*cellSz)+","+\
                       str((y-h/2)+i*cellSz)+","+str(cellSz)+","+str(cellSz)+")")
  return drawData

# Example of state object from EJS textbook
#class VillageState:
#  def __init__(self,place,parcels):
#    self.place=place
#    self.parcels=parcels
#  def move(self,dest):
#    if not dest in getattr(ROAD_GRAPH,self.place):
#      return self
#    else:
#      parcels=[]
#      for p in self.parcels:
#        if p.place!=self.place:
#          parcels.append(p)
#        else:
#          if p.address!=dest:
#            parcels.append(Parcel(dest,p.address))
#      return VillageState(dest,parcels)
#  @staticmethod
#  def random(parcelCnt=5):
#    parcels=[]
#    places=dir(ROAD_GRAPH)
#    places.sort()
#    places=places[:len(places)-5]
#    for i in range(parcelCnt):
#      address=choice(places)
#      place=choice(places)
#      while place==address:
#        place=choice(places)
#      parcels.append(Parcel(place,address))
#    return VillageState("Post Office",parcels)

# 
