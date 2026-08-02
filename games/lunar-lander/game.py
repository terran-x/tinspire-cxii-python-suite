#=======================
from physx_engine import *
from ti_draw import *
from ti_system import *
from math import *
from random import *
from menus import *
from sys import *
from score import *
#=======================
# Moon constants
MOON_MASS=7.35*10**22
MOON_RAD=1.74*10**6
# Descent lunar module init. properties
DLM_G_MASS=15200
DLM_FUEL_MASS=8165
DLM_MAX_THRUST=45040
DLM_MAX_FR=8.6
# CM Columbia properties
CMC_ORB_ALT=120096
CMC_ORB_VEL=1580
#=======================
class Environment:
  def __init__(self,sim=False,ctrl=-1,dbg=False,lz=[],sfc=-65):
    self.sim=sim
    self.controls=ctrl
    self.debug=dbg
    self.surface=sfc
    self.initAlt=0
    self.lz=lz
    self.LZind=[]
    self.lReboot=False
    self.rbTimer=0
    self.score=0
    self.scoreboard=None
    self.state=0
    self.timer=0
    self.ani_timer=0
    self.run_time=0
    self.camera=None
    self.key=""
    self.objArr=[]
    self.grvArr=[]
    self.menus=[]
    self.inputlock=False
    
    # Camera
    self.camera=Camera()
    
    # Lander object
    if self.sim:
      lm=Lander(0,CMC_ORB_ALT,DLM_G_MASS,DLM_FUEL_MASS,CMC_ORB_VEL)
      self.objArr.append(lm)
    elif not self.sim:
      lm=Lander(0,CMC_ORB_ALT*uniform(0.005,0.015),DLM_G_MASS,DLM_FUEL_MASS*0.1)
      self.objArr.append(lm)
    # Set initial altitude for score calcs
    self.initAlt=self.objArr[0].displayAlt+fabs(self.surface)+1
    
    # Moon object
    moon=object(0,-MOON_RAD,MOON_MASS,0,0,0,0,"moon")
    self.objArr.append(moon)
    
    # Create gravity object array for physics engine
    self.grvArr=self.objArr.copy()
    
    # Setup menu array
    self.menus.append(Menu(self.camera.width,self.camera.height,["Start","Settings","Scoreboard","Help","Quit"],"main",1,[0,0,0],[255,255,255],[255,0,0],[221,44]))
    self.menus.append(Menu(self.camera.width,self.camera.height,["Controls: "+str(self.controls),"Sim: "+str(self.sim),"Debug Mode: "+str(self.debug), "Back"],"settings",1,[0,0,0],[255,255,255],[255,0,0],[221,44]))
    
    # Spawn landing target
    self.lz=self.randLZ()
    
    # Check if surface bg frame needed
    if lm.pos[1]<=0.5*self.camera.height:
      self.camera.bgNum=randint(7,9)
    
    # Initialize scoreboard
    self.initSB()
    
    return

  def update(self,delta):
    # Update lander, return false if destroyed
    if not self.objArr[0].update(self,delta):
      return 0
    
    # Process user inputs
    if not self.inputlock:
      self.input(delta)
    
    # Moon object follow lander x position
    self.objArr[1].pos[0]=self.objArr[0].pos[0]
    
    # Update grid location for lander
    self.camera.prevGR=self.camera.gridRef.copy()
    self.camera.updGridRef(self.objArr[0].pos[0],self.objArr[0].pos[1])
    
    # Update onscreen lz indicator
    if not self.sim:
      self.LZind=self.lndrToLZ(self.objArr[0])
    
    # System reboot of lander
    if self.lReboot:
      self.rbTimer-=delta
      if self.objArr[0].reboot(self.rbTimer):
        self.inputlock=False
        self.lReboot=False
        self.rbTimer=0
    
    # Next background image for display
    self.camera.bgImgNum()
    return 1

