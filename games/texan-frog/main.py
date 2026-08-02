################################
#
#                    TEXAN★FROG
#                    ¯¯¯¯¯¯¯¯¯¯¯¯¯¯
#                                                       τεrraη_χ '23
################################
from time import *
from ti_system import *
from ti_draw import *
from sys import *
####
from Level import *
from menus import *
from globalsettings import *
from ti_game import *
from hiscore import *
####

def main():
  loopTime=get_time_ms()
  runTime=0
  key=""
  dead=0
  r=0
  finalScore=0
  hsBoard=scoreboard("tfscores",[],10)
  try:
    keymap=recall_value("keymap")
  except:
    keymap=store_value("keymap",1)
  try:
    hiScrs=recall_list("highscores")
    hiScrs=hs_import(hiScrs)
    for i in range(0,len(hiScrs)):
      hsBoard.scores[i]=hiScrs[i]
  except:
    store_list("highscores",hs_export(hsBoard.scores))
  
  while 1:
    if gs.state==-1:
      gs.state=mainMenu()
      if gs.state==0:
        loopTime=get_time_ms()
        level=Level(1,2,15000,keymap)
      elif gs.state==1:
        hScoreMenu()
        continue
      elif gs.state==2:
        settingMenu()
        hiScrs=recall_list("highscores")
        hiScrs=hs_import(hiScrs)
        for i in range(0,len(hiScrs)):
          hsBoard.scores[i]=hiScrs[i]
        continue
      elif gs.state==3:
        helpMenu()
        continue
      elif gs.state==4:
        exit()
      else:
        exit()
        
    delta=(get_time_ms()-loopTime)/1000
    loopTime=get_time_ms()
    runTime+=delta
    delay=0
    
    key=get_key()
    dead=level.update(delta,key)
    if dead==1:
      wait(2)
      loopTime=get_time_ms()
      if level.lives==0:
        clear()
        runTime=0
        newScore=hscore("NEW",finalScore)
        if hsBoard.update(newScore):
          newScore.name=newHS(newScore.score)
          store_list("highscores",hs_export(hsBoard.scores))
          hScoreMenu()
        r=gameover(finalScore)
        if r==1:
          finalScore=0
          loopTime=get_time_ms()
          gs.state=0
          level=Level(1,2,15000,level.input)
        elif r==0:
          gs.state=-1
          loopTime=get_time_ms()
          continue
      else:
        level.score-=3000
        level=Level(level.num,(level.lives-1),level.score,level.input)
    elif dead==0:
      use_buffer()
      level.draw()
      paint_buffer()
      level.score-=int(((runTime-10)/10)*1500)
      wait(1)
      if level.score<0:
        level.score=0
      finalScore+=level.score
      lvlFinish(level)
      loopTime=get_time_ms()
      runTime=0
      if level.num<=99:
        level=Level(level.num+1,2,15000,level.input)
      else:
        gs.state=-1
        continue
    use_buffer()
    level.draw()
    paint_buffer()
    level.lastKey=key
  return

main()

# 
