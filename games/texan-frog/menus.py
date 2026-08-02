####
from ti_draw import *
from ti_system import *
from builtins import *
####
from ti_game import *
from hiscore import *
from globalsettings import *
####

def mainMenu():
  menu="main"
  dim=get_screen_dim()
  w=dim[0]
  h=dim[1]
  x=w/64
  y=h/42
  options=["start","hScore","settings","help","exit"]
  lStep=3
  
  while 1:
    mPos=get_mouse()
    key=get_key()
    use_buffer()
    drawLogo(w,h)
    drawChoices(w,h,lStep,-1,-1,menu,-1,-1,-1)
#    draw_text(245,205,"x:"+str(mPos[0])+" y:"+str(mPos[1]))
    paint_buffer()
    
    if key=="down" or key=="2":
      if lStep<=12:
        lStep+=3
      else:
        lStep=3
    elif key=="up" or key=="8":
      if lStep>=6:
        lStep-=3
      else:
        lStep=15
    elif key=="enter" or key=="center":
      for i in range(0,len(options)):
        if (i+1)*3==lStep:
          return i
    
    if 108<=mPos[1]<=125 and (w/3)<=mPos[0]<=(w*2/3):
      lStep=3
    elif 126<=mPos[1]<=137 and (w/3)<=mPos[0]<=(w*2/3):
      lStep=6
    elif 138<=mPos[1]<=150 and (w/3)<=mPos[0]<=(w*2/3):
      lStep=9
    elif 151<=mPos[1]<=163 and (w/3)<=mPos[0]<=(w*2/3):
      lStep=12
    elif 164<=mPos[1]<=176 and (w/3)<=mPos[0]<=(w*2/3):
      lStep=15
  return

def newHS(score):
  menu="newhiscore"
  dim=get_screen_dim()
  w=dim[0]
  h=dim[1]
  x=w/64
  y=h/42
  idx=0
  name="---"
#  scrBoard=hs_import(recall_list("highscores"))
  
  while 1:
    mPos=get_mouse()
    key=get_key()
    if key!="" and len(key)<2:
      if 97<=ord(key)<=122 or 48<=ord(key)<=57:
        if name[0]=="-":
          name=""
        key=ord(key)
        if idx<=2:
          name+=chr(key)
          idx+=1
          name=str.upper(name)
    elif key=="del" and str.find(name,"-")==-1:
      name=name[:len(name)-1]
      idx-=1
      if len(name)==0:
        name="---"
    elif key=="enter" and len(name)==3 and str.find(name,"-")==-1:
      return name
    use_buffer()
    drawChoices(w,h,-1,name,score,menu,-1,-1,-1)
    paint_buffer()
    
#    if key=="esc":
#      gs.state=-1
#      return
  return

def hScoreMenu():
  menu="hiscores"
  dim=get_screen_dim()
  w=dim[0]
  h=dim[1]
  x=w/64
  y=h/42
  scrBoard=hs_import(recall_list("highscores"))
  
  while 1:
    mPos=get_mouse()
    key=get_key()
    use_buffer()
    drawChoices(w,h,-1,-1,-1,menu,-1,-1,scrBoard)
    paint_buffer()
    
    if key=="esc":
      gs.state=-1
      return
  return

def settingMenu():
  dim=get_screen_dim()
  w=dim[0]
  h=dim[1]
  x=w/64
  y=h/42
  options=["keyset","clrHS","back"]
  lStep=3
  menu="settings"
  clrScores=0
  keymap=recall_value("keymap")
  
  while 1:
    mPos=get_mouse()
    key=get_key()
    use_buffer()
    drawLogo(w,h)
    drawChoices(w,h,lStep,-1,-1,menu,keymap,clrScores,-1)
    paint_buffer()
    
    if key=="down" or key=="2":
      if lStep<=6:
        lStep+=3
      else:
        lStep=3
    elif key=="up" or key=="8":
      if lStep>=6:
        lStep-=3
      else:
        lStep=9
    elif key=="enter" or key=="center":
      if lStep==3:
        if keymap==1:
          keymap=2
        else:
          keymap=1
      elif lStep==6:
        hsBoard=scoreboard("tfscores",[],10)
        store_list("highscores",hs_export(hsBoard.scores))
        clrScores=1
      elif lStep==9:
        store_value("keymap",keymap)
        gs.state=-1
        return
      
    if 108<=mPos[1]<=125 and (w/3)<=mPos[0]<=(w*2/3):
      lStep=3
    elif 126<=mPos[1]<=137 and (w/3)<=mPos[0]<=(w*2/3):
      lStep=6
    elif 138<=mPos[1]<=150 and (w/3)<=mPos[0]<=(w*2/3):
      lStep=9
  return

