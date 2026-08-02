####################
# ₀º°·∘ℙℎγšχ ξğïε ∘·°º₀ 
#           τεrraη_χ '23
####################
from math import *
################
#Engine
################
global G_CONST # Gravitational constant
G_CONST=6.67*10**(-11)

def gravity(objs,delta):
  xD=0 # x displacement
  yD=0 # y displacement
  xF=0 # x force
  yF=0 # y force
  disp=0 # Displacement
  lstIdx=len(objs)-1 # Object array final index
  
  if len(objs)>1:
    for i in range(0,lstIdx):
      for j in range(i+1,lstIdx+1):
        # Distance between objects calc
        xD=objs[i].pos[0]-objs[j].pos[0]
        yD=objs[i].pos[1]-objs[j].pos[1]
        disp=sqrt(xD**2+yD**2)
        
        # Force of gravity calc
        gForce=G_CONST*objs[i].mass*objs[j].mass*disp**(-2)
        xF=(xD*disp**-1)*gForce
        yF=(yD*disp**-1)*gForce
        
        # New acceleration calc, sign inversion for attraction
        objs[i].accel.coord[0]+=-1*xF*(objs[i].mass)**(-1)
        objs[j].accel.coord[0]+=xF*(objs[j].mass)**(-1)
        objs[i].accel.coord[1]+=-1*yF*(objs[i].mass)**(-1)
        objs[j].accel.coord[1]+=yF*(objs[j].mass)**(-1)
      
      # Calc new velocities
      objs[i].vel.coord[0]+=objs[i].accel.coord[0]*delta
      objs[i].vel.coord[1]+=objs[i].accel.coord[1]*delta
      
      # Calc new positions
      objs[i].pos[0]+=objs[i].vel.coord[0]*delta
      objs[i].pos[1]+=objs[i].vel.coord[1]*delta
      
      # Reset acceleration
      objs[i].accel.coord[0]=0
      objs[i].accel.coord[1]=0
      
    # Final obj velocity
    objs[lstIdx].vel.coord[0]+=objs[lstIdx].accel.coord[0]*delta
    objs[lstIdx].vel.coord[1]+=objs[lstIdx].accel.coord[1]*delta
    
    # Final obj position
    objs[lstIdx].pos[0]+=objs[lstIdx].vel.coord[0]*delta
    objs[lstIdx].pos[1]+=objs[lstIdx].vel.coord[1]*delta
    
    # Reset acceleration final obj
    objs[lstIdx].accel.coord[0]=0
    objs[lstIdx].accel.coord[1]=0
  
  return

################
#Objects
################
class object:
  def __init__(self,x,y,m,a=0,ad=0,v=0,vd=0,t="object"):
    self.accel=vector(a,ad)
    self.vel=vector(v,vd)
    self.pos=[x,y]
    self.mass=m
    self.type=t

################
#Vector class
################
class vector:
  def __init__(self,m=0,d=0):
    d=radians(d)
    self.mag=m
    self.coord=[m*cos(d),m*sin(d)]
# 
