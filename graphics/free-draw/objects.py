class object:
  def __init__(self,x,y,t="object"):
    self.type=t
    self.x=x
    self.y=y

class rectangle(object):
  def __init__(self,x,y,w,h,c,f=-1,t="rectangle"):
    object.__init__(self,x,y,t)
    self.colour=c
    self.width=w
    self.height=h
    self.fill=f

class circle(object):
  def __init__(self,x,y,r,c,f=-1,t="circle"):
    object.__init__(self,x,y,t)
    self.colour=c
    self.radius=r
    self.fill=f

class line(object):
  def __init__(self,x,y,x2,y2,c,t="line"):
    object.__init__(self,x,y,t)
    self.x2=x2
    self.y2=y2
    self.colour=c

class arc(object):
  def __init__(self,x,y,w,h,a1,a2,c,f=-1,t="arc"):
    object.__init__(self,x,y,t)
    self.width=w
    self.height=h
    self.angle1=a1
    self.angle2=a2
    self.fill=f
    self.colour=c

class polygon(object):
  def __init__(self,x,y,c,f=-1,t="polygon"):
    object.__init__(self,x,y,t)
    self.fill=f
    self.colour=c
