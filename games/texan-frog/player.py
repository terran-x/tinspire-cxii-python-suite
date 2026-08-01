####
from ti_draw import *
from math import *
####
class Frog:
  x=0
  y=0
  colour=[]
  hop=0
  size=0
  state=0
  xlim1=0
  xlim2=0
  ylim1=0
  ylim2=0

  def __init__(self,x,y,s,d,c,x1,x2,y1,y2):
    self.x=x
    self.y=y
    self.size=s
    self.hop=d
    self.colour=c
    self.state=1
    self.xlim1=x1
    self.xlim2=x2
    self.ylim1=y1
    self.ylim2=y2
    return

  def draw(self):
    use_buffer()
    set_color(self.colour[0],self.colour[1],self.colour[2])
    fill_circle(self.x,self.y,self.size)
    return

  def update(self,key,keyset):
    if key==keyset[0] and not self.x<=self.xlim1:
      self.x-=self.hop
    elif key==keyset[1] and not self.x>=self.xlim2:
      self.x+=self.hop
    elif key==keyset[2] and not self.y<=self.ylim1:
      self.y-=self.hop
    elif key==keyset[3] and not self.y>=self.ylim2:
      self.y+=self.hop
    return

  def xStep(self,rObj,mode):
    xGrid=[]
    xTar=0
    width=0
    
    if mode==1:
      width=rObj.width
    else:
      width=rObj.viewW
    
    xTar=width/2
    while xTar>0:
      xGrid.append(xTar)
      xTar-=self.hop
    xTar=width/2
    while xTar<width:
      xTar+=self.hop
      if xTar<width:
        xGrid.append(xTar)
    xGrid=sorted(xGrid)
    
    for i in range(0,len(xGrid)):
      if mode==1:
        prX=self.x-rObj.x
      else:
        prX=self.x
      if i==0:
        optX=fabs(prX-xGrid[i])
        xTar=xGrid[i]
      if optX>fabs(prX-xGrid[i]):
        optX=fabs(prX-xGrid[i])
        xTar=xGrid[i]
    return(xTar)
