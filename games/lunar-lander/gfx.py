#=======================
from images.py import *
from ti_system import *
from math import *
from random import *
from ti_windows import *
#=======================
def drawGFX(env,delta):
  winXY=[]
  key=""
  
  clear()
  use_buffer()
  if env.camera.zoom==1:
    set_window(env.camera.frameXY[0],env.camera.frameXY[1],env.camera.frameXY[2],env.camera.frameXY[3])
  else:
    winXY=env.camera.zoomXY(env.objArr[0].pos[0],env.objArr[0].pos[1],env.camera.zoom)
    set_window(winXY[0],winXY[1],winXY[2],winXY[3])
  
  bgImg(env.camera.bgNum,env.camera.frameXY[0]+0.5*env.camera.width,env.camera.frameXY[2]+0.5*env.camera.height)
  
  if not env.sim:
    if not env.lReboot:
      drawTarget(env)
  
  if not env.objArr[0].exploding:
    if env.objArr[0].landed:
      if landedAni(env):
        dispScore(env,winXY)
        if get_key(1)=="enter":
          set_window(0,get_screen_dim()[0],0,get_screen_dim()[1])
          if env.hsCheck():
            while key!="enter":
              key=get_key()
              drawHSBd(env)
            env.state=0
          env.state=0
    else:
      drawJet(env)
      drawLander(env)
      if not env.debug:
        if not env.lReboot:
          drawHUD(env,delta)
        else:
          rebooting(env)
      else:
        debugInfo(env)
  elif xplsnAni(env,delta):
    env.objArr[0].destroyed=True
    env.objArr[0].exploding=False
    env.ani_timer=0
  
  paint_buffer()
  return

# New high score
def newHS():
  sDim=get_screen_dim()
  name=inputbox(.5*sDim[0],.5*sDim[1],.4*sDim[0],.5*sDim[1],"New high score!!!, Enter name (3 characters):","",3,[255,0,0]).run()
  if name!=None and len(name)==3:
    return name.upper()
  else:
    name=newHS()
    return name
  return

# Thrust graphics
def drawJet(env):
  if env.objArr[0].fuel>0 and env.objArr[0].throttle>0:
    if env.controls==1:
      if env.key=="left":
        imgAttThrstr("r",env.objArr[0].pos[0],env.objArr[0].pos[1])
      elif env.key=="right":
        imgAttThrstr("l",env.objArr[0].pos[0],env.objArr[0].pos[1])
      elif env.key=="up":
        imgThruster(env.objArr[0].pos[0]+0.5,env.objArr[0].pos[1]-5)
    elif env.controls==-1:
      if env.objArr[0].burn[1]==1:
        imgThruster(env.objArr[0].pos[0]+0.5,env.objArr[0].pos[1]-5)
      if env.objArr[0].burn[0]==1:
        imgAttThrstr("r",env.objArr[0].pos[0],env.objArr[0].pos[1])
      if env.objArr[0].burn[2]==1:
        imgAttThrstr("l",env.objArr[0].pos[0],env.objArr[0].pos[1])
  return

# Lander graphic
def drawLander(env):
  if not env.objArr[0].landed:
    imgBscLndr(env.objArr[0].pos[0],env.objArr[0].pos[1])
  else:
    imgLander(env.objArr[0].pos[0],env.objArr[0].pos[1])
  return

