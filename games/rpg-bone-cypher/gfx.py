# Ģřąρħιş
####################
from ti_draw import *
from bc_images import *
from dungeons import *
from zones import *
####################
# Manages controllers and rendering.
class GFXManager:
  def __init__(self,plyr=None,npcs=None,bgos=None):
    self.player=plyr
    self.npcs=npcs # Non-playable characters
    self.bgo=bgos # Background objects
    self.scene=SceneController()
    self.camera=Camera(self.player.x,self.player.y,self.scene.w,self.scene.h)
    self.hud=HUD()
    
    self.scene.addDungeon()
    self.scene.current=self.scene.dungeons[0]
#    self.scene.addZone(TOWN)
#    self.scene.current=self.scene.zones[0]
    entry=self.scene.current.entry
    self.player.x=entry["pxl_address"][0]+entry["size"]/2
    self.player.y=entry["pxl_address"][1]+entry["size"]/2
    self.player.gridXY=entry["type"]
  
  def render(self,delta):
    x=self.camera.x
    y=self.camera.y
    w=self.camera.w
    h=self.camera.h
    clear()
    use_buffer()
    self.camera.lock(self.player)
    set_window(x-w*.5,x+w*.5,y-h*.5,y+h*.5)
    self.scene.drawBG([0,0,0])
    self.scene.current.draw()
    self.hud.display(x,y,w,h,self.player)
    self.hud.debug(x,y,w,h,delta)
    if self.player.state=="walk":
      self.player.animate.walk(delta)
    else:
      self.player.animate.stand()
    paint_buffer()

## temp hitbox test routine
#  def drawHBox(self):
#    bounds=self.player.calcRect()
#    w=self.player.w
#    h=self.player.h
#    set_color(255,0,0)
#    draw_rect(bounds[0],bounds[2],w,.1*h)

## temp collision test function
#  def showCell(self):
#    cell=self.player.tile
#    if cell!=None:
#      x1=cell["pxl_address"][0]
#      y1=cell["pxl_address"][1]
#      set_color(0,255,0)
#      draw_rect(x1,y1,cell["size"],cell["size"])

# Handles character and object animations.
class AniController:
  def __init__(self,object):
    self.timer=0
    self.step_duration=0.24
    self.step_pause=0.12
    self.startXY=[]
    self.object=object
  
# Handles walking animation and character movement.
# (Movement contained here to sync with animation.)
  def walk(self,delta):
    char=self.object
    if self.timer==0:
      self.startXY=[char.x,char.y]
    self.timer+=delta
    tDist=char.scene.cellSz # Travel distance
    vel=tDist/(self.step_duration*2)
    if char.dir=="down":
      if self.timer<self.step_duration:
        eval(char.sprites[0][1]+"%d,"%char.x+"%d)"%char.y)
        char.y-=vel*delta
      elif self.timer<self.step_duration+self.step_pause:
        eval(char.sprites[0][0]+"%d,"%char.x+"%d)"%char.y)
      elif self.timer<self.step_duration*2+self.step_pause:
        eval(char.sprites[0][2]+"%d,"%char.x+"%d)"%char.y)
        char.y-=vel*delta
      else:
        char.state="idle"
        char.y=self.startXY[1]-tDist
        self.timer=0
    
    elif char.dir=="up":
      if self.timer<self.step_duration:
        eval(char.sprites[1][1]+"%d,"%char.x+"%d)"%char.y)
        char.y+=vel*delta
      elif self.timer<self.step_duration+self.step_pause:
        eval(char.sprites[1][0]+"%d,"%char.x+"%d)"%char.y)
      elif self.timer<self.step_duration*2+self.step_pause:
        eval(char.sprites[1][2]+"%d,"%char.x+"%d)"%char.y)
        char.y+=vel*delta
      else:
        char.state="idle"
        char.y=self.startXY[1]+tDist
        self.timer=0
    
    elif char.dir=="left":
      if self.timer<self.step_duration:
        eval(char.sprites[2][1]+"%d,"%char.x+"%d)"%char.y)
        char.x-=vel*delta
      elif self.timer<self.step_duration+self.step_pause:
        eval(char.sprites[2][0]+"%d,"%char.x+"%d)"%char.y)
      elif self.timer<self.step_duration*2+self.step_pause:
        eval(char.sprites[2][2]+"%d,"%char.x+"%d)"%char.y)
        char.x-=vel*delta
      else:
        char.state="idle"
        char.x=self.startXY[0]-tDist
        self.timer=0
    
    elif char.dir=="right":
      if self.timer<self.step_duration:
        eval(char.sprites[3][1]+"%d,"%char.x+"%d)"%char.y)
        char.x+=vel*delta
      elif self.timer<self.step_duration+self.step_pause:
        eval(char.sprites[3][0]+"%d,"%char.x+"%d)"%char.y)
      elif self.timer<self.step_duration*2+self.step_pause:
        eval(char.sprites[3][2]+"%d,"%char.x+"%d)"%char.y)
        char.x+=vel*delta
      else:
        char.state="idle"
        char.x=self.startXY[0]+tDist
        self.timer=0

# Loads correct sprite when standing. 
  def stand(self):
    char=self.object
    if char.dir=="up":
      eval(char.sprites[1][0]+"%d,"%char.x+"%d)"%char.y)
    elif char.dir=="down":
      eval(char.sprites[0][0]+"%d,"%char.x+"%d)"%char.y)
    elif char.dir=="left":
      eval(char.sprites[2][0]+"%d,"%char.x+"%d)"%char.y)
    elif char.dir=="right":
      eval(char.sprites[3][0]+"%d,"%char.x+"%d)"%char.y)

# Handle drawing of bg scenes (and PCG for open map)
class SceneController:
  def __init__(self):
    self.w=get_screen_dim()[0]
    self.h=get_screen_dim()[1]
    self.dungeons=[]
    self.zones=[]
    self.current=None
  
  def addZone(self,zone):
    self.zones.append(Zone(zone))
  
  def addDungeon(self,w=7,h=10):
    self.dungeons.append(Dungeon(w,h,0,0,26))
  
  def removeDungeon(self):
    self.dungeons.pop()
  
  def drawBG(self,colour=[0,150,0]):
    set_color(0,0,0)
    fill_rect(-318*4,-212*4,8*318,8*212)
    set_color(colour[0],colour[1],colour[2])
    if self.current!=None:
      x=self.current.x
      y=self.current.y
      w=self.current.width
      h=self.current.height
      fill_rect(x-w/2,y-h/2,w,h)

# Game camera controls
class Camera:
  def __init__(self,x,y,w,h):
    self.x=x
    self.y=y
    self.w=w
    self.h=h
    self.magnification=1
    self.zoom(self.magnification)
  
  def zoom(self,mag):
    self.magnification=mag
    self.w/=mag
    self.h/=mag
  
  def lock(self,target):
    if target!=None:
      self.x=target.x
      self.y=target.y
  
  # Write logic for panning boundaries.
  def boundaries(self,x1,y1,x2,y2):
    pass

class HUD:
  def __init__(self,clr=[255,0,0]):
    self.colour=clr
  
  def display(self,x,y,w,h,char):
    set_color(self.colour[0],self.colour[1],self.colour[2])
    draw_text(x-.5*w,y-.5*h,"HP: "+str(char.hp))
    draw_text(x,y-.5*h,"tile:" +str(round(char.gridXY,3)))
  
  def debug(self,x,y,w,h,delta):
    fps=0
    set_color(255,0,0)
    if delta>0:
      fps=1/delta
    draw_text(x+.36*w,y-.5*h,"fps:" +str(round(fps,3)))
