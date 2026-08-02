####
from ti_draw import *
####
class BGObject:
  x=0
  y=0
  width=0
  height=0
  colour=[]

  def __init__(self,x,y,w,h,c):
    self.x=x
    self.y=y
    self.width=w
    self.height=h
    self.colour=c
    return

  def draw(self):
    use_buffer()
    set_color(self.colour[0],self.colour[1],self.colour[2])
    fill_rect(self.x,self.y,self.width,self.height)
    return

# 