# Lander explosion animation
def xplsnAni(env,delta):
    x=env.camera.width*0.02
    clear()
    env.ani_timer+=delta
    if env.ani_timer<0.1:
      bgImg(env.camera.bgNum,env.camera.frameXY[0]+0.5*env.camera.width-x,env.camera.frameXY[2]+0.5*env.camera.height)
      imgXplsn(1,env.objArr[0].pos[0]-x,env.objArr[0].pos[1])
    elif env.ani_timer<0.2:
      bgImg(env.camera.bgNum,env.camera.frameXY[0]+0.5*env.camera.width+x,env.camera.frameXY[2]+0.5*env.camera.height)
      imgXplsn(1,env.objArr[0].pos[0]+x,env.objArr[0].pos[1])
    elif env.ani_timer<0.3:
      bgImg(env.camera.bgNum,env.camera.frameXY[0]+0.5*env.camera.width-x,env.camera.frameXY[2]+0.5*env.camera.height)
      imgXplsn(1,env.objArr[0].pos[0]-x,env.objArr[0].pos[1])
    elif env.ani_timer<0.4:
      bgImg(env.camera.bgNum,env.camera.frameXY[0]+0.5*env.camera.width+x,env.camera.frameXY[2]+0.5*env.camera.height)
      imgXplsn(2,env.objArr[0].pos[0]+x,env.objArr[0].pos[1])
    elif env.ani_timer<0.5:
      bgImg(env.camera.bgNum,env.camera.frameXY[0]+0.5*env.camera.width-x,env.camera.frameXY[2]+0.5*env.camera.height)
      imgXplsn(2,env.objArr[0].pos[0]-x,env.objArr[0].pos[1])
    elif env.ani_timer<0.6:
      bgImg(env.camera.bgNum,env.camera.frameXY[0]+0.5*env.camera.width+x,env.camera.frameXY[2]+0.5*env.camera.height)
      imgXplsn(2,env.objArr[0].pos[0]+x,env.objArr[0].pos[1])
    elif env.ani_timer<0.7:
      bgImg(env.camera.bgNum,env.camera.frameXY[0]+0.5*env.camera.width-x,env.camera.frameXY[2]+0.5*env.camera.height)
    else:
      # Return true on animation completion
      bgImg(env.camera.bgNum,env.camera.frameXY[0]+0.5*env.camera.width,env.camera.frameXY[2]+0.5*env.camera.height)
      return True
    return False

def landedAni(env):
  bgImg(8,env.camera.frameXY[0]+1.49*env.camera.width,env.camera.frameXY[2]+0.5*env.camera.height)
  bgImg(9,env.camera.frameXY[0]-0.49*env.camera.width,env.camera.frameXY[2]+0.5*env.camera.height)
  set_color(239,239,239)
  fill_rect(env.camera.frameXY[0]-0.49*env.camera.width,env.camera.frameXY[2]-0.5*env.camera.height,2*env.camera.width,0.51*env.camera.height)
  if env.camera.zoom>0.2:
    env.camera.zoom-=0.02
    drawLander(env)
  else:
    # Return true on animation completion
    drawLander(env)
    return True
  return False

def timeDisp(secs):
  min=secs/60
  sec=(min-trunc(min))*60
  return [trunc(min),int(sec)]

def dispScore(env,wxy):
  strHt=4
  tm=timeDisp(env.run_time)
  env.score=env.scrAcc()
  set_color(255,0,0)
  draw_text(wxy[0],wxy[3]-strHt,"Distance from target: "+str(int(fabs(env.lz[0]-env.objArr[0].pos[0])))+"m")
  draw_text(wxy[0]+2/3*(wxy[1]-wxy[0]),wxy[3]-strHt,str(int(env.landScr()))+" pts")
  draw_text(wxy[0],wxy[3]-2*strHt,"Time: "+str(tm[0])+"m "+str(tm[1])+"s")
  draw_text(wxy[0]+2/3*(wxy[1]-wxy[0]),wxy[3]-2*strHt,str(int(env.timeScr()))+" pts")
  draw_text(wxy[0],wxy[3]-3*strHt,"Damage: "+str(int(env.objArr[0].damage))+"%")
  draw_text(wxy[0]+2/3*(wxy[1]-wxy[0]),wxy[3]-3*strHt,str(int(env.dmgScr()))+" pts")
  draw_text(wxy[0],wxy[3]-4*strHt,"Fuel left: "+str(int(env.objArr[0].fuel/env.objArr[0].max_fuel*100))+"%")
  draw_text(wxy[0]+2/3*(wxy[1]-wxy[0]),wxy[3]-4*strHt,str(int(env.fuelScr()))+" pts")
  set_color(0,255,0)
  draw_text(wxy[0],wxy[3]-6*strHt,"FINAL SCORE:")
  draw_text(wxy[0]+2/3*(wxy[1]-wxy[0]),wxy[3]-6*strHt,str(env.score)+" pts")
  paint_buffer()
  return

def drawLogo(x,y):
  imgLogo(x,y)
  return

