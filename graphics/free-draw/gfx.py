#================================
from ti_draw import *
from sys import *
from ti_system import *
import ti_plotlib as plt
#================================
def drawGFX(env,cMenu):
  use_buffer()
  if env.state==0:
    set_window(env.zoomXY[0],env.zoomXY[1],env.zoomXY[2],env.zoomXY[3])
    clear()
    if env.grid==1:
      plt.grid(10,10,"dotted")
    drawObjects(env.objArr)
    drawGhostShape(env.ghstShp)
    drawHUD(env)
  elif env.state==1:
    if not cMenu.gradWhlFlag: #Flags prevent redraw of colour/gradient wheels for better performance.
      clear_rect(cMenu.wheelX+cMenu.wheelW,0,env.winX-(cMenu.wheelX+cMenu.wheelW),env.winY)
    else:
      clear_rect(cMenu.wheelX+cMenu.wheelW,0,env.winX-(cMenu.wheelX+cMenu.wheelW),2/5*env.winY)
    if not cMenu.wheelFlag:
      set_window(0,env.winX,0,env.winY)
      clear()
      drawCWheel(cMenu)
      cMenu.wheelFlag=True
    drawCMenu(cMenu)
  elif env.state==2:
    set_window(0,env.winX,0,env.winY)
    clear()
    drawHelp(env)
  elif env.state==3:
    drawExitMenu(env)
  elif env.state==4:
    drawSaveMenu(env)
  paint_buffer()
  return

def drawObjects(objArr):
  for i in range(len(objArr)):
    set_color(objArr[i].colour[0],objArr[i].colour[1],objArr[i].colour[2])
    if objArr[i].type=="rectangle":
      if objArr[i].fill==-1:
        draw_rect(objArr[i].x,objArr[i].y,objArr[i].width,objArr[i].height)
      else:
        fill_rect(objArr[i].x,objArr[i].y,objArr[i].width,objArr[i].height)
    elif objArr[i].type=="circle":
      if objArr[i].fill==-1:
        draw_circle(objArr[i].x,objArr[i].y,objArr[i].radius)
      else:
        fill_circle(objArr[i].x,objArr[i].y,objArr[i].radius)
    elif objArr[i].type=="line":
      draw_line(objArr[i].x,objArr[i].y,objArr[i].x2,objArr[i].y2)
    elif objArr[i].type=="arc":
      if objArr[i].fill==-1:
        draw_arc(objArr[i].x,objArr[i].y,objArr[i].width,objArr[i].height,objArr[i].angle1,objArr[i].angle2)
      else:
        fill_arc(objArr[i].x,objArr[i].y,objArr[i].width,objArr[i].height,objArr[i].angle1,objArr[i].angle2)
    elif objArr[i].type=="polygon":
      if objArr[i].fill==-1:
        draw_poly(objArr[i].x,objArr[i].y)
      else:
        fill_poly(objArr[i].x,objArr[i].y)
  return

def drawGhostShape(ghost):
  if ghost!=[]:
    for i in range(len(ghost)):
      set_color(ghost[i].colour[0],ghost[i].colour[1],ghost[i].colour[2])
      if ghost[i].type=="rectangle":
        if ghost[i].fill==-1:
          draw_rect(ghost[i].x,ghost[i].y,ghost[i].width,ghost[i].height)
        else:
          fill_rect(ghost[i].x,ghost[i].y,ghost[i].width,ghost[i].height)
      elif ghost[i].type=="circle":
        if ghost[i].fill==-1:
          draw_circle(ghost[i].x,ghost[i].y,ghost[i].radius)
        else:
          fill_circle(ghost[i].x,ghost[i].y,ghost[i].radius)
      elif ghost[i].type=="line":
        draw_line(ghost[i].x,ghost[i].y,ghost[i].x2,ghost[i].y2)
      elif ghost[i].type=="arc":
        if ghost[i].fill==-1:
          draw_arc(ghost[i].x,ghost[i].y,ghost[i].width,ghost[i].height,ghost[i].angle1,ghost[i].angle2)
        else:
          fill_arc(ghost[i].x,ghost[i].y,ghost[i].width,ghost[i].height,ghost[i].angle1,ghost[i].angle2)
      elif ghost[i].type=="polygon":
        if ghost[i].fill==-1:
          draw_poly(ghost[i].x,ghost[i].y)
        else:
          fill_poly(ghost[i].x,ghost[i].y)
  
  return