# Handles user keypad input
  def input(self,delta):
    self.key=get_key()
    if self.objArr[0].fuel>0:
      if self.controls==1:
        if self.key=="left":
          self.objArr[0].onBurn(1,delta,self.controls)
        elif self.key=="right":
          self.objArr[0].onBurn(3,delta,self.controls)
        elif self.key=="up":
          self.objArr[0].onBurn(2,delta,self.controls)
      elif self.controls==-1:
        if self.key=="left":
          self.objArr[0].burn[0]*=-1
          if self.objArr[0].burn[2]==1:
            self.objArr[0].burn[2]*=-1
        elif self.key=="right":
          self.objArr[0].burn[2]*=-1
          if self.objArr[0].burn[0]==1:
            self.objArr[0].burn[0]*=-1
        elif self.key=="up":
          self.objArr[0].burn[1]*=-1
    if self.key=="7":
      self.objArr[0].setThrottle(1)
    elif self.key=="4":
      self.objArr[0].setThrottle(-1)
    if self.key=="r":
      if not self.lReboot:
        self.objArr[0].burn=[-1,-1,-1]
        self.inputlock=True
        self.lReboot=True
        self.rbTimer=5
    if self.key=="esc":
      self.menus[0]=Menu(self.camera.width,self.camera.height,["Continue","Settings","Scoreboard","Help","Quit"],"pause",1,[0,0,0],[255,255,255],[255,0,0],[221,44])
      self.state=0
    return

# Creates random lz position
  def randLZ(self):
    if not self.sim:
      return [randint(-1000,1000),self.surface-18]
    return 0

# Setup scoreboard
  def initSB(self):
    self.scoreboard=scoreboard("landerHS",[],10)
    # Write stored high scores to scoreboard if available
    try:
      hiScrs=recall_list("highscores")
      hiScrs=hs_import(hiScrs)
      for i in range(0,len(hiScrs)):
        self.scoreboard.scores[i]=hiScrs[i]
    except:
      store_list("highscores",hs_export(self.scoreboard.scores))
    return

# Check for high score
  def hsCheck(self):
    newScr=hscore("NEW",self.score)
    if self.scoreboard.update(newScr):
      newScr.name=newHS()
      store_list("highscores",hs_export(self.scoreboard.scores))
      return True
    return False

# Score accumulation
  def scrAcc(self):
    score=self.landScr()
    score+=self.timeScr()
    score+=self.dmgScr()
    score+=self.fuelScr()
    return int(score)

# Score modifier: time
  def timeScr(self):
    tav=16 # Target average velocity
    lzd=sqrt(self.lz[0]**2+self.initAlt**2) # Dist to LZ
    tt=lzd/tav # Target time in secs
    return 1000+(self.run_time-tt)*-25

# Score modifier: landed
  def landScr(self):
    lnd=500 # Successful landing
    trgDist=fabs(self.lz[0]-self.objArr[0].pos[0]) # Dist. from target
    if trgDist<=15:
      ds=1000
    elif trgDist<=30:
      ds=500
    elif trgDist<=50:
      ds=250
    elif trgDist>50:
      ds=-trgDist*2
    return lnd+ds

# Score modifier: damage
  def dmgScr(self):
    return -self.objArr[0].damage*10

# Score modifier: fuel
  def fuelScr(self):
    return self.objArr[0].fuel/self.objArr[0].max_fuel*500

# Calc where lander/lz line intersects window frame
  def lndrToLZ(self,lander):
    # Check lz not in window
    if self.camera.frameXY[0]>self.lz[0] or self.lz[0]>self.camera.frameXY[1] or self.lz[1]<self.camera.frameXY[2]:
      # Calc args between lander and lz, lwr left win, lwr right win
      argL=pi+atan2((lander.pos[1]-self.camera.frameXY[2]),(lander.pos[0]-self.camera.frameXY[0]))
      argR=(3/2)*pi+atan2((self.camera.frameXY[1]-lander.pos[0]),(lander.pos[1]-self.camera.frameXY[2]))
      argTL=pi+atan2((lander.pos[1]-self.lz[1]),(lander.pos[0]-self.lz[0]))
      # Return indicator coords based frame intersection zone
      if argTL<argL:
        return [self.camera.frameXY[0],lander.pos[1]-(lander.pos[0]-self.camera.frameXY[0])*tan(argTL),1]
      elif argTL<=argR:
        return [lander.pos[0]-(lander.pos[1]-self.camera.frameXY[2])/tan(argTL),self.camera.frameXY[2],2]
      else:
        return [self.camera.frameXY[1],lander.pos[1]-fabs((self.camera.frameXY[1]-lander.pos[0])*tan(argTL)),3]
    return 0