# Menu graphics
def drawMenu(menu):
  txtDim=[]
  
  clear()
  use_buffer()
  set_window(0,menu.width,0,menu.height)
  
  # Paint background
  set_color(menu.bgColour[0],menu.bgColour[1],menu.bgColour[2])
  fill_rect(0,0,menu.width,menu.height)
  
  # Paint logo
  drawLogo(menu.width*0.5,menu.height-menu.logoDim[1])
  
  # Paint Options
  for i in range(len(menu.options)):
    txtDim=string_size(menu.options[i])
    if menu.step==i+1:
      set_color(menu.indColour[0],menu.indColour[1],menu.indColour[2])
      draw_text((menu.width-txtDim[0])*0.5,(menu.height-2*menu.logoDim[1])-(i+1)*txtDim[1],menu.options[i])
      draw_text(0.25*menu.width,(menu.height-2*menu.logoDim[1])-(i+1)*txtDim[1],"▼")
    else:
      set_color(menu.optColour[0],menu.optColour[1],menu.optColour[2])
      draw_text((menu.width-txtDim[0])*0.5,(menu.height-2*menu.logoDim[1])-(i+1)*txtDim[1],menu.options[i])
  paint_buffer()
  return

# Help screen
def drawHelp(env):
  clear()
  use_buffer()
  imgHelpScr(env)
  paint_buffer()
  return

# High scores board
def drawHSBd(env):
  clear()
  use_buffer()
  imgSBScr(env)
  paint_buffer()
  return

# HUD graphics
def drawHUD(env,delta):
  xVel=str(env.objArr[0].displayXVel)
  yVel=str(env.objArr[0].displayYVel)
  alt=str(env.objArr[0].displayAlt)
  
  imgHUD(env.camera.frameXY[0]+1.12*env.camera.width,env.camera.frameXY[2]+0.39*env.camera.height,env.objArr[0].faults,env.objArr[0].fuel/env.objArr[0].max_fuel,env.objArr[0].throttle*0.1)
  
  # Fuel/thrust labels
  set_color(220,0,0)
  draw_text(env.camera.frameXY[0]+0.94*env.camera.width,env.camera.frameXY[2]+0.94*env.camera.height,"F")
  draw_text(env.camera.frameXY[0]+0.94*env.camera.width,env.camera.frameXY[2]+0.89*env.camera.height,"U")
  draw_text(env.camera.frameXY[0]+0.94*env.camera.width,env.camera.frameXY[2]+0.84*env.camera.height,"E")
  draw_text(env.camera.frameXY[0]+0.94*env.camera.width,env.camera.frameXY[2]+0.79*env.camera.height,"L")
  set_color(0,200,200)
  draw_text(env.camera.frameXY[0]+0.97*env.camera.width,env.camera.frameXY[2]+0.94*env.camera.height,"T")
  draw_text(env.camera.frameXY[0]+0.97*env.camera.width,env.camera.frameXY[2]+0.89*env.camera.height,"H")
  draw_text(env.camera.frameXY[0]+0.97*env.camera.width,env.camera.frameXY[2]+0.84*env.camera.height,"R")
  draw_text(env.camera.frameXY[0]+0.97*env.camera.width,env.camera.frameXY[2]+0.79*env.camera.height,"T")
  
  # Alt/Vel instrument labels
  set_color(150,150,150)
  draw_text(env.camera.frameXY[0],env.camera.frameXY[2]+0.93*env.camera.height,"ALTITUDE")
  draw_text(env.camera.frameXY[0],env.camera.frameXY[2]+0.79*env.camera.height,"VELOCITY")
  draw_text(env.camera.frameXY[0],env.camera.frameXY[2]+0.58*env.camera.height,"ERRORS")
  
  # Alt/Vel instrument data
  set_color(255,130,0)
  if len(xVel)<6:
    draw_text(env.camera.frameXY[0]+0.01*env.camera.width,env.camera.frameXY[2]+0.71*env.camera.height,"H: "+xVel)
  if len(yVel)<6:
    draw_text(env.camera.frameXY[0]+0.01*env.camera.width,env.camera.frameXY[2]+0.66*env.camera.height,"V: "+yVel)
  if len(alt)<9:
    draw_text(env.camera.frameXY[0]+0.01*env.camera.width,env.camera.frameXY[2]+0.86*env.camera.height,alt)
  if env.objArr[0].faults!=[]:
    for i in range(0,len(env.objArr[0].faults)):
      draw_text(env.camera.frameXY[0]+0.01*env.camera.width,env.camera.frameXY[2]+0.515*env.camera.height-12*i,env.objArr[0].faults[i][1])
  
  # Alarm indicators
  if env.objArr[0].fuel_alarm:
    set_color(255,0,0)
  else:
    set_color(80,80,80)
  draw_rect((env.camera.frameXY[0]+0.23*env.camera.width),env.camera.frameXY[2]+0.92*env.camera.height,38,15)
  draw_text((env.camera.frameXY[0]+0.24*env.camera.width),(env.camera.frameXY[2]+0.91*env.camera.height)+2,"FUEL")
  
  if env.objArr[0].dmg_alarm:
    set_color(255,0,0)
  else:
    set_color(80,80,80)
  draw_rect((env.camera.frameXY[0]+0.37*env.camera.width),env.camera.frameXY[2]+0.92*env.camera.height,35,15)
  draw_text((env.camera.frameXY[0]+0.38*env.camera.width),(env.camera.frameXY[2]+0.91*env.camera.height)+2,"DMG")
  
  if env.objArr[0].fault_alarm:
    set_color(255,0,0)
  else:
    set_color(80,80,80)
  draw_rect((env.camera.frameXY[0]+0.505*env.camera.width),env.camera.frameXY[2]+0.92*env.camera.height,33,15)
  draw_text((env.camera.frameXY[0]+0.515*env.camera.width),(env.camera.frameXY[2]+0.91*env.camera.height)+2,"ERR")
  
  warnLight(env,delta)
  drawLZInd(env)
  return

