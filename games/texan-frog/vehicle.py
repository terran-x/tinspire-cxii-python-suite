####
from ti_draw import *
####
class Vehicle:
  x=0
  y=0
  width=0
  height=0
  dir=1
  vel=0
  xlim1=0
  xlim2=0
  colour=[]
  delay=0
  state=0

  def __init__(self,x,y,w,h,d,v,x1,x2,c,l):
    self.x=x
    self.y=y
    self.width=w
    self.height=h
    self.dir=d
    self.vel=v
    self.xlim1=x1
    self.xlim2=x2
    self.colour=c
    self.delay=l
    self.state=0
    return

  def draw(self):
    use_buffer()
    set_color(self.colour[0],self.colour[1],self.colour[2])
    fill_rect(self.x,self.y,self.width,self.height)
    return

  def update(self,delta):
    if self.delay>=0:
      self.delay-=delta
      return
    self.x+=delta*self.vel*self.dir
    if self.dir==1:
      if self.x>=self.xlim2:
        if self.state<2:
          self.state=2
          return 1
      elif self.x>=self.xlim1:
        if self.state<1:
          self.state=1
          return 1
      else:
        self.state=0
    else:
      if self.x<=self.xlim2:
        if self.state<2:
          self.state=2
          return 1
      elif self.x<=self.xlim1:
        if self.state<1:
          self.state=1
          return 1
      else:
        self.state=0
    return 0

# 