# Handles whether lander has landed/taken off
  def landCheck(self,lander):
    if lander.pos[1]<=self.surface and not lander.landed:
      lander.landed=True
      self.lReboot=False
      self.inputlock=True
      # Applies damage if rqd
      lander.dmgCalc()
      lander.vel.coord=[0,0]
      lander.pos[1]=self.surface-1
      # Stops thrusters on land
      if self.controls==-1:
        for i in range(3):
          if lander.burn[i]==1:
            lander.burn[i]*=-1
      self.grvArr.remove(lander)
      if lander.damage<100:
        self.state=3
      return 1
    # Handles take off
    elif lander.burn[1]==1 and lander.landed and lander.fuel>0 or self.controls==1 and self.key=="up" and lander.landed and lander.fuel>0:
      lander.pos[1]=self.surface+1
      lander.landed=False
      self.grvArr.append(lander)
    return 0

# Handles menus
  def displayMenus(self):
    slxn=None
    key=""
    
    self.menus[0].show()
    slxn=self.menus[0].input()
    # Start
    if slxn==self.menus[0].options[0]:
      return 1
    # Settings
    elif slxn==self.menus[0].options[1]:
      while 1:
        self.menus[1].show()
        slxn=self.menus[1].input()
        # Control setting
        if slxn==self.menus[1].options[0]:
          self.controls*=-1
          self.menus[1]=Menu(self.camera.width,self.camera.height,["Controls: "+str(self.controls),"Sim: "+str(self.sim),"Debug Mode: "+str(self.debug), "Back"],"settings",self.menus[1].step,[0,0,0],[255,255,255],[255,0,0],[221,44])
        # Simulation/game setting
        elif slxn==self.menus[1].options[1]:
          if self.menus[0].type!="pause":
            self.sim=not self.sim
            self.menus[1]=Menu(self.camera.width,self.camera.height,["Controls: "+str(self.controls),"Sim: "+str(self.sim),"Debug Mode: "+str(self.debug), "Back"],"settings",self.menus[1].step,[0,0,0],[255,255,255],[255,0,0],[221,44])
        # Debug display setting
        elif slxn==self.menus[1].options[2]:
          self.debug=not self.debug
          self.menus[1]=Menu(self.camera.width,self.camera.height,["Controls: "+str(self.controls),"Sim: "+str(self.sim),"Debug Mode: "+str(self.debug), "Back"],"settings",self.menus[1].step,[0,0,0],[255,255,255],[255,0,0],[221,44])
        # Back
        elif slxn==self.menus[1].options[3]:
          break
    # High scores
    elif slxn==self.menus[0].options[2]:
      while 1:
        drawHSBd(self)
        key=get_key()
        if key=="enter" or key=="esc":
          break
    # Help
    elif slxn==self.menus[0].options[3]:
      while 1:
        drawHelp(self)
        key=get_key()
        if key=="enter" or key=="esc":
          break
    # Quit
    elif slxn==self.menus[0].options[4]:
      exit()
    return 0