# Warning light graphic
def warnLight(env,delta):
  if env.objArr[0].warn_alarm and env.timer<1:
    set_color(255,0,0)
    draw_rect((env.camera.frameXY[0]+0.5*env.camera.width)-32,env.camera.frameXY[2]+0.5*env.camera.height,64,21)
    draw_text((env.camera.frameXY[0]+0.5*env.camera.width)-31,(env.camera.frameXY[2]+0.5*env.camera.height)+2,"WARNING")
    env.timer+=delta
  elif env.objArr[0].warn_alarm and env.timer<=0:
    env.objArr[0].warn_alarm=False
    env.timer=0
  return

# LZ target graphic
def drawTarget(env):
  if not env.objArr[0].landed:
    imgTarget(env.lz[0],env.lz[1])
  return

# LZ target indicator graphic
def drawLZInd(env):
  if env.LZind and env.objArr[0].navigation:
    imgLZInd(env.LZind[0],env.LZind[1],env.LZind[2])
  return

def rebooting(env):
  set_color(255,0,0)
  draw_text(env.camera.frameXY[0]+0.5*(env.camera.width-string_size("rebooting...")[0]),env.camera.frameXY[2]+0.5*env.camera.height,"Rebooting...")
  return

def debugInfo(env):
  set_color(255,0,0)
# Lander vel
  draw_text(env.camera.frameXY[0]+210,env.camera.frameXY[2],"vX: "+str(int(env.objArr[0].vel.coord[0]))+", vY:"+str(int(env.objArr[0].vel.coord[1])))
# Lander fuel
  draw_text(env.camera.frameXY[0],env.camera.frameXY[2],"Fuel: "+str(int((env.objArr[0].fuel/env.objArr[0].max_fuel)*100))+"%")
# Lander dmg
  draw_text(env.camera.frameXY[0]+75,env.camera.frameXY[2],"Dmg: "+str(int(env.objArr[0].damage))+"%")
# Lander throttle
  draw_text(env.camera.frameXY[0]+145,env.camera.frameXY[2],"Thr: "+str(int((env.objArr[0].throttle*0.1)*100))+"%")
# Lander pos
  draw_text(env.camera.frameXY[0],env.camera.frameXY[3]-38,"X: "+str(int((env.objArr[0].pos[0]))))
  draw_text(env.camera.frameXY[0],env.camera.frameXY[3]-57,"Y: "+str(int((env.objArr[0].pos[1]))))
# Viewport borders
  draw_text(env.camera.frameXY[0],env.camera.frameXY[3]-19,"vXY: ["+str(int(env.camera.frameXY[0]))+", "+str(int(env.camera.frameXY[1]))+", "+str(int(env.camera.frameXY[2]))+", "+str(int(env.camera.frameXY[3]))+"]")
# Grid ref data
  draw_text(env.camera.frameXY[0],env.camera.frameXY[3]-76,"GRef: "+str(env.camera.gridRef))
  draw_text(env.camera.frameXY[0],env.camera.frameXY[3]-95,"PrevGR: "+str(env.camera.prevGR))
# Temporary debug data slot
  draw_text(env.camera.frameXY[0],env.camera.frameXY[3]-95-18,"ind: "+str(env.LZind))
  draw_text(env.camera.frameXY[0],env.camera.frameXY[3]-95-18*2,"runtime: "+str(round(env.run_time,1)))
#  draw_text(env.camera.frameXY[0],env.camera.frameXY[3]-95-18*3,": "+str())
  return

# 