def helpMenu():
  menu="help"
  dim=get_screen_dim()
  w=dim[0]
  h=dim[1]
  x=w/64
  y=h/42
  
  while 1:
    mPos=get_mouse()
    key=get_key()
    use_buffer()
    drawChoices(w,h,-1,-1,-1,menu,-1,-1,-1)
    paint_buffer()
    
    if key=="esc":
      gs.state=-1
      return
  return

def drawChoices(w,h,lStep,name,score,menu,keymap,clrHs,scrBoard):
  x=w/64
  y=h/42
  
  if menu=="main":
    set_color(0,255,0)
    draw_text((w/2)-(2.4*x),(h/2)+(3*y),"Start")
    draw_text((w/2)-(6.4*x),(h/2)+(6*y),"High Scores")
    draw_text((w/2)-(4.3*x),(h/2)+(9*y),"Settings")
    draw_text((w/2)-(2.1*x),(h/2)+(12*y),"Help")
    draw_text((w/2)-(1.9*x),(h/2)+(15*y),"Exit")
    set_color(255,0,0)
    draw_text(w/3,(h/2-y/5)+(lStep*y),"★")
  
  elif menu=="hiscores":
    set_color(0,0,0)
    fill_rect(0,0,w,h)
    set_color(0,255,0)
    draw_text((w/2-20*x),(3.2*y),"TEXAN FROG HIGH SCORES")
    set_color(240,235,0)
    draw_text((x-2),(6*y),"★★★★★★★★★★★★★★★★★★★★★★★★")
    draw_text((x+6),(42*y)," ★★★★★  (Press \'esc\' to continue!)  ★★★★★ ")
    for i in range(0,len(scrBoard)+2):
      set_color(240,235,0)
      draw_text((x-3),((i+1)*3*y+30),"★")
      draw_text((61*x),((i+1)*3*y+30),"★")
      if i<len(scrBoard):
        set_color(255,0,0)
        draw_text((25*x),((i+1)*3*y+35),scrBoard[i].name)
        set_color(0,255,0)
        draw_text((35*x),((i+1)*3*y+35),scrBoard[i].score)
  
  elif menu=="settings":
    set_color(0,255,0)
    draw_text((w/2)-(7*x),(h/2)+(3*y),"Keymap")
    draw_text((w/2)+(10*x),(h/2)+(3*y),str(keymap))
    draw_text((w/2)-(7.2*x),(h/2)+(6*y),"Clear scores")
    if clrHs:
      draw_text((w/2)+(10*x),(h/2)+(6*y),"-Cleared")
    draw_text((w/2)-(7*x),(h/2)+(9*y),"Back")
    set_color(255,0,0)
    draw_text(w/3,(h/2-y/5)+(lStep*y),"★")
  
  elif menu=="help":
    set_color(0,0,0)
    fill_rect(0,0,w,h)
    set_color(255,0,0)
    draw_text((w/2-6*x),(3*y),"★HELP★")
    set_color(0,255,0)
    draw_text((x),(6*y),"Why did the frog cross the road?")
    draw_text((x),(9*y),"Who knows, but it's your job to stop it from croaking!")
    draw_text((x),(12*y),"Make it to the other side without being run over,")
    draw_text((x),(15*y),"drowned or eaten.")
    set_color(255,0,0)
    draw_text((x),(20*y),"Keymap 1:")
    draw_text((x),(23*y), "Keymap 2:")
    draw_text((w/2-9*x),(27*y), "Bonus pickups")
    set_color(0,255,0)
    draw_text((15*x),(20*y), "keypad \'up,down,left,right\'")
    draw_text((15*x),(23*y), "numpad \'8,2,4,6\'")
    set_color(240,200,0)
    draw_text((x),(31*y), "★")
    set_color(230,230,235)
    draw_text((x),(34*y), "★")
    set_color(240,235,0)
    draw_text((w/2),(31*y), "★")
    set_color(255,0,10)
    draw_text((w/2),(34*y), "▼")
    set_color(0,255,0)
    draw_text((5*x),(31*y), "500 Points")
    draw_text((5*x),(34*y), "1000 Points")
    draw_text((w/2+4*x),(31*y), "2000 Points")
    draw_text((w/2+4*x),(34*y), "1000 Points + 1up")
    draw_text((18*x),(38*y), "(Press \'esc\' to go back)")
    draw_text((10*x),(41*y), "Coded by Cam special thanks to Tim")
  elif menu=="newhiscore":
    set_color(0,0,0)
    fill_rect(0,0,w,h)
    set_color(0,255,0)
    draw_text(w/2-(string_size(str(score)+" points")[0]/2),(h/2-9*y),str(score)+" points")
    draw_text(w/2-21*x,(h/2-6*y), "Nice work, you got a new high score!")
    draw_text(w/2-19*x,(h/2-3*y), "Type your name and press \'enter\':")
    set_color(255,0,0)
    draw_text(w/2-2*x,(h/2+3*y), name)

