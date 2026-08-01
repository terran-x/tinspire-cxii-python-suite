####
from ti_draw import *
####
class RvrHaz:
  x=0
  y=0
  width=0
  height=0
  type=0
  animate=0
  cellcnt=0
  solid=1
  eat=0
  dir=1
  vel=0
  xlim1=0
  xlim2=0
  colour=[]
  delay=0
  state=0

  def __init__(self,x,y,w,h,t,d,v,x1,x2,c,l):
    self.x=x
    self.y=y
    self.width=w
    self.height=h
    self.type=t
    self.dir=d
    self.vel=v
    self.xlim1=x1
    self.xlim2=x2
    self.colour=c
    self.delay=l
    self.state=0
    self.animate=0
    self.cellcnt=0
    return

  def draw(self):
    use_buffer()
    if self.animate==1 and self.cellcnt!=0:
      set_color(self.colour[0],self.colour[1],self.colour[2])
      if self.cellcnt>=70 or self.cellcnt<=30:
        self.solid=1
        fill_rect(self.x,self.y,self.height,self.height)
        fill_rect(self.x+(2*self.height),self.y,self.height,self.height)
      else:
        self.solid=0
      self.cellcnt-=1
    elif self.animate==2 and self.cellcnt!=0:
      set_color(self.colour[0],self.colour[1],self.colour[2])
      set_pen("thick","solid")
      if self.dir==1:
        fill_rect(self.x,self.y,.66*self.width,self.height)
        draw_line(self.x+.66*self.width,self.y+.1*self.height,self.x+self.width,self.y-.3*self.height)
        draw_line(self.x+.66*self.width,self.y+.2*self.height,self.x+self.width,self.y-.2*self.height)
        draw_line(self.x+.66*self.width,self.y+.8*self.height,self.x+self.width,self.y+.8*self.height)
      elif self.dir==-1:
        fill_rect(self.x+(.33*self.width),self.y,(.66*self.width),self.height)
        draw_line(self.x,self.y-.3*self.height,self.x+(.33*self.width),self.y+.1*self.height)
        draw_line(self.x,self.y-.2*self.height,self.x+(.33*self.width),self.y+.2*self.height)
        draw_line(self.x,self.y+.8*self.height,self.x+(.33*self.width),self.y+.8*self.height)
      self.eat=1
      self.cellcnt-=1
      if self.cellcnt==0:
        self.eat=0
    else:
      self.animate=0
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