def drawHUD(env):
  symOM=""
  symBP=""
  
  if env.visibleHUD==1:
    #Drawing tool indicator
    set_color(env.hudClr[0],env.hudClr[1],env.hudClr[2])
    if env.curOM=="rectangle":
      symOM="▫"
    elif env.curOM=="circle":
      symOM="Ο"
    elif env.curOM=="line":
      symOM="—"
      draw_text(env.zoomXY[0]+(string_size("Tool: "+symOM)[0]*env.winScale),env.zoomXY[2]," Thickness: "+str(env.lineThk))
    elif env.curOM=="arc":
      symOM="∡"
    elif env.curOM=="brush":
      symOM="==C>"
      if env.brshPrfl==-1:
        symBP="▫"
      else:
        symBP="Ο"
      draw_text(env.zoomXY[0]+(string_size("Tool: "+symOM)[0]*env.winScale),env.zoomXY[2]," Thickness: "+str(env.brushThk))
      draw_text(env.zoomXY[0]+(string_size("Tool: "+symOM+" Thickness: "+str(env.brushThk))[0]*env.winScale),env.zoomXY[2]," Profile: "+symBP)
    elif env.curOM=="polygon":
      symOM="★"
    draw_text(env.zoomXY[0],env.zoomXY[2],"Tool: "+symOM)
    
    #Pointer position
    draw_text(env.zoomXY[1]-(string_size("X:"+str(env.mPos[0])+" Y:"+str(env.mPos[1]))[0]*env.winScale),env.zoomXY[2],"X:"+str(env.mPos[0])+" Y:"+str(env.mPos[1]))
    
    #Fill and colour indicator
    set_color(env.colour[0],env.colour[1],env.colour[2])
    if env.fill==1:
      fill_circle(env.zoomXY[1]-(33/30*string_size("X:"+str(env.mPos[0])+" Y:"+str(env.mPos[1]))[0]*env.winScale),env.zoomXY[2]+1/31*(env.zoomXY[3]-env.zoomXY[2]),1/64*(env.zoomXY[1]-env.zoomXY[0]))
    else:
      draw_circle(env.zoomXY[1]-(33/30*string_size("X:"+str(env.mPos[0])+" Y:"+str(env.mPos[1]))[0]*env.winScale),env.zoomXY[2]+1/31*(env.zoomXY[3]-env.zoomXY[2]),1/64*(env.zoomXY[1]-env.zoomXY[0]))
    
    #Magnification indicator
    set_color(env.hudClr[0],env.hudClr[1],env.hudClr[2])
    draw_text(env.zoomXY[1]-(string_size(str(env.magLvl)+"x")[0]*env.winScale),env.zoomXY[3]-(string_size(str(env.magLvl)+"x")[1]*env.winScale),str(env.magLvl)+"x")
  
  return

def drawExitMenu(env):
  set_color(245,245,245)
  fill_rect((2*env.zoomXY[0]+env.zoomXY[1])/3,(2*env.zoomXY[2]+env.zoomXY[3])/3,(env.zoomXY[1]-env.zoomXY[0])/3,(env.zoomXY[3]-env.zoomXY[2])/3)
  set_color(0,0,0)
  draw_rect((2*env.zoomXY[0]+env.zoomXY[1])/3,(2*env.zoomXY[2]+env.zoomXY[3])/3,(env.zoomXY[1]-env.zoomXY[0])/3,(env.zoomXY[3]-env.zoomXY[2])/3)
  draw_rect((147*env.zoomXY[0]+78*env.zoomXY[1])/225,(147*env.zoomXY[2]+78*env.zoomXY[3])/225,(23/75)*(env.zoomXY[1]-env.zoomXY[0]),(114/375)*(env.zoomXY[3]-env.zoomXY[2]))
  draw_text((15*env.zoomXY[0]+11*env.zoomXY[1])/26,(13*env.zoomXY[2]+11*env.zoomXY[3])/24,"Exit? y/n")
  
  return

