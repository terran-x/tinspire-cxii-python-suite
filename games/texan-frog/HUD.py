####
from ti_draw import *
from level import *
####
class hud:
  x=0
  y=0
  width=0
  height=0

  def __init__(self,x,y,w,h,lvl):
    self.x=x
    self.y=y
    self.width=w
    self.height=h
    self.lvl=lvl
    return

  def draw(self):
    x=self.width/40
    use_buffer()
    set_color(0,255,0)
    if self.lvl.lives<=4:
      xGap=x
      for i in range(0,self.lvl.lives):
        fill_circle(xGap,self.y+(self.height/4),self.height/8)
        xGap+=(self.width/24)
    elif 99>=self.lvl.lives>4:
      draw_text(x/3,(self.y+(self.height/2)),str(self.lvl.lives))
    else:
      draw_text(x/3,(self.y+(self.height/2)),"99")
    
    set_color(0,0,0)
    num=str(self.lvl.num)
    if len(num)<2:
      num="0"+num
    if self.lvl.num<=99:
      draw_text((self.width-(x*4)),(self.y+self.height/2),"lvl:"+num)
    else:
      draw_text((self.width-(x*4.8)),(self.y+self.height/2),"lvl:"+num)
    time=self.tFormat()
    set_color(0,0,0)
    draw_text((self.width-(x*6))/2,self.y+(self.height/2),time)
    set_color(255,0,0)
#    draw_text(228,200,"x:"+str(round(self.lvl.pChar.x,1))+" y:"+str(round(self.lvl.pChar.y,1)))
#    draw_text(228,200,"Score: "+str(self.lvl.score))
    return

  def tFormat(self):
    ms=int(round((self.lvl.timer-floor(self.lvl.timer))*99,2))
    s=int(fmod(floor(self.lvl.timer),60))
    m=int((floor(self.lvl.timer)/60))
    if len(str(ms))<2:
      ms="0"+str(ms)
    if len(str(s))<2:
      s="0"+str(s)
    if len(str(m))<2:
      m="0"+str(m)
    time=str(m)+":"+str(s)+":"+str(ms)
    return time