def drawLogo(w,h):
  x=12
  
  set_color(0,0,0)
  fill_rect(0,0,w,h)
  set_color(0,255,0)
  set_pen("thick","solid")
  draw_line(15+x,20,50+x,15) #T
  draw_line(15+x,24,50+x,19)
  fill_rect(28+x,22,8,35)
  fill_rect(45+x,30,7,27) #E
  draw_line(52+x,32,65+x,32)
  draw_line(52+x,42,60+x,42)
  draw_line(52+x,54,65+x,54)
  draw_line(72+x,28,90+x,58) #X
  draw_line(74+x,30,92+x,56)
  draw_line(72+x,56,90+x,30)
  draw_line(100+x,56,107+x,30) #A
  draw_line(102+x,56,109+x,30)
  draw_line(109+x,30,116+x,56)
  draw_line(102+x,47,114+x,47)
  draw_line(125+x,30,125+x,56) #N
  draw_line(125+x,30,137+x,56)
  draw_line(127+x,30,139+x,56)
  draw_line(141+x,30,141+x,56)
  
  set_color(255,220,0)
  set_pen("thin","solid")
  fill_poly([188+x,148+x,174+x],[56,35,35]) #★
  fill_poly([148+x,188+x,162+x],[56,35,35])
  fill_poly([162+x,168+x,174+x],[35,25,35])
  
  set_color(0,255,0)
  set_pen("thick","solid")
  draw_line(195+x,22,195+x,56) #F
  draw_line(197+x,22,197+x,56)
  draw_line(197+x,23,220+x,20)
  draw_line(197+x,25,220+x,22)
  draw_line(195+x,37,210+x,37)
  draw_line(217+x,32,217+x,56) #R
  draw_line(220+x,34,223+x,34)
  draw_arc(219+x,34,10,10,270,200)
  draw_line(222+x,44,231+x,56)
  draw_arc(238+x,34,10,19,90,180) #O
  draw_line(242+x,34,247+x,34)
  draw_line(242+x,54,247+x,54)
  draw_arc(243+x,34,10,19,268,182)
  draw_arc(262+x,34,12,19,90,180) #G
  draw_line(266+x,34,276+x,34)
  draw_line(268+x,54,274+x,54)
  draw_line(276+x,44,276+x,56)
  
  set_pen("medium","solid")
  draw_line(25+x,64,278+x,64)

def lvlFinish(level):
  key=get_key()
  x=level.viewW/64
  y=level.viewH/42
  
  set_color(0,0,0)
  fill_rect(0,0,level.viewW,level.viewH)
  set_color(0,255,0)
  draw_text(level.viewW/3.5,level.viewH/2,"★ ζεγεζ " + str(level.num)+ " σmρζετε ★")
  draw_text(level.viewW/2.3,level.viewH/2+3*y,str(level.score)+" ρτs")
  paint_buffer()
  while 1:
    key=get_key()
    if key!="":
      return 1

def gameover(score):
  dim=get_screen_dim()
  w=dim[0]
  h=dim[1]
  x=w/64
  y=h/42
  key=get_key()
  
  set_color(0,0,0)
  fill_rect(0,0,w,h)
  set_color(255,0,0)
  draw_text(w/2-8*x,h/2-3*y,"GAME OVER")
  set_color(0,255,0)
  draw_text(w/2-(string_size("Score: "+str(score))[0]/2),h/2,"Score: "+str(score))
  draw_text(w/2-6.7*x,h/2+3*y,"Retry? (y/n)")
  paint_buffer()
  
  while 1:
    key=get_key()
    if key=="y":
      return 1
    elif key=="n":
      return 0

# 