class Lander(object):
  def __init__(self,x,y,m,f=DLM_FUEL_MASS,v=0,vd=180,a=0,ad=0,lnd=False,dmg=0,fr=DLM_MAX_FR,thr=DLM_MAX_THRUST,t="lander"):
    object.__init__(self,x,y,m,a,ad,v,vd,t)
    self.throttle=10
    self.max_fuel=f
    self.fuel=f
    self.max_fr=fr
    self.fuel_rate=self.throttle*self.max_fr*0.1
    self.warn_alarm=False
    self.fuel_alarm=False
    self.dmg_alarm=False
    self.fault_alarm=False
    self.navigation=True
    self.damage=dmg
    self.exploding=False
    self.destroyed=False
    self.faults=[]
    self.displayAlt=y
    self.displayXVel=int(self.vel.coord[0])
    self.displayYVel=int(self.vel.coord[1])
    self.landed=lnd
    self.thrust=thr
    self.burn=[-1,-1,-1]
    self.dry_mass=self.mass-self.fuel
    self.td_threshold=228000 # total destruction (15m/s*15200kg)

  def update(self,env,delta):
    self.displayAlt=int(self.pos[1]+fabs(env.surface)+1)
    self.displayXVel=int(self.vel.coord[0])
    self.displayYVel=int(self.vel.coord[1])
    
    if env.controls==-1:
      for i in range(3):
        if self.burn[i]==1:
          self.onBurn(i+1,delta,env.controls)
    
    env.landCheck(self)
    
    self.randFault()
    self.warningCheck()
    self.faultToll()
    
    if self.destroyed:
      env.menus[0].options[0]="Start"
      env.menus[0].type="main"
      env.objArr.remove(self)
      env.state=2
      return 0
    
    return 1

  def reboot(self,time):
    if time<=0:
      self.fault_alarm=False
      self.navigation=True
      self.faults=[]
      return 1
    return 0

  def setThrottle(self,dir):
    if dir==1 and self.throttle<10:
      self.throttle+=1
    elif dir==-1 and self.throttle>0:
      self.throttle-=1
    self.fuel_rate=self.throttle*self.max_fr*0.1
    return

  def onBurn(self,thruster,delta,controls):
    # Primary thruster
    if thruster==2:
      self.fuel-=delta*self.fuel_rate
      self.mass=self.fuel+self.dry_mass
      self.vel.coord[1]+=(self.thrust*(self.throttle*0.1)/self.mass)*delta
      if controls==-1 and self.fuel<=0:
        self.burn[1]*=-1
    else:
      # Secondary thrusters
      self.fuel-=delta*self.fuel_rate
      self.mass=self.fuel+self.dry_mass
      if thruster==3:
        self.accel.coord[0]+=(self.thrust*self.throttle*0.1)/self.mass
        if controls==-1 and self.fuel<=0:
          self.burn[2]*=-1
      elif thruster==1:
        self.accel.coord[0]-=(self.thrust*self.throttle*0.1)/self.mass
        if controls==-1 and self.fuel<=0:
          self.burn[0]*=-1
    return

  def dmgCalc(self):
    if self.vel.coord[1]<-3:
      try:
        self.faults.remove(["damage","DMG:"+str(int(self.damage))+"%"])
        self.damage+=((int(self.vel.coord[1])*-(self.mass))/self.td_threshold)*100
        self.faults.append(["damage","DMG:"+str(int(self.damage))+"%"])
      except:
        self.damage+=((int(self.vel.coord[1])*-(self.mass))/self.td_threshold)*100
        self.faults.append(["damage","DMG:"+str(int(self.damage))+"%"])
    
    if self.vel.coord[0]<-3 or self.vel.coord[0]>3:
      try:
        self.faults.remove(["damage","DMG:"+str(int(self.damage))+"%"])
        self.damage+=(int(fabs(self.vel.coord[0]))*(self.mass)/self.td_threshold)*100
        self.faults.append(["damage","DMG:"+str(int(self.damage))+"%"])
      except:
        self.damage+=(int(fabs(self.vel.coord[0]))*(self.mass)/self.td_threshold)*100
        self.faults.append(["damage","DMG:"+str(int(self.damage))+"%"])
    
    if self.damage>=100:
      self.lReboot=False
      self.exploding=True
      self.damage=100
    return

  def warningCheck(self):
     if self.fuel/self.max_fuel<0.15 and not self.fuel_alarm:
       self.fuel_alarm=True
       self.warn_alarm=True
     if self.damage>5 and not self.dmg_alarm:
       self.dmg_alarm=True
       self.warn_alarm=True
     if self.faults!=[] and not self.fault_alarm:
       self.fault_alarm=True
     return

  def randFault(self):
    # Fuel leak fault
    if self.faults.count(["fuel","100FLK"])==0 and self.faults.count(["fuel","101FLK"])==0:
      if 5<=self.damage<50 and random()<=0.001:
        self.faults.append(["fuel","100FLK"])
        self.warn_alarm=True
        return 1
      elif self.damage>=50 and random()<=0.002:
        self.faults.append(["fuel","101FLK"])
        self.warn_alarm=True
        return 1
    elif self.faults.count(["fuel","100FLK"])==1:
      if self.damage>=50 and random()<=0.002:
        self.faults.remove(["fuel","100FLK"])
        self.faults.append(["fuel","101FLK"])
        self.warn_alarm=True
        return 1
    # Engine fault
    if self.faults.count(["engine","200ENG"])==0:
      if self.damage>=5 and random()<=0.002:
        self.faults.append(["engine","200ENG"])
        self.warn_alarm=True
        return 1
    # Navigation system fault
    if self.faults.count(["navigation","300NAV"])==0:
      if random()<=0.0002:
        self.faults.append(["navigation","300NAV"])
        self.warn_alarm=True
        return 1
    # Computer system fault
    if self.faults.count(["computer","400CPU"])==0:
      if random()<=0.0002:
        self.faults.append(["computer","400CPU"])
        self.warn_alarm=True
        return 1
    return 0

  def faultToll(self):
    # Fuel depletion on leak
    if self.faults.count(["fuel","100FLK"])==1:
      self.fuel-=0.6
    elif self.faults.count(["fuel","101FLK"])==1:
      self.fuel-=1
    # Engine power loss
    if self.faults.count(["engine","200ENG"])==1 and self.thrust==DLM_MAX_THRUST:
      self.thrust*=0.7
    # Navigation system false output
    if self.faults.count(["navigation","300NAV"])==1:
      self.navigation=False
    # Computer system error
    if self.faults.count(["computer","400CPU"])==1:
      if random()>0.2:
        self.displayAlt=randint(0,99999999)
      if random()>0.2:
        self.displayXVel=randint(-99999,99999)
        self.displayYVel=randint(-99999,99999)
    return

