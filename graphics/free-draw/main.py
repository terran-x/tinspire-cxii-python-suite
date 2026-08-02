#================================
#
#                    ▫--®ξ∈ÐřΛω--▫
#                                                           τεrraη_χ '24
#================================
from ti_system import *
from gfx import *
from interface import *
from sys import *
from ti_plotlib import *
from splashscreen import *
#================================
def main():
#  fdSplash(2)
  
  delta=0
  loopTime=0
  runTime=0
  env=Environment()
  clrMenu=ColourMenu()
  help=Help()
  slxnMd=SlxnMode()
  
  window(0,(155/159)*env.winX,0,(210/212)*env.winY)
  set_window(0,env.winX,0,env.winY)

  while 1:
    loopTime=get_time_ms()
    runTime+=delta
    
    env.mPos=list(get_mouse())
    # Pointer position corrections for zoom level.
    env.mPos[0]=int(env.mPos[0]*env.winScale+env.zoomXY[0])
    env.mPos[1]=int((env.winY-env.mPos[1])*env.winScale+env.zoomXY[2]) # Also corrects Y-axis inversion.
    
    env.key=get_key()
    
    if env.state==-1:
      break
    elif env.state==0 and env.slxnMode==-1:
      env.input()
    elif env.state==0 and env.slxnMode:
      slxnMd.input(env)
    elif env.state==1:
      clrMenu.input(env)
    elif env.state==2:
      help.input(env)
    elif env.state==3:
      if env.key=="y" or env.key=="enter":
        env.state=4
      elif env.key=="n" or env.key=="esc":
        env.state=0
    elif env.state==4:
      if env.key=="y" or env.key=="enter":
        env.saveImg()
        drawSaveNote(env)
        drawExportNote(env)
        env.state=-1
      elif env.key=="n" or env.key=="esc":
        drawExportNote(env)
        env.state=-1
    
    drawGFX(env,clrMenu)
    
    delta=(get_time_ms()-loopTime)/1000
  env.exportImg()
  return

main()
exit()

# 
