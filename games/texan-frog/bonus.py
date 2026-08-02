####
from ti_draw import *
from random import *
####
class Bonus:
  x=0
  y=0
  row=0
  colour=[[240,200,0],[230,230,235],[240,235,0],[255,0,10]]
  type=["brnz","slvr","gold","life"]
  points=[500,1000,2000,1000]
  state=0
  timer=0

  def __init__(self,x,y,r,idx):
    self.x=x
    self.y=y
    self.row=r
    self.type=self.type[idx]
    self.colour=self.colour[idx]
    self.points=self.points[idx]
    self.state=1
    self.timer=3+(random()*3)

  def draw(self):
    use_buffer()
    set_color(self.colour[0],self.colour[1],self.colour[2])
    if self.type=="life":
      draw_text(self.x-6,self.y+6,"▼")
    else:
      draw_text(self.x-6,self.y+6,"★")
#    fill_circle(self.x,self.y,6)
    return

# 