class Camera:
  def __init__(self,x=0,y=0,w=get_screen_dim()[0],h=get_screen_dim()[1],z=1):
    self.x=x
    self.y=y
    self.width=w
    self.height=h
    self.zoom=z
    self.gridRef=[0,0]
    self.prevGR=[]
    self.frameXY=[x-w/2,x+w/2,y-h/2,y+h/2]
    self.bgNum=1

# Updates grid ref. containing target obj. 
  def updGridRef(self,objPosX,objPosY):
    if objPosX>0:
      self.gridRef[0]=trunc((objPosX+self.width/2)/self.width)
    else:
      self.gridRef[0]=trunc((objPosX-self.width/2)/self.width)
    if objPosY>0:
      self.gridRef[1]=trunc((objPosY+self.height/2)/self.height)
    else:
      self.gridRef[1]=trunc((objPosY-self.height/2)/self.height)
    return

# Selects correct background image slide.
  def bgImgNum(self):
    r=0
    if self.prevGR!=self.gridRef:
      self.frameXY=self.grFrameXY()
      if self.frameXY[2]>0:
        r=randint(1,6)
        while r==self.bgNum:
          r=randint(1,6)
        self.bgNum=r
      else:
        r=randint(7,9)
        while r==self.bgNum:
          r=randint(7,9)
        self.bgNum=r
      return

# Calculates grid frame XY coordinates.
  def grFrameXY(self):
    return [self.gridRef[0]*self.width-0.5*self.width,self.gridRef[0]*self.width+0.5*self.width,self.gridRef[1]*self.height-0.5*self.height,self.gridRef[1]*self.height+0.5*self.height]

# Returns target obj. frame XY coordinates.
  def objTrackFrame(self,objPosX,objPosY):
    return [objPosX-self.width/2,objPosX+self.width/2,objPosY-self.height/2,objPosY+self.height/2]

# Zoom on target
  def zoomXY(self,posX,posY,mag):
    x1=0
    x2=0
    y1=0
    y2=0
    winW=self.width*mag
    winH=self.height*mag
    winXY=[]
    
    x1=int(posX-(winW/2))
    x2=int(posX+(winW/2))
    y1=int(posY-(winH/2))
    y2=int(posY+(winH/2))
    
    winXY.append(x1)
    winXY.append(x2)
    winXY.append(y1)
    winXY.append(y2)
    
    return winXY

# 
