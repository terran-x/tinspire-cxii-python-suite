# Vector Class
#================================
from math import *
#================================
class Vector:
  def __init__(self,components,id=""):
    self.comps=components
    self.id=""
    self._x=None
    self._y=None
    self._z=None
    self._norm=None
  def __add__(self,other):
    sumComp=[]
    if len(self.comps)==len(other.comps):
      for i in range(len(self.comps)):
        sumComp.append(self.comps[i]+other.comps[i])
      return Vector(sumComp)
  def __sub__(self,other):
    subComp=[]
    if len(self.comps)==len(other.comps):
      for i in range(len(self.comps)):
        subComp.append(self.comps[i]-other.comps[i])
      return Vector(subComp)
  def __mul__(self,other):
    if len(self.comps)==len(other.comps)==3:
      x=self.comps[1]*other.comps[2]-self.comps[2]*other.comps[1]
      y=self.comps[2]*other.comps[0]-self.comps[0]*other.comps[2]
      z=self.comps[0]*other.comps[1]-self.comps[1]*other.comps[0]
      return Vector([x,y,z])
  def polar(self):
    if len(self.comps)==2:
      return [self.norm,degrees(atan2(self.comps[1],self.comps[0]))]
    else:
      return False
  @property
  def norm(self):
    return self._norm
  @norm.getter
  def norm(self):
    sum=0
    for value in self.comps:
      sum+=value**2
    return sqrt(sum)
  @property
  def x(self):
    return self._x
  @x.getter
  def x(self):
    try:
      if len(self.comps)<4:
        return self.comps[0]
    except:
      return None
  @property
  def y(self):
    return self._y
  @y.getter
  def y(self):
    try:
      if len(self.comps)<4:
        return self.comps[1]
    except:
      return None
  @property
  def z(self):
    return self._z
  @z.getter
  def z(self):
    try:
      if len(self.comps)<4:
        return self.comps[2]
    except:
      return None
# 
