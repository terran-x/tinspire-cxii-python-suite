#### 
from ti_draw import *
from random import *
from math import *
####
from bgobject import *
from vehicle import *
from riverhaz import *
from player import *
from hud import *
from bonus import *
####
class Level:
  viewW=0
  viewH=0
  rowH=0
  num=1
  lives=0
  timer=0
  score=0
  pChar=0
  hud=0
  bnsItems=0
  bgObjects=0
  vehDir=0
  vehVel=0
  vehHaz=0
  vehTime=0
  rvrDir=0
  rvrVel=0
  rvrHaz=0
  rvrTime=0
  lastY=0
  lastKey=0
  input=0
  keyset=0

  def __init__(self,lvl,lives,score,input):
    dim=get_screen_dim()
    w=dim[0]
    h=dim[1]
    r=floor(h/9)
    self.rowH=r
    self.viewW=w
    self.viewH=h
    self.num=lvl
    self.timer=0
    self.lives=lives
    self.score=score
    self.input=input
    if self.input==1:
      self.keyset=["left","right","up","down"]
    elif self.input==2:
      self.keyset=["4","6","8","2"]
      
    
    self.vehTime=[0,0,0,0]
    self.vehDir=[0,0,0,0]
    self.vehDir[0]=choice([-1,1])
    self.vehDir[1]=choice([-1,1])
    self.vehDir[2]=choice([-1,1])
    self.vehDir[3]=choice([-1,1])
    self.vehVel=[0,0,0,0]
    self.vehVel[0]=uniform(25+self.num,50+self.num)
    self.vehVel[1]=uniform(25+self.num,50+self.num)
    self.vehVel[2]=uniform(25+self.num,50+self.num)
    self.vehVel[3]=uniform(25+self.num,50+self.num)
    
    self.rvrTime=[0,0,0]
    self.rvrDir=[0,0,0]
    self.rvrDir[0]=choice([-1,1])
    self.rvrDir[1]=choice([-1,1])
    self.rvrDir[2]=choice([-1,1])
    self.rvrVel=[0,0,0]
    self.rvrVel[0]=uniform(10+self.num,30+self.num)
    self.rvrVel[1]=uniform(10+self.num,30+self.num)
    self.rvrVel[2]=uniform(10+self.num,30+self.num)
    
    self.bgObjects=[]
    self.addBGObject(0,0,w,r,[130,70,0])
    self.addBGObject(0,r,w,r*3,[0,20,220])
    self.addBGObject(0,r*4,w,r*4,[200,200,200])
    self.addBGObject(0,r*8,w,r*3,[30,180,30])
    self.addBGObject(w/4,0,w/212,r,[0,0,0])
    self.addBGObject(2*w/4,0,w/212,r,[0,0,0])
    self.addBGObject(3*w/4,0,w/212,r,[0,0,0])
    
    self.vehHaz=[[],[],[],[]]
    self.addVehicle(0)
    self.addVehicle(1)
    self.addVehicle(2)
    self.addVehicle(3)
    
    self.rvrHaz=[[],[],[]]
    self.addRHaz(0)
    self.addRHaz(1)
    self.addRHaz(2)
    
    self.pChar=0
    self.addPlayer(6,[0,255,0],self.rowH)
    
    self.hud=0
    self.addHud(0,r*8.5,w,r*1.5)
    
    self.bnsItems=[]
    return

  def addBGObject(self,x,y,w,h,c):
    bgo=BGObject(x,y,w,h,c)
    self.bgObjects.append(bgo)
    return

  def addPlayer(self,s,c,hop):
    x=self.viewW/2
    y=self.viewH-(self.rowH/2)-s
    x1=hop
    x2=self.viewW-hop
    y1=hop
    y2=self.viewH-hop
    self.pChar=Frog(x,y,s,hop,c,x1,x2,y1,y2)
    return

  def addVehicle(self,row):
    x=0
    y=(row+4)*self.rowH
    w=self.viewW*choice([.4,.3,.2,.1])
    h=self.rowH-2
    x1=0
    x2=0
    d=self.vehDir[row]
    c=choice([[255,255,0],[240,0,10],[0,0,120],[230,230,255],[0,0,0],[0,120,0],[0,100,120],[200,150,0]])
    if d==-1:
      x=self.viewW
      x1=self.viewW-w
      x2=-w
    else:
      x=-w
      x1=0
      x2=self.viewW+w
    vh=Vehicle(x,y,w,h,d,self.vehVel[row],x1,x2,c,random())
    self.vehHaz[row].append(vh)
    return

  def addRHaz(self,row):
    x=0
    y=(row+1)*self.rowH
    h=self.rowH-2
    x1=0
    x2=0
    d=self.rvrDir[row]
    dly=0
    
    if self.num<=32 and random()<=.2:
      t=1
    elif 32<self.num<=64 and random()<=.35:
      t=1
    elif self.num>64 and random()<=.5:
      t=1
    else:
      t=0
    
    if self.num<=32:
      dly=random()
    else:
      dly=.5*random()
    
    if t==0:
      w=self.viewW*choice([.35,.2,.1])
      c=[110,60,0]
    else:
      w=self.viewW*.2
      c=[40,150,20]
      
    if d==-1:
      x=self.viewW
      x1=self.viewW-w
      x2=-w
    else:
      x=-w
      x1=0
      x2=self.viewW+w
    rh=RvrHaz(x,y,w,h,t,d,self.rvrVel[row],x1,x2,c,dly)
    self.rvrHaz[row].append(rh)
    return

  def addHud(self,x,y,w,h):
    self.hud=hud(x,y,w,h,self)

  def addBonus(self,x,y,r,t):
    bi=Bonus(x,y,r,t)
    self.bnsItems.append(bi)

  def draw(self):
    use_buffer()
    for i in range(0,len(self.bgObjects)):
      self.bgObjects[i].draw()
    for i in range(0,len(self.rvrHaz)):
      for j in range(0,len(self.rvrHaz[i])):
        self.rvrHaz[i][j].draw()
    for i in range(0,len(self.bnsItems)):
      self.bnsItems[i].draw()
    for i in range(0,len(self.vehHaz)):
      for j in range(0,len(self.vehHaz[i])):
        self.vehHaz[i][j].draw()
    self.pChar.draw()
    self.hud.draw()
    return

  def update(self,delta,input):
    self.timer+=delta
    vGen=0
    vRm=0
    vTime=0
    for i in range(0,len(self.vehHaz)):
      vGen=0
      for j in range(0,len(self.vehHaz[i])):
        if self.vehHaz[i][j].update(delta)==1:
          if self.vehHaz[i][j].state==1:
            vGen=1
          elif self.vehHaz[i][j].state==2:
            vRm=self.vehHaz[i][j]
      
      if self.num<=32:
        vTime=floor((101-self.num)/16)
      elif 33<=self.num<=64:
        vTime=floor((101-self.num)/20)
      elif self.num>=65:
        vTime=1
      
      if vGen==1:
        self.vehTime[i]=delta
      elif self.vehTime[i]>=vTime:
        self.vehTime[i]=0
        self.addVehicle(i)
      elif self.vehTime[i]>0:
        self.vehTime[i]+=delta
      
      if vRm!=0:
        self.vehHaz[i].remove(vRm)
        vRm=0
    
    lGen=0
    lRm=0
    lTime=0
    for i in range(0,len(self.rvrHaz)):
      lGen=0
      for j in range(0,len(self.rvrHaz[i])):
        if self.rvrHaz[i][j].update(delta)==1:
          if self.rvrHaz[i][j].state==1:
            lGen=1
          elif self.rvrHaz[i][j].state==2:
            lRm=self.rvrHaz[i][j]
        if self.rvrHaz[i][j].type==1 and self.rvrHaz[i][j].animate==0 and random()<=0.01:
          self.rvrHaz[i][j].animate=choice([1,2])
          if self.rvrHaz[i][j].animate==1:
            self.rvrHaz[i][j].cellcnt=100
          else:
            self.rvrHaz[i][j].cellcnt=20
      
      if self.num<=32:
        lTime=1
      else:
        lTime=0.1
      
      if lGen==1:
        self.rvrTime[i]=delta
      elif self.rvrTime[i]>=2:
        self.rvrTime[i]=0
        self.addRHaz(i)
      elif self.rvrTime[i]>0:
        self.rvrTime[i]+=delta
      
      if lRm!=0:
        self.rvrHaz[i].remove(lRm)
        lRm=0
    
    onScrn=0-(self.pChar.size/2)<self.pChar.x<self.viewW+(self.pChar.size/2)
    clipping=self.clipping(delta,input)
    if clipping==1 or not onScrn:
      return 1
    elif clipping==0:
      return 0
    
    if random()<=.005 and len(self.bnsItems)<3:
      r=randint(1,7)
      y=(self.viewH-(self.rowH/2)-self.pChar.size)-(self.pChar.hop*r)
      if r>4:
        rHaz=self.rvrHaz[int(fabs(r-7))][randint(0,len(self.rvrHaz[int(fabs(r-7))])-1)]
        x=rHaz.x+self.bnsDrop(rHaz)+2
      else:
        x=randrange(self.pChar.hop,self.viewW-self.pChar.hop,self.pChar.hop)
      t=randint(0,3)
      self.addBonus(x-2,y,r,t)
    elif random()<=.008 and len(self.bnsItems)<1:
      x=choice([self.viewW/8,1.5*self.viewW/4,2.5*self.viewW/4,3.5*self.viewW/4])
      y=self.rowH/2
      t=randint(0,3)
      r=8
      self.addBonus(x,y,r,t)
    
    rm=0
    for i in range(0,len(self.bnsItems)):
      self.bnsItems[i].timer-=delta
      if self.bnsItems[i].timer<=0:
        rm=self.bnsItems[i]
      if 4<self.bnsItems[i].row<8:
        idx=int(fabs(self.bnsItems[i].row-7))
        self.bnsItems[i].x+=delta*self.rvrVel[idx]*self.rvrDir[idx]
    if rm!=0:
      self.bnsItems.remove(rm)
      rm=0
    
    return

  def clipping(self,delta,input):
    x=0
    y=0
    l=0
    h=0
    
    if self.pChar.y>=self.bgObjects[2].y:
      for i in range(0,len(self.vehHaz)):
        for j in range(0,len(self.vehHaz[i])):
          x=self.vehHaz[i][j].x
          y=self.vehHaz[i][j].y
          l=self.vehHaz[i][j].width
          h=self.vehHaz[i][j].height
          xClip=x<=self.pChar.x<=(x+l)
          yClip=y<=self.pChar.y<=(y+h)
          
          if xClip and yClip:
            return 1
    
    elif self.bgObjects[1].y<self.pChar.y<self.bgObjects[2].y:
      for i in range(0,len(self.rvrHaz)):
        for j in range(0,len(self.rvrHaz[i])):
          x=self.rvrHaz[i][j].x
          y=self.rvrHaz[i][j].y
          l=self.rvrHaz[i][j].width
          h=self.rvrHaz[i][j].height
          xClip=x<=self.pChar.x<=(x+l)
          yClip=y<=self.pChar.y<=(y+h)
          lMth=self.rvrHaz[i][j].x<=self.pChar.x<=self.rvrHaz[i][j].x+.33*self.rvrHaz[i][j].width
          rMth=self.rvrHaz[i][j].x+self.rvrHaz[i][j].width>=self.pChar.x>=self.rvrHaz[i][j].x+.66*self.rvrHaz[i][j].width
          logVec=delta*self.rvrVel[i]*self.rvrDir[i]
          
          if xClip and yClip:
            if y!=self.lastY:
              self.pChar.x=self.rvrHaz[i][j].x+self.pChar.xStep(self.rvrHaz[i][j],1)
              self.lastY=y
            
            self.pChar.x+=logVec
            self.bnsClip()
            
            if input != "":
              self.pChar.update(input,self.keyset)
            
            if self.rvrHaz[i][j].solid==0:
              return 1
            elif self.rvrHaz[i][j].eat==1:
              if lMth and self.rvrHaz[i][j].dir==-1 or rMth and self.rvrHaz[i][j].dir==1:
                return 1
            return
      return 1
    
    if self.pChar.y<self.rowH:
      if self.pChar.x<=self.viewW/4:
        self.pChar.x=(self.viewW/8)
      elif self.viewW/4<self.pChar.x<=2*(self.viewW/4):
        self.pChar.x=(1.5*self.viewW/4)
      elif 2*(self.viewW/4)<self.pChar.x<=3*(self.viewW/4):
        self.pChar.x=(2.5*self.viewW/4)
      elif self.pChar.x>3*(self.viewW/4):
        self.pChar.x=(3.5*self.viewW/4)
      self.bnsClip()
      return 0
    
    if self.lastKey=="down" or self.lastKey=="2" and self.lastY==3*self.rowH:
      self.pChar.x=self.pChar.xStep(self,2)
      self.lastY=0
    
    self.pChar.update(input,self.keyset)
    self.bnsClip()

  def bnsDrop(self,rObj):
    xGrid=[]
    xTar=0
    
    xTar=rObj.width/2
    while xTar>0:
      xGrid.append(xTar)
      xTar-=self.pChar.hop
    xTar=rObj.width/2
    while xTar<rObj.width:
      xTar+=self.pChar.hop
      if xTar<rObj.width:
        xGrid.append(xTar)
    xGrid=sorted(xGrid)
    
    xTar=choice(xGrid)
    return(xTar)

  def bnsClip(self):
    rm=0
    for i in range(0,len(self.bnsItems)):
      xClip=self.pChar.x-self.pChar.size<self.bnsItems[i].x<self.pChar.x+self.pChar.size
      yClip=self.pChar.y-self.pChar.size<self.bnsItems[i].y<self.pChar.y+self.pChar.size
      if xClip and yClip:
        self.score+=self.bnsItems[i].points
        if self.bnsItems[i].type=="life":
          self.lives+=1
        rm=self.bnsItems[i]
    if rm!=0:
      self.bnsItems.remove(rm)
      rm=0
    return