def drawSaveMenu(env):
  set_color(245,245,245)
  fill_rect((2*env.zoomXY[0]+env.zoomXY[1])/3,(2*env.zoomXY[2]+env.zoomXY[3])/3,(env.zoomXY[1]-env.zoomXY[0])/3,(env.zoomXY[3]-env.zoomXY[2])/3)
  set_color(0,0,0)
  draw_rect((2*env.zoomXY[0]+env.zoomXY[1])/3,(2*env.zoomXY[2]+env.zoomXY[3])/3,(env.zoomXY[1]-env.zoomXY[0])/3,(env.zoomXY[3]-env.zoomXY[2])/3)
  draw_rect((147*env.zoomXY[0]+78*env.zoomXY[1])/225,(147*env.zoomXY[2]+78*env.zoomXY[3])/225,(23/75)*(env.zoomXY[1]-env.zoomXY[0]),(114/375)*(env.zoomXY[3]-env.zoomXY[2]))
  draw_text((13*env.zoomXY[0]+9*env.zoomXY[1])/22,(13*env.zoomXY[2]+11*env.zoomXY[3])/24,"Save? y/n")
  
  return

def drawSaveNote(env):
  set_color(245,245,245)
  fill_rect((2*env.zoomXY[0]+env.zoomXY[1])/3,(2*env.zoomXY[2]+env.zoomXY[3])/3,(env.zoomXY[1]-env.zoomXY[0])/3,(env.zoomXY[3]-env.zoomXY[2])/3)
  set_color(0,0,0)
  draw_rect((2*env.zoomXY[0]+env.zoomXY[1])/3,(2*env.zoomXY[2]+env.zoomXY[3])/3,(env.zoomXY[1]-env.zoomXY[0])/3,(env.zoomXY[3]-env.zoomXY[2])/3)
  draw_rect((147*env.zoomXY[0]+78*env.zoomXY[1])/225,(147*env.zoomXY[2]+78*env.zoomXY[3])/225,(23/75)*(env.zoomXY[1]-env.zoomXY[0]),(114/375)*(env.zoomXY[3]-env.zoomXY[2]))
  draw_text((9*env.zoomXY[0]+7*env.zoomXY[1])/16,(13*env.zoomXY[2]+11*env.zoomXY[3])/24,"Saved")
  paint_buffer()
  wait(1)
  
  return

def drawExportNote(env):
  set_color(245,245,245)
  fill_rect((2*env.zoomXY[0]+env.zoomXY[1])/3,(2*env.zoomXY[2]+env.zoomXY[3])/3,(env.zoomXY[1]-env.zoomXY[0])/3,(env.zoomXY[3]-env.zoomXY[2])/3)
  set_color(0,0,0)
  draw_rect((2*env.zoomXY[0]+env.zoomXY[1])/3,(2*env.zoomXY[2]+env.zoomXY[3])/3,(env.zoomXY[1]-env.zoomXY[0])/3,(env.zoomXY[3]-env.zoomXY[2])/3)
  draw_rect((147*env.zoomXY[0]+78*env.zoomXY[1])/225,(147*env.zoomXY[2]+78*env.zoomXY[3])/225,(23/75)*(env.zoomXY[1]-env.zoomXY[0]),(114/375)*(env.zoomXY[3]-env.zoomXY[2]))
  draw_text((7*env.zoomXY[0]+5*env.zoomXY[1])/12,(13*env.zoomXY[2]+11*env.zoomXY[3])/24,"Exported")
  paint_buffer()
  wait(1)
  
  return

def drawCWheel(cMenu):
  for i in range(0,60):
    set_color(255,int(i*(255/60)),0)
    fill_arc(cMenu.wheelX,cMenu.wheelY,cMenu.wheelW,cMenu.wheelH,i,(360/60))
    set_color(255-int(i*(255/60)),255,0)
    fill_arc(cMenu.wheelX,cMenu.wheelY,cMenu.wheelW,cMenu.wheelH,i+60,(360/60))
    set_color(0,255,int(i*(255/60)))
    fill_arc(cMenu.wheelX,cMenu.wheelY,cMenu.wheelW,cMenu.wheelH,i+120,(360/60))
    set_color(0,255-int(i*(255/60)),255)
    fill_arc(cMenu.wheelX,cMenu.wheelY,cMenu.wheelW,cMenu.wheelH,i+180,(360/60))
    set_color(int(i*(255/60)),0,255)
    fill_arc(cMenu.wheelX,cMenu.wheelY,cMenu.wheelW,cMenu.wheelH,i+240,(360/60))
    set_color(255,0,255-int(i*(255/60)))
    fill_arc(cMenu.wheelX,cMenu.wheelY,cMenu.wheelW,cMenu.wheelH,i+300,(360/60))
  return

