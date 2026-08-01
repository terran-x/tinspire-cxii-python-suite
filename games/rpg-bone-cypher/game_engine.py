# 2Ð Ģąmε•ξŋğιŋε
####################
from ti_system import *
from objects import *
from game_logic import *
from game_env import GameState
from gfx import GFXManager
####################
# Initialises engine and runs game loop
def run():
  loopTime=0
  runTime=0
  env=GameState()
  env.player=Warrior()
  env.gfx=GFXManager(env.player,env.npcs,env.bgos)
  env.player.scene=env.gfx.scene.current # Only for clipping
  while 1:
    loopTime=get_time_ms()
    runTime+=env.delta
    env.key=get_key()
    env.input()
    env.gfx.render(env.delta)
    env.delta=(get_time_ms()-loopTime)/1000

run()
