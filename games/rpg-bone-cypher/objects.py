# Ǿbĵεŧş
####################
from gfx import AniController
import sys
####################
# Character sprites.
WAR_SPR=[["wfs(","wfr(","wfl("],["wrs(","wrr(","wrl("],\
["wlp(","wlp_rs(","wlp_ls("],["wrp(","wrp_ls(","wrp_rs("]]
#MAG_SPRITES=
#ROG_SPRITES=
# Character state
STATE=["idle","walk","attack","defend","cast"]
####################
class Object:
  def __init__(self,x=0,y=0,w=1,h=1,dir="down",scene=None,type=""):
    self.x=x
    self.y=y
    self.w=w
    self.h=h
    self.dir=dir
    self.type=type
    self.scene=scene
    self._tile=None
  
  def calcRect(self):
    # [x1,x2,y1,y2]
    return [self.x-.5*self.w,self.x+.5*self.w,\
         self.y-.5*self.h, self.y+.5*self.h]
  
  @property
  def tile(self): 
    return self._tile
  @tile.getter 
  def tile(self):
    grd=self.scene.grid # Map tile grid
    for i in range(len(grd)): # Grid row
      for j in range(len(grd[i])): # Grid column
        # Get current cell.
        if grd[i][j]["pxl_address"][0]<self.x<=\
        grd[i][j]["pxl_address"][0]+grd[i][j]["size"] and \
        grd[i][j]["pxl_address"][1]<self.y<=\
        grd[i][j]["pxl_address"][1]+grd[i][j]["size"]:
          return grd[i][j]
    return

class Character(Object):
  def __init__(self,x,y,w,h,hp,stats={"str":1,"spd":1,"wlk":1}):
    Object.__init__(self,x,y,w,h)
    self.hp=hp
    self.stats=stats
    self.sprites=WAR_SPR
    self.inventory=[]
    self.sprite=self.sprites[0][0]
    self.state=STATE[0]
    self.animate=AniController(self)
  
  # Sets character state and direction properties.
  def walk(self,keyDir,dist):
    # Face new dir or walk if already facing that dir.
    if self.dir==keyDir:
      if keyDir in self.canWalk(keyDir):
        self.state=STATE[1]
    else:
      self.dir=keyDir
  
  #  Checks for obstructions in walking path.
  def canWalk(self,drxn):
    walkDirs=["left","right","up","down"]
    aTiles=self.getAdjTiles(self.tile["tile_address"])
    if drxn=="left":
      if aTiles[0]==-1 or aTiles[0]["type"]==-1:
        walkDirs.remove(drxn)
    if drxn=="right":
      if aTiles[1]==-1 or aTiles[1]["type"]==-1:
        walkDirs.remove(drxn)
    if drxn=="up":
      if aTiles[2]==-1 or aTiles[2]["type"]==-1:
        walkDirs.remove(drxn)
    if drxn=="down":
      if aTiles[3]==-1 or aTiles[3]["type"]==-1:
        walkDirs.remove(drxn)
    return walkDirs
  
  def getAdjTiles(self,ctileAdd):
    aTiles=[-1,-1,-1,-1] # Adjacent tiles; [L,R,U,D]; -1 if none.
    try:
      if ctileAdd[1]!=0:
        aTiles[0]=self.scene.grid[ctileAdd[0]][ctileAdd[1]-1]
    except:
      1
    try:
      aTiles[1]=self.scene.grid[ctileAdd[0]][ctileAdd[1]+1]
    except:
      1
    try:
      if ctileAdd[0]!=0:
        aTiles[2]=self.scene.grid[ctileAdd[0]-1][ctileAdd[1]]
    except:
      1
    try:
      aTiles[3]=self.scene.grid[ctileAdd[0]+1][ctileAdd[1]]
    except:
      1
    return aTiles

class Warrior(Character):
  def __init__(self,x=0,y=0,w=12,h=26,hp=100,ap=100,stats={"str":30,"spd":20,"wlk":40},inventory=[]):
    Character.__init__(self,x,y,w,h,hp,stats)
    self.type="warrior"
    self.ap=ap
    self.inventory=inventory
