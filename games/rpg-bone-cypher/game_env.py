# Ģąmε•ξŋυιřøŋmεŋŧ
####################
from ti_system import *
from game_logic import *
####################
class GameState:
  def __init__(self):
    self.key=""
    self.delta=0
    self.player=None
    self.npcs=[] # Non-playable characters
    self.bgos=[] # Background objects
    self.gfx=None
    self.state=1
  
  def input(self):
    if self.key=="up" or self.key=="down" or \
    self.key=="left" or self.key=="right":
      if self.player.state!="walk":
        self.player.walk(self.key,self.gfx.scene.current.cellSz)
    elif self.key=="+":
      self.gfx.camera.zoom(2)
    elif self.key=="-":
      self.gfx.camera.zoom(.5)
# Debugging use
#    elif self.key=="m":
#      print(self.gfx.scene.current.matrix)
#    elif self.key==",":
#      print("player tile:",self.player.tile)
#      print(self.player.getAdjTiles(self.player.tile["tile_address"]))
# 
