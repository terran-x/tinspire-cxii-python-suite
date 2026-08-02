#=======================
#
#                 LΛΝDΞR  
#                                      τεrraη_χ '24
#=======================
from game import *
from gfx import *
from sys import *
from ti_system import *
#=======================
def main():
  delta=0
  loopTime=0
  runTime=0
  hiScrs=[]
  
  # Initialise environment
  env=Environment()
  
  # Main loop
  while 1:
    loopTime=get_time_ms()
    runTime+=delta
    
    # Display menus
    if env.state==0:
      if env.displayMenus():
        if env.menus[0].type!="pause":
          env=Environment(env.sim,env.controls,env.debug,env.lz)
        env.state=1
    # Run game/sim
    elif env.state==1:
      env.run_time+=delta
      if env.update(delta):
        drawGFX(env,delta)
        gravity(env.grvArr,delta)
    # Lander destroyed
    elif env.state==2:
      wait(3)
      env.state=0
    # Landed successfully
    elif env.state==3:
      drawGFX(env,delta)
#      if env.hsCheck():
#        print(env.score)
    delta=(get_time_ms()-loopTime)/1000
  return

main()
#=======================
#  Apollo 11: LM Eagle Stats
###Stage 1: Descent module
#Total mass: 15200 kg (wet)
#Propellant mass: 8165 kg
#Maximum thrust: 45.04 kN
#Fuel consumption: ~8.6 kg/s
#     (At max thrust and fuel load)
###Stage 2: Ascent module
#Total mass: 4821 kg (wet)
#Propellant mass: 2376 kg
#Maximum thrust: 15.57 kN
#Fuel consumption: ~8.32 kg/s
#     (At max thrust and fuel load)
###Apollo 11: CM Columbia
#Orbit altitude: 111-130 km
#=======================

# 