def drawCMenu(cMenu):
  if cMenu.mseInCWhlBnds:
    clear_rect(cMenu.wheelX+cMenu.wheelW,cMenu.winY,cMenu.winX-(cMenu.wheelX+cMenu.wheelW),cMenu.winY)
    if 0<=cMenu.mseWhlTheta<60:
      cMenu.previewClr=[255,int(cMenu.mseWhlTheta*(255/60)),0]
    elif 60<=cMenu.mseWhlTheta<120:
      cMenu.previewClr=[255-int((cMenu.mseWhlTheta-60)*(255/60)),255,0]
    elif 120<=cMenu.mseWhlTheta<=180:
      cMenu.previewClr=[0,255,int((cMenu.mseWhlTheta-120)*(255/60))]
    elif -180<=cMenu.mseWhlTheta<-120:
      cMenu.previewClr=[0,255-int((cMenu.mseWhlTheta+180)*(255/60)),255]
    elif -120<=cMenu.mseWhlTheta<-60:
      cMenu.previewClr=[int((cMenu.mseWhlTheta+120)*(255/60)),0,255]
    elif -60<=cMenu.mseWhlTheta<0:
      cMenu.previewClr=[255,0,255-int((cMenu.mseWhlTheta+60)*(255/60))]
    
    set_color(cMenu.previewClr[0],cMenu.previewClr[1],cMenu.previewClr[2])
    fill_circle(cMenu.gWhlXC,1/4*cMenu.rRibY,cMenu.rRibX/8)
    set_color(0,0,0)
    draw_text((10/9)*cMenu.rRibX,1/25*cMenu.rRibY,"R: "+str(cMenu.previewClr[0])+" G: "+str(cMenu.previewClr[1])+" B: "+str(cMenu.previewClr[2]))
    cMenu.gradWhlFlag=False
  elif cMenu.mseInGWhlBnds:
    clear_rect(cMenu.wheelX+cMenu.wheelW,0,cMenu.winX-(cMenu.wheelX+cMenu.wheelW),2/5*cMenu.winY)
    if 0<=cMenu.mseGWhlTheta<120:
      cMenu.previewClr=[int(cMenu.slxnClr[0]-(cMenu.mseGWhlTheta*(cMenu.slxnClr[0]/120))),int(cMenu.slxnClr[1]-(cMenu.mseGWhlTheta*(cMenu.slxnClr[1]/120))),int(cMenu.slxnClr[2]-(cMenu.mseGWhlTheta*(cMenu.slxnClr[2]/120)))]
    elif 120<=cMenu.mseGWhlTheta<240:
      cMenu.previewClr=[0+int((cMenu.mseGWhlTheta-120)*(255/120)),0+int((cMenu.mseGWhlTheta-120)*(255/120)),0+int((cMenu.mseGWhlTheta-120)*(255/120))]
    elif 240<=cMenu.mseGWhlTheta<360:
      cMenu.previewClr=[int(255-((cMenu.mseGWhlTheta-240)*(255-cMenu.slxnClr[0])/120)),int(255-((cMenu.mseGWhlTheta-240)*(255-cMenu.slxnClr[1])/120)),int(255-((cMenu.mseGWhlTheta-240)*(255-cMenu.slxnClr[2])/120))]
    
    set_color(cMenu.previewClr[0],cMenu.previewClr[1],cMenu.previewClr[2])
    fill_circle(cMenu.gWhlXC,1/4*cMenu.rRibY,cMenu.rRibX/8)
    set_color(0,0,0)
    draw_text((14/13)*cMenu.rRibX,1/25*cMenu.rRibY,"R: "+str(cMenu.previewClr[0])+" G: "+str(cMenu.previewClr[1])+" B: "+str(cMenu.previewClr[2]))
  elif cMenu.slxnClr!=[] and not cMenu.mseInCWhlBnds:
      set_color(cMenu.slxnClr[0],cMenu.slxnClr[1],cMenu.slxnClr[2])
      fill_circle(cMenu.gWhlXC,1/4*cMenu.rRibY,cMenu.rRibX/8)
      set_color(0,0,0)
      draw_text((14/13)*cMenu.rRibX,1/25*cMenu.rRibY,"R: "+str(cMenu.slxnClr[0])+" G: "+str(cMenu.slxnClr[1])+" B: "+str(cMenu.slxnClr[2]))
      if not cMenu.gradWhlFlag:
        drawGradWheel(cMenu)
        cMenu.gradWhlFlag=True
  return

