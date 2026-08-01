#=======================
from gfx import *
#=======================
class Menu:
  def __init__(self,w,h,o,t="",s=1,bc=[255,255,255],oc=[0,0,0],ic=[255,0,0],ld=[0,0]):
    self.width=w
    self.height=h
    self.options=o
    self.step=s
    self.type=t
    self.bgColour=bc
    self.optColour=oc
    self.indColour=ic
    self.logoDim=ld
    self.mPos=[]
    self.key=""

  def show(self):
    drawMenu(self)
    return

  def input(self):
    self.mPos=get_mouse()
    self.key=get_key()
    if self.key=="down":
      if self.step<=(len(self.options)-1):
        self.step+=1
      else:
        self.step=1
    elif self.key=="up":
      if self.step>=2:
        self.step-=1
      else:
        self.step=len(self.options)
    elif self.key=="enter" or self.key=="center":
      return self.options[self.step-1]
    return