def drawGradWheel(cMenu):
  firstClr=cMenu.slxnClr
  scndClr=[0,0,0]
  thrdClr=[255,255,255]
  
  for i in range(0,120):
    firstClr=[abs(int(firstClr[0]-(cMenu.slxnClr[0]/120))),abs(int(firstClr[1]-(cMenu.slxnClr[1]/120))),abs(int(firstClr[2]-(cMenu.slxnClr[2]/120)))]
    scndClr=[abs(int(scndClr[0]+(255/120))),abs(int(scndClr[1]+(255/120))),abs(int(scndClr[2]+(255/120)))]
    thrdClr=[abs(thrdClr[0]-((255-cMenu.slxnClr[0])/120)),abs(thrdClr[1]-((255-cMenu.slxnClr[1])/120)),abs(thrdClr[2]-((255-cMenu.slxnClr[2])/120))]
    if i==120-1:
      firstClr=[0,0,0]
      scndClr=[255,255,255]
      thrdClr=cMenu.slxnClr
    set_color(firstClr[0],firstClr[1],firstClr[2])
    fill_arc(cMenu.gWhlX,cMenu.gWhlY-cMenu.gWhlW,cMenu.gWhlW,cMenu.gWhlH,i,1)
    set_color(scndClr[0],scndClr[1],scndClr[2])
    fill_arc(cMenu.gWhlX,cMenu.gWhlY-cMenu.gWhlW,cMenu.gWhlW,cMenu.gWhlH,120+i,1)
    set_color(int(thrdClr[0]),int(thrdClr[1]),int(thrdClr[2]))
    fill_arc(cMenu.gWhlX,cMenu.gWhlY-cMenu.gWhlW,cMenu.gWhlW,cMenu.gWhlH,240+i,1)
  return

def drawHelp(env):
  strHt=string_size("abc")[1]
  set_color(255,0,0)
  draw_text(env.winX/2-(1/2*string_size("FreeDraw Help")[0]),9/10*env.winY,"FreeDraw Help")
  set_color(0,0,0)
  draw_line(env.winX/2-(1/2*string_size("FreeDraw Help")[0]),(9/10*env.winY),env.winX/2+(1/2*string_size("FreeDraw Help")[0]),(9/10*env.winY))
  draw_text(0,9/10*env.winY-strHt,"'g' grid on/off")
  draw_text(0,9/10*env.winY-2*strHt,"'v' HUD visibility")
  draw_text(0,9/10*env.winY-3*strHt,"'f' fill on/off")
  draw_text(0,9/10*env.winY-4*strHt,"'c' colour menu")
  draw_text(0,9/10*env.winY-5*strHt,"'esc' cancel/back")
  draw_text(0,9/10*env.winY-6*strHt,"'h' help menu")
  draw_text(0,9/10*env.winY-7*strHt,"'s' save drawing (one slot)")
  draw_text(0,9/10*env.winY-8*strHt,"'o' open saved drawing")
  draw_text(0,9/10*env.winY-9*strHt,"'del' delete last object")
  draw_text(0,9/10*env.winY-10*strHt,"'e' export code to shell")
  draw_text(env.winX/2,9/10*env.winY-strHt,"'+'/'-' zoom in/out") 
  draw_text(env.winX/2,9/10*env.winY-2*strHt,"'('/')' brush/line thickness")
  draw_text(env.winX/2,9/10*env.winY-3*strHt,"',' switch brush profile")
  draw_text(env.winX/2,9/10*env.winY-4*strHt,"'tab' dab brush")
  draw_text(env.winX/2,9/10*env.winY-5*strHt,"'t' cycle drawing tool")
  draw_text(env.winX/2,9/10*env.winY-6*strHt,"'0-9' colour history")
  draw_text(env.winX/2,9/10*env.winY-7*strHt,"'enter' finalise polygon")
  draw_text(env.winX/2,9/10*env.winY-8*strHt,"'down' cycle arc direction")
  draw_text(env.winX/2,9/10*env.winY-9*strHt,"'?!' Selection mode")
  draw_text(env.winX/2,9/10*env.winY-10*strHt,"'+/-' cycle objects in SM")

# 
