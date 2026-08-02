#================================
#               INTERFACE CONTENTS
#================================
# Environment class methods
#         input                                           line 63
#         zoom                                          line 335
#         mseAngle                                  line 357
#         exportImg                                  line 372
#         saveImg                                     line 453
#         loadClr                                       line 529
#         loadImg                                      line 545
#         xyLimits                                      line 645
# ColourMenu class methods
#         input                                           line 844
#         mseCWhlCheck                       line 859
#         mseGWhlCheck                       line 870
#         exit                                              line 884
# Help class methods
#         input                                           line 894
# Selection Mode class methods
#         input                                           line 904
#         cycleObj                                    line 932
#         setInitSlxn                                 line 935
#         exit                                             line 943
#         moveObj                                    line 952
#================================
from objects import *
from math import *
from ti_draw import *
from ti_st import *
from gfx import *
#================================
class Environment:
  objArr=[]
  objModes=["rectangle","circle","line","arc","brush","polygon"]
  curOM=objModes[0]
  slxnMode=-1
  colour=[0,0,0]
  clrHist=[colour]
  brushThk=5
  lineThk=5
  brshPrfl=1
  grid=-1
  ghstShp=[]
  clkState=0
  visibleHUD=1
  key=""
  mPos=[]
  mPoints=[]
  mAngle=[]
  arcDir=1
  fill=-1
  winScale=1
  magLvl=1
  winX=get_screen_dim()[0]
  winY=get_screen_dim()[1]
  zoomXY=[0,winX,0,winY]
  XYShift=5/318*winX
  hudClr=[0,0,0]
  state=0

# Handles device input behaviour in drawing environment.
  def input(self):
    if self.key=="center":
      if self.curOM==self.objModes[0]: # Rectangle tool.
        if self.clkState==0:
          self.mPoints.append(self.mPos)
          self.clkState+=1
        elif self.clkState==1: 
          self.mPoints.append(self.mPos)
          if self.mPos[0]>self.mPoints[0][0] and self.mPos[1]>self.mPoints[0][1]:
            self.objArr.append(rectangle(self.mPoints[0][0],self.mPoints[0][1],self.mPos[0]-self.mPoints[0][0],self.mPos[1]-self.mPoints[0][1],self.colour,self.fill))
          elif self.mPos[0]<self.mPoints[0][0] and self.mPos[1]<self.mPoints[0][1]:
            self.objArr.append(rectangle(self.mPos[0],self.mPos[1],self.mPoints[0][0]-self.mPos[0],self.mPoints[0][1]-self.mPos[1],self.colour,self.fill))
          elif self.mPos[0]<self.mPoints[0][0] and self.mPos[1]>self.mPoints[0][1]:
            self.objArr.append(rectangle(self.mPos[0],self.mPoints[0][1],self.mPoints[0][0]-self.mPos[0],self.mPos[1]-self.mPoints[0][1],self.colour,self.fill))
          elif self.mPos[0]>self.mPoints[0][0] and self.mPos[1]<self.mPoints[0][1]:
            self.objArr.append(rectangle(self.mPoints[0][0],self.mPos[1],self.mPos[0]-self.mPoints[0][0],self.mPoints[0][1]-self.mPos[1],self.colour,self.fill))
          self.mPoints=[]
          self.clkState=0
          self.ghstShp=[]
      
      elif self.curOM==self.objModes[1]: # Circle tool.
        if self.clkState==0:
          self.mPoints.append(self.mPos)
          self.clkState+=1
        elif self.clkState==1:
          self.mPoints.append(self.mPos)
          self.objArr.append(circle(self.mPoints[0][0],self.mPoints[0][1],sqrt((self.mPoints[1][0]-self.mPoints[0][0])**2+(self.mPoints[1][1]-self.mPoints[0][1])**2),self.colour,self.fill))
          self.mPoints=[]
          self.clkState=0
          self.ghstShp=[]
      
      if self.curOM==self.objModes[2]: # Line tool.
        if self.clkState==0:
          self.mPoints.append(self.mPos)
          self.mAngle=[0]
          self.clkState+=1
        elif self.clkState==1:
          self.mPoints.append(self.mPos)
          if len(self.ghstShp)!=0:
            for i in range(len(self.ghstShp)):
              self.objArr.append(self.ghstShp[i])
          self.mPoints=[]
          self.clkState=0
          self.ghstShp=[]
      
      if self.curOM==self.objModes[3]: # Arc tool.
        if self.clkState==0:
          self.mPoints.append(self.mPos)
          self.mAngle=[0,360]
          self.clkState+=1
        elif self.clkState==1:
          self.mPoints.append(self.mPos)
          if self.mPos[0]>self.mPoints[0][0] and self.mPos[1]>self.mPoints[0][1]:
            self.objArr.append(arc(self.mPoints[0][0],self.mPoints[0][1],self.mPos[0]-self.mPoints[0][0],self.mPos[1]-self.mPoints[0][1],self.mAngle[0],self.mAngle[1],self.colour,self.fill))
          elif self.mPos[0]<self.mPoints[0][0] and self.mPos[1]<self.mPoints[0][1]:
            self.objArr.append(arc(self.mPos[0],self.mPos[1],self.mPoints[0][0]-self.mPos[0],self.mPoints[0][1]-self.mPos[1],self.mAngle[0],self.mAngle[1],self.colour,self.fill))
          elif self.mPos[0]<self.mPoints[0][0] and self.mPos[1]>self.mPoints[0][1]:
            self.objArr.append(arc(self.mPos[0],self.mPoints[0][1],self.mPoints[0][0]-self.mPos[0],self.mPos[1]-self.mPoints[0][1],self.mAngle[0],self.mAngle[1],self.colour,self.fill))
          elif self.mPos[0]>self.mPoints[0][0] and self.mPos[1]<self.mPoints[0][1]:
            self.objArr.append(arc(self.mPoints[0][0],self.mPos[1],self.mPos[0]-self.mPoints[0][0],self.mPoints[0][1]-self.mPos[1],self.mAngle[0],self.mAngle[1],self.colour,self.fill))
          self.clkState+=1
          self.mPoints=[]
          self.ghstShp=[]
        elif self.clkState==2:
          self.objArr[len(self.objArr)-1].angle1=self.mAngle[0]=self.mseAngle(self.objArr[len(self.objArr)-1].x+(1/2)*self.objArr[len(self.objArr)-1].width,self.objArr[len(self.objArr)-1].y+(1/2)*self.objArr[len(self.objArr)-1].height)
          self.clkState+=1
        elif self.clkState==3:
          self.objArr[len(self.objArr)-1].angle2=self.mAngle[1]=self.mseAngle(self.objArr[len(self.objArr)-1].x+(1/2)*self.objArr[len(self.objArr)-1].width,self.objArr[len(self.objArr)-1].y+(1/2)*self.objArr[len(self.objArr)-1].height,self.arcDir,self.mAngle[0])
          self.clkState=0
      
      if self.curOM==self.objModes[4]: # Brush tool.
        if self.clkState==0:
          self.fill=1
          self.clkState+=1
        elif self.clkState==1:
          self.clkState=0
      
      if self.curOM==self.objModes[5]: # Polygon tool.
        if self.clkState>=0:
          if self.clkState==0 and self.fill==1:
            self.fill=-1
          self.mPoints.append(self.mPos)
          self.clkState+=1
    
    elif self.key=="enter":
      if self.curOM==self.objModes[5] and self.clkState>0:
        xSet=[]
        ySet=[]
        for i in range(len(self.mPoints)):
          xSet.append(self.mPoints[i][0])
          ySet.append(self.mPoints[i][1])
        self.objArr.append(polygon(xSet,ySet,self.colour,self.fill))
        self.mPoints=[]
        self.clkState=0
        self.ghstShp=[]
    elif self.key=="t" and self.clkState==0:
      if self.objModes.index(self.curOM)<len(self.objModes)-1:
        self.curOM=self.objModes[self.objModes.index(self.curOM)+1]
      else:
        self.curOM=self.objModes[0]
    elif self.key=="(" or self.key==")":
      if self.curOM==self.objModes[4]:
        if self.key=="(" and self.brushThk>1:
          self.brushThk-=1
        elif self.key==")" and self.brushThk<30:
          self.brushThk+=1
      elif self.curOM==self.objModes[2]:
        if self.key=="(" and self.lineThk>1:
          self.lineThk-=1
        elif self.key==")" and self.lineThk<30:
          self.lineThk+=1
    elif self.key=="," and self.curOM==self.objModes[4]:
      self.brshPrfl*=-1
    elif self.key=="tab" and self.curOM==self.objModes[4]:
      if self.brshPrfl==-1:
        self.objArr.append(rectangle(self.mPos[0]-(0.5*self.brushThk),self.mPos[1]-(0.5*self.brushThk),self.brushThk,self.brushThk,self.colour,1))
      else:
        self.objArr.append(circle(self.mPos[0],self.mPos[1],0.5*self.brushThk,self.colour,1))
    
    elif self.key=="up":
      self.zoomXY[3]+=self.XYShift*self.winScale
      self.zoomXY[2]+=self.XYShift*self.winScale
    elif self.key=="right":
      self.zoomXY[1]+=self.XYShift*self.winScale
      self.zoomXY[0]+=self.XYShift*self.winScale
    elif self.key=="down":
      self.zoomXY[3]-=self.XYShift*self.winScale
      self.zoomXY[2]-=self.XYShift*self.winScale
    elif self.key=="left":
      self.zoomXY[1]-=self.XYShift*self.winScale
      self.zoomXY[0]-=self.XYShift*self.winScale
    
    elif self.key=="y":
      if self.hudClr==[0,0,0]:
        self.hudClr=[255,255,0]
      else:
        self.hudClr=[0,0,0]
    
    elif self.key=="g":
      self.grid*=-1
    elif self.key=="esc":
      if self.clkState>1 and self.curOM!=self.objModes[5]:
        self.objArr.pop()
      elif self.clkState==0:
        self.state=3
      self.mPoints=[]
      self.clkState=0
      self.ghstShp=[]
    elif self.key=="v":
      self.visibleHUD*=-1
    elif self.key=="f":
      self.fill*=-1
    elif self.key=="c":
      self.state=1
    elif self.key=="h":
      self.state=2
    elif self.key=="del":
      if self.curOM==self.objModes[5] and self.clkState>0:
        self.mPoints.pop()
        self.ghstShp[len(self.ghstShp)-1].x=self.ghstShp[len(self.ghstShp)-1].x[:len(self.ghstShp[len(self.ghstShp)-1].x)-2]+self.ghstShp[len(self.ghstShp)-1].x[len(self.ghstShp[len(self.ghstShp)-1].x)-1:]
        self.ghstShp[len(self.ghstShp)-1].y=self.ghstShp[len(self.ghstShp)-1].y[:len(self.ghstShp[len(self.ghstShp)-1].y)-2]+self.ghstShp[len(self.ghstShp)-1].y[len(self.ghstShp[len(self.ghstShp)-1].y)-1:]
        self.clkState-=1
      elif self.objArr!=[]:
        self.objArr.pop()
    elif self.key=="x":
      self.state=3
    elif self.key=="s":
      self.saveImg()
      drawSaveNote(self)
    elif self.key=="o":
      self.clrHist=self.loadClr()
      self.objArr=self.loadImg()
    elif self.key=="e":
      self.exportImg()
      drawExportNote(self)
    elif self.key=="+":
      if self.winScale>0.0625:
        self.winScale*=0.5
        self.magLvl*=2
      self.zoomXY=self.zoom()
    elif self.key=="-":
      if self.winScale<16:
        self.winScale*=2
        self.magLvl*=0.5
      self.zoomXY=self.zoom()
    elif self.key=="z":
      self.zoomXY=[0,self.winX,0,self.winY]
      self.winScale=1
      self.magLvl=1
    elif self.key==".":
      self.zoomXY=[0-(self.zoomXY[1]-self.zoomXY[0])/2,(self.zoomXY[1]-self.zoomXY[0])/2,0-(self.zoomXY[3]-self.zoomXY[2])/2,(self.zoomXY[3]-self.zoomXY[2])/2]
    elif self.key=="down":
      if self.curOM==self.objModes[3] and self.clkState==3:
        self.arcDir*=-1
    elif self.key=="return" and self.clkState==0:
      self.objArr.append(rectangle(0,0,self.winX,self.winY,self.colour,1))
    elif self.key=="?!" and self.clkState==0:
      self.slxnMode*=-1
    elif self.key!="":
      try:
        if 48<=ord(self.key)<=57:
          try:
            self.colour=self.clrHist[int(self.key)]
          except:
            self.colour=self.colour
      except:
        1
    
    if self.key=="":
      if self.state==0:
        if self.clkState==1:
          if self.curOM==self.objModes[0]:
            if self.mPos[0]>self.mPoints[0][0] and self.mPos[1]>self.mPoints[0][1]:
              self.ghstShp=[rectangle(self.mPoints[0][0],self.mPoints[0][1],self.mPos[0]-self.mPoints[0][0],self.mPos[1]-self.mPoints[0][1],self.colour,self.fill)]
            elif self.mPos[0]<self.mPoints[0][0] and self.mPos[1]<self.mPoints[0][1]:
              self.ghstShp=[rectangle(self.mPos[0],self.mPos[1],self.mPoints[0][0]-self.mPos[0],self.mPoints[0][1]-self.mPos[1],self.colour,self.fill)]
            elif self.mPos[0]<self.mPoints[0][0] and self.mPos[1]>self.mPoints[0][1]:
              self.ghstShp=[rectangle(self.mPos[0],self.mPoints[0][1],self.mPoints[0][0]-self.mPos[0],self.mPos[1]-self.mPoints[0][1],self.colour,self.fill)]
            elif self.mPos[0]>self.mPoints[0][0] and self.mPos[1]<self.mPoints[0][1]:
              self.ghstShp=[rectangle(self.mPoints[0][0],self.mPos[1],self.mPos[0]-self.mPoints[0][0],self.mPoints[0][1]-self.mPos[1],self.colour,self.fill)]
          
          elif self.curOM==self.objModes[1]:
            self.ghstShp=[circle(self.mPoints[0][0],self.mPoints[0][1],sqrt((self.mPoints[0][0]-self.mPos[0])**2+(self.mPoints[0][1]-self.mPos[1])**2),self.colour,self.fill)]
          
          elif self.curOM==self.objModes[2]:
            self.ghstShp=[line(self.mPoints[0][0],self.mPoints[0][1],self.mPos[0],self.mPos[1],self.colour)]
            if self.lineThk>1 and len(self.ghstShp)==1:
              self.mAngle[0]=radians(self.mseAngle(self.mPoints[0][0],self.mPoints[0][1]))
              for i in range(self.lineThk*2-2):
                if i%2==0:
                  self.ghstShp.append(line(self.mPoints[0][0]+(floor((i+2)/2)/16*cos(self.mAngle[0]+pi/2)),self.mPoints[0][1]+(floor((i+2)/2)/16*sin(self.mAngle[0]+pi/2)),self.mPos[0]+(floor((i+2)/2)/16*cos(self.mAngle[0]+pi/2)),self.mPos[1]+(floor((i+2)/2)/16*sin(self.mAngle[0]+pi/2)),self.colour))
                else:
                  self.ghstShp.append(line(self.mPoints[0][0]-(floor((i+2)/2)/16*cos(self.mAngle[0]+pi/2)),self.mPoints[0][1]-(floor((i+2)/2)/16*sin(self.mAngle[0]+pi/2)),self.mPos[0]-(floor((i+2)/2)/16*cos(self.mAngle[0]+pi/2)),self.mPos[1]-(floor((i+2)/2)/16*sin(self.mAngle[0]+pi/2)),self.colour))
          
          elif self.curOM==self.objModes[3]:
            if self.mPos[0]>self.mPoints[0][0] and self.mPos[1]>self.mPoints[0][1]:
              self.ghstShp=[arc(self.mPoints[0][0],self.mPoints[0][1],self.mPos[0]-self.mPoints[0][0],self.mPos[1]-self.mPoints[0][1],self.mAngle[0],self.mAngle[1],self.colour,self.fill)]
            elif self.mPos[0]<self.mPoints[0][0] and self.mPos[1]<self.mPoints[0][1]:
              self.ghstShp=[arc(self.mPos[0],self.mPos[1],self.mPoints[0][0]-self.mPos[0],self.mPoints[0][1]-self.mPos[1],self.mAngle[0],self.mAngle[1],self.colour,self.fill)]
            elif self.mPos[0]<self.mPoints[0][0] and self.mPos[1]>self.mPoints[0][1]:
              self.ghstShp=[arc(self.mPos[0],self.mPoints[0][1],self.mPoints[0][0]-self.mPos[0],self.mPos[1]-self.mPoints[0][1],self.mAngle[0],self.mAngle[1],self.colour,self.fill)]
            elif self.mPos[0]>self.mPoints[0][0] and self.mPos[1]<self.mPoints[0][1]:
              self.ghstShp=[arc(self.mPoints[0][0],self.mPos[1],self.mPos[0]-self.mPoints[0][0],self.mPoints[0][1]-self.mPos[1],self.mAngle[0],self.mAngle[1],self.colour,self.fill)]
          
          elif self.curOM==self.objModes[4]:
            if self.objArr==[] or self.objArr[len(self.objArr)-1].type=="circle" or self.objArr[len(self.objArr)-1].type=="rectangle" and self.objArr[len(self.objArr)-1].x!=(self.mPos[0]-(0.5*self.brushThk)) and self.objArr[len(self.objArr)-1].y!=(self.mPos[1]-(0.5*self.brushThk)):
              if self.brshPrfl==-1:
                self.objArr.append(rectangle(self.mPos[0]-(0.5*self.brushThk),self.mPos[1]-(0.5*self.brushThk),self.brushThk,self.brushThk,self.colour,1))
              else:
                self.objArr.append(circle(self.mPos[0],self.mPos[1],0.5*self.brushThk,self.colour,1))
        
        elif self.clkState==2 and self.curOM==self.objModes[3]:
          self.mAngle[0]=self.mseAngle(self.objArr[len(self.objArr)-1].x+(1/2)*self.objArr[len(self.objArr)-1].width,self.objArr[len(self.objArr)-1].y+(1/2)*self.objArr[len(self.objArr)-1].height)
          self.objArr[len(self.objArr)-1].angle1=360
          self.objArr[len(self.objArr)-1].angle2=self.mAngle[0]-360
          self.objArr[len(self.objArr)-1].fill=self.fill
          self.objArr[len(self.objArr)-1].colour=self.colour
        elif self.clkState==3 and self.curOM==self.objModes[3]:
          self.objArr[len(self.objArr)-1].angle2=self.mAngle[1]=self.mseAngle(self.objArr[len(self.objArr)-1].x+(1/2)*self.objArr[len(self.objArr)-1].width,self.objArr[len(self.objArr)-1].y+(1/2)*self.objArr[len(self.objArr)-1].height,self.arcDir,self.mAngle[0])
          self.objArr[len(self.objArr)-1].fill=self.fill
          self.objArr[len(self.objArr)-1].colour=self.colour
        if self.clkState>0 and self.curOM==self.objModes[5]:
          xSet=[]
          ySet=[]
          for i in range(len(self.mPoints)):
            xSet.append(self.mPoints[i][0])
            ySet.append(self.mPoints[i][1])
          xSet.append(self.mPos[0])
          ySet.append(self.mPos[1])
          self.ghstShp=[polygon(xSet,ySet,self.colour,self.fill)]

# Handles zoom functionality
  def zoom(self):
    x1=0
    x2=0
    y1=0
    y2=0
    winW=self.winX*self.winScale
    winH=self.winY*self.winScale
    winXY=[]
    
    x1=int(self.mPos[0]-(winW/2))
    x2=int(self.mPos[0]+(winW/2))
    y1=int(self.mPos[1]-(winH/2))
    y2=int(self.mPos[1]+(winH/2))
    
    winXY.append(x1)
    winXY.append(x2)
    winXY.append(y1)
    winXY.append(y2)
    
    return winXY

# Calculates cursor angle from ref. point
  def mseAngle(self,xRef,yRef,dir=1,argOffset=0):
    argOffset=radians(argOffset)
    xVal=self.mPos[0]-xRef
    yVal=self.mPos[1]-yRef
    mTheta=atan2(yVal,xVal)
    mTheta=degrees(atan2(sin(mTheta-argOffset),cos(mTheta-argOffset)))
    if dir==1:
      if mTheta<0:
        mTheta+=360
    else:
      if mTheta>0:
        mTheta-=360
    return mTheta

# Exports drawing for external use
  def exportImg(self):
    x=0
    y=0
    x2=0
    y2=0
    angle1=0
    angle2=0
    width=0
    height=0
    rad=0
    imgBdr=self.xyLimits()
    imgWidth=imgBdr[1]-imgBdr[0]
    imgHeight=imgBdr[3]-imgBdr[2]
    imgMidpnt=[imgWidth/2,imgHeight/2]
    xFix=-(imgBdr[0]+imgMidpnt[0]) # XY offset to initialise image
    yFix=-(imgBdr[2]+imgMidpnt[1]) # at 0,0.
    
    print("from ti_draw import *")
    print("# Image details:")
    print("# Total objects: "+str(len(self.objArr)))
    print("# Width: "+str(round(imgWidth,1))+", Height: "+str(round(imgHeight,1)))
    print("# Code to draw image")
    print("def drawImg(xOffset,yOffset):")
    print("  set_window(0,get_screen_dim()[0],0,get_screen_dim()[1])")
    for i in range(len(self.objArr)):
      if i==0:
        print("  set_color("+str(self.objArr[i].colour[0])+","+str(self.objArr[i].colour[1])+","+str(self.objArr[i].colour[2])+")")
      elif self.objArr[i].colour!=self.objArr[i-1].colour:
        print("  set_color("+str(self.objArr[i].colour[0])+","+str(self.objArr[i].colour[1])+","+str(self.objArr[i].colour[2])+")")
      if self.objArr[i].type=="circle":
        x=str(round(self.objArr[i].x+xFix,2))
        y=str(round(self.objArr[i].y+yFix,2))
        rad=str(round(self.objArr[i].radius,2))
        if self.objArr[i].fill==1:
          print("  fill_circle("+x+"+xOffset,"+y+"+yOffset,"+rad+")")
        else:
          print("  draw_circle("+x+"+xOffset,"+y+"+yOffset,"+rad+")")
      elif self.objArr[i].type=="rectangle":
        x=str(round(self.objArr[i].x+xFix,2))
        y=str(round(self.objArr[i].y+yFix,2))
        width=str(round(self.objArr[i].width,2))
        height=str(round(self.objArr[i].height,2))
        if self.objArr[i].fill==1:
          print("  fill_rect("+x+"+xOffset,"+y+"+yOffset,"+width+","+height+")")
        else:
          print("  draw_rect("+x+"+xOffset,"+y+"+yOffset,"+width+","+height+")")
      elif self.objArr[i].type=="line":
        x=str(round(self.objArr[i].x+xFix,2))
        y=str(round(self.objArr[i].y+yFix,2))
        x2=str(round(self.objArr[i].x2+xFix,2))
        y2=str(round(self.objArr[i].y2+yFix,2))
        print("  draw_line("+x+"+xOffset,"+y+"+yOffset,"+x2+"+xOffset,"+y2+"+yOffset)")
      elif self.objArr[i].type=="arc":
        x=str(round(self.objArr[i].x+xFix,2))
        y=str(round(self.objArr[i].y+yFix,2))
        angle1=str(round(self.objArr[i].angle1,2))
        angle2=str(round(self.objArr[i].angle2,2))
        width=str(round(self.objArr[i].width,2))
        height=str(round(self.objArr[i].height,2))
        if self.objArr[i].fill==1:
          print("  fill_arc("+x+"+xOffset,"+y+"+yOffset,"+width+","+height+","+angle1+","+angle2+")")
        else:
          print("  draw_arc("+x+"+xOffset,"+y+"+yOffset,"+width+","+height+","+angle1+","+angle2+")")
      elif self.objArr[i].type=="polygon":
        x=self.objArr[i].x
        y=self.objArr[i].y
        for j in range(len(x)):
          x[j]=x[j]+xFix
          y[j]=y[j]+yFix
        print("  x="+str(x))
        print("  y="+str(y))
        print("  for i in range(len(x)):")
        print("    x[i]=x[i]+xOffset")
        print("    y[i]=y[i]+yOffset")
        if self.objArr[i].fill==1:
          print("  fill_poly(x,y)")
        else:
          print("  draw_poly(x,y)")
    return

# Stores object array in ROM
  def saveImg(self):
    circles=[]
    rectangles=[]
    lines=[]
    arcs=[]
    polygons=[]
    zOrder=[]
    palette=[]
    
    for i in range(len(self.objArr)):
      if self.objArr[i].type=="circle":
        zOrder.append(1)
        circles.append(self.objArr[i].x)
        circles.append(self.objArr[i].y)
        circles.append(self.objArr[i].radius)
        circles.append(self.objArr[i].colour[0])
        circles.append(self.objArr[i].colour[1])
        circles.append(self.objArr[i].colour[2])
        circles.append(self.objArr[i].fill)
      elif self.objArr[i].type=="rectangle":
        zOrder.append(2)
        rectangles.append(self.objArr[i].x)
        rectangles.append(self.objArr[i].y)
        rectangles.append(self.objArr[i].width)
        rectangles.append(self.objArr[i].height)
        rectangles.append(self.objArr[i].colour[0])
        rectangles.append(self.objArr[i].colour[1])
        rectangles.append(self.objArr[i].colour[2])
        rectangles.append(self.objArr[i].fill)
      elif self.objArr[i].type=="line":
        zOrder.append(3)
        lines.append(self.objArr[i].x)
        lines.append(self.objArr[i].y)
        lines.append(self.objArr[i].x2)
        lines.append(self.objArr[i].y2)
        lines.append(self.objArr[i].colour[0])
        lines.append(self.objArr[i].colour[1])
        lines.append(self.objArr[i].colour[2])
      elif self.objArr[i].type=="arc":
        zOrder.append(4)
        arcs.append(self.objArr[i].x)
        arcs.append(self.objArr[i].y)
        arcs.append(self.objArr[i].width)
        arcs.append(self.objArr[i].height)
        arcs.append(self.objArr[i].angle1)
        arcs.append(self.objArr[i].angle2)
        arcs.append(self.objArr[i].colour[0])
        arcs.append(self.objArr[i].colour[1])
        arcs.append(self.objArr[i].colour[2])
        arcs.append(self.objArr[i].fill)
      elif self.objArr[i].type=="polygon":
        zOrder.append(5)
        polygons.append(len(self.objArr[i].x)) # Num of elements in coordinate array.
        for j in range(len(self.objArr[i].x)):
          polygons.append(self.objArr[i].x[j])
          polygons.append(self.objArr[i].y[j])
        polygons.append(self.objArr[i].colour[0])
        polygons.append(self.objArr[i].colour[1])
        polygons.append(self.objArr[i].colour[2])
        polygons.append(self.objArr[i].fill)
    
    for i in range(len(self.clrHist)):
      for j in range(len(self.clrHist[i])):
        palette.append(self.clrHist[i][j])
    
    writeSTLst("circles",circles)
    writeSTLst("rectangles",rectangles)
    writeSTLst("lines",lines)
    writeSTLst("arcs",arcs)
    writeSTLst("polygons",polygons)
    writeSTLst("zorder",zOrder)
    writeSTLst("palette",palette)
    
    return

# Loads colour palette
  def loadClr(self):
    palette=[]
    clrArr=[]
    
    try:
      palette=readSTLst("palette")
    except:
      palette=[]
    
    for i in range(0,len(palette),3):
      clrArr.append(palette[i:i+3])
    self.colour=clrArr[0]
    
    return clrArr

# Retrieves object array from ROM
  def loadImg(self):
    circles=[]
    rectangles=[]
    lines=[]
    arcs=[]
    polygons=[]
    zOrder=[]
    objArr=[]
    tmpArr=[]
    xSet=[]
    ySet=[]
    
    try:
      circles=readSTLst("circles")
    except:
      circles=[]
    try:
      rectangles=readSTLst("rectangles")
    except:
      rectangles=[]
    try:
      lines=readSTLst("lines")
    except:
      lines=[]
    try:
      arcs=readSTLst("arcs")
    except:
      arcs=[]
    try:
      polygons=readSTLst("polygons")
    except:
      polygons=[]
    try:
      zOrder=readSTLst("zorder")
    except:
      zOrder=[]
    
    for i in range(len(zOrder)):
      if zOrder[i]==1:
        for j in range(0,7):
          if j==3:
            tmpArr.append(circles[3:6])
          elif j<3 or j>5:
            tmpArr.append(circles[j])
        circles=circles[7:]
        objArr.append(circle(tmpArr[0],tmpArr[1],tmpArr[2],tmpArr[3],tmpArr[4]))
        tmpArr=[]
      
      elif zOrder[i]==2:
        for j in range(0,8):
          if j==4:
            tmpArr.append(rectangles[4:7])
          elif j<4 or j>6:
            tmpArr.append(rectangles[j])
        rectangles=rectangles[8:]
        objArr.append(rectangle(tmpArr[0],tmpArr[1],tmpArr[2],tmpArr[3],tmpArr[4],tmpArr[5]))
        tmpArr=[]
      
      elif zOrder[i]==3:
        for j in range(0,7):
          if j==4:
            tmpArr.append(lines[4:7])
          elif j<4:
            tmpArr.append(lines[j])
        lines=lines[7:]
        objArr.append(line(tmpArr[0],tmpArr[1],tmpArr[2],tmpArr[3],tmpArr[4]))
        tmpArr=[]
      
      elif zOrder[i]==4:
        for j in range(0,10):
          if j==6:
            tmpArr.append(arcs[6:9])
          elif j<6 or j>8:
            tmpArr.append(arcs[j])
        arcs=arcs[10:]
        objArr.append(arc(tmpArr[0],tmpArr[1],tmpArr[2],tmpArr[3],tmpArr[4],tmpArr[5],tmpArr[6],tmpArr[7]))
        tmpArr=[]
    
      elif zOrder[i]==5:
        xSet=[]
        ySet=[]
        for j in range(1,polygons[0]*2+5):
          if j<=polygons[0]*2:
            if j%2!=0:
              xSet.append(polygons[j])
            else:
              ySet.append(polygons[j])
          elif j==polygons[0]*2+1:
            tmpArr.append(polygons[polygons[0]*2+1:polygons[0]*2+4])
          elif j==polygons[0]*2+4:
            tmpArr.append(polygons[j])
        tmpArr.insert(0,xSet)
        tmpArr.insert(1,ySet)
        polygons=polygons[polygons[0]*2+5:]
        objArr.append(polygon(tmpArr[0],tmpArr[1],tmpArr[2],tmpArr[3]))
        tmpArr=[]
    
    return objArr

# Finds XY limits of image. 
  def xyLimits(self):
    xyLims=[1*10**30,0,1*10**30,0] # Final xy limits for all objects. Python infinity type?
    xMin=0 # Temporary min x value.
    xMax=0 # Temporary max x value.
    yMin=0 # Temporary min y value.
    yMax=0 # Temporary max y value.
    a=0 # Ellipse equation variable.
    b=0 # Ellipse equation variable.
    x=0 # Ellipse equation variable.
    y=0 # Ellipse equation variable.
    x2=0 # Ellipse equation variable.
    y2=0 # Ellipse equation variable.
    arcStartXY=[] # Arc start point coordinates.
    arcEndXY=[] # Arc end point coordinates.
    argRng=[] # Arc argument range.
    
    if len(self.objArr)>0:
      for i in range(len(self.objArr)):
        if self.objArr[i].type=="arc":
          # Calculate XY coordinates for arc start/end points.
          a=self.objArr[i].width/2
          b=self.objArr[i].height/2
          x=(a*b)/(sqrt(b**2+(a*tan(radians(self.objArr[i].angle1)))**2))
          y=x*tan(radians(self.objArr[i].angle1))
          x2=(a*b)/(sqrt(b**2+(a*tan(radians(self.objArr[i].angle2+self.objArr[i].angle1)))**2))
          y2=x2*tan(radians(self.objArr[i].angle1+self.objArr[i].angle2))
          
          # Correction for tan sign inversion in Y and negation of X.
          if 90<self.objArr[i].angle1<270:
            x*=-1
            y*=-1
          if 90<self.objArr[i].angle1+self.objArr[i].angle2<270:
            x2*=-1
            y2*=-1
          
          arcStartXY=[x+(self.objArr[i].x+self.objArr[i].width/2),y+(self.objArr[i].y+self.objArr[i].height/2)]
          arcEndXY=[x2+(self.objArr[i].x+self.objArr[i].width/2),y2+(self.objArr[i].y+self.objArr[i].height/2)]
          
          # Calculate XY limits for arc.
          if self.objArr[i].angle2>0:
            argRng=[self.objArr[i].angle1,(self.objArr[i].angle1+self.objArr[i].angle2)%360]
          else:
            argRng=[(self.objArr[i].angle1+self.objArr[i].angle2)%360,self.objArr[i].angle1]
          if argRng[0]>argRng[1]:
            xMax=self.objArr[i].x+self.objArr[i].width
          elif arcStartXY[0]>arcEndXY[0]:
            xMax=arcStartXY[0]
          else:
            xMax=arcEndXY[0]
          
          if argRng[0]<90<argRng[1] or argRng[0]>argRng[1] and not argRng[1]<90<argRng[0]:
            yMax=self.objArr[i].y+self.objArr[i].height
          elif arcStartXY[1]>arcEndXY[1]:
            yMax=arcStartXY[1]
          else:
            yMax=arcEndXY[1]
          
          if argRng[0]<180<argRng[1] or argRng[0]>argRng[1] and not argRng[1]<180<argRng[0]:
            xMin=self.objArr[i].x
          elif arcStartXY[0]<arcEndXY[0]:
            xMin=arcStartXY[0]
          else:
            xMin=arcEndXY[0]
          
          if argRng[0]<270<argRng[1] or argRng[0]>argRng[1] and not argRng[1]<270<argRng[0]:
            yMin=self.objArr[i].y
          elif arcStartXY[1]<arcEndXY[1]:
            yMin=arcStartXY[1]
          else:
            yMin=arcEndXY[1]
          
          # Compare/update final limits.
          if xMin<xyLims[0]:
            xyLims[0]=xMin
          if xMax>xyLims[1]:
            xyLims[1]=xMax
          if yMin<xyLims[2]:
            xyLims[2]=yMin
          if yMax>xyLims[3]:
            xyLims[3]=yMax
        
        elif self.objArr[i].type=="rectangle":
          xMin=self.objArr[i].x
          xMax=self.objArr[i].x+self.objArr[i].width
          yMin=self.objArr[i].y
          yMax=self.objArr[i].y+self.objArr[i].height
          
          # Compare/update final limits.
          if xMin<xyLims[0]:
            xyLims[0]=xMin
          if xMax>xyLims[1]:
            xyLims[1]=xMax
          if yMin<xyLims[2]:
            xyLims[2]=yMin
          if yMax>xyLims[3]:
            xyLims[3]=yMax
        
        elif self.objArr[i].type=="circle":
          xMin=self.objArr[i].x-self.objArr[i].radius
          xMax=self.objArr[i].x+self.objArr[i].radius
          yMin=self.objArr[i].y-self.objArr[i].radius
          yMax=self.objArr[i].y+self.objArr[i].radius
          
          # Compare/update final limits.
          if xMin<xyLims[0]:
            xyLims[0]=xMin
          if xMax>xyLims[1]:
            xyLims[1]=xMax
          if yMin<xyLims[2]:
            xyLims[2]=yMin
          if yMax>xyLims[3]:
            xyLims[3]=yMax
        
        elif self.objArr[i].type=="line":
          if self.objArr[i].x<self.objArr[i].x2:
            xMin=self.objArr[i].x
            xMax=self.objArr[i].x2
          else:
            xMin=self.objArr[i].x2
            xMax=self.objArr[i].x
          if self.objArr[i].y<self.objArr[i].y2:
            yMin=self.objArr[i].y
            yMax=self.objArr[i].y2
          else:
            yMin=self.objArr[i].y2
            yMax=self.objArr[i].y
          
          # Compare/update final limits.
          if xMin<xyLims[0]:
            xyLims[0]=xMin
          if xMax>xyLims[1]:
            xyLims[1]=xMax
          if yMin<xyLims[2]:
            xyLims[2]=yMin
          if yMax>xyLims[3]:
            xyLims[3]=yMax
        
        elif self.objArr[i].type=="polygon":
          xMin=min(self.objArr[i].x)
          xMax=max(self.objArr[i].x)
          yMin=min(self.objArr[i].y)
          yMax=max(self.objArr[i].y)
          
          # Compare/update final limits.
          if xMin<xyLims[0]:
            xyLims[0]=xMin
          if xMax>xyLims[1]:
            xyLims[1]=xMax
          if yMin<xyLims[2]:
            xyLims[2]=yMin
          if yMax>xyLims[3]:
            xyLims[3]=yMax
    else:
      xyLims=[0,0,0,0]
    return xyLims

# Menu for changing colours.
class ColourMenu:
  # Colour wheel properties
  winX=get_screen_dim()[0]
  winY=get_screen_dim()[1]
  wheelX=1/15*winX
  wheelY=1/8*winY
  wheelW=3/4*winY
  wheelH=3/4*winY
  wheelXC=wheelX+wheelW/2 # Wheel centre X
  wheelYC=1/2*winY # Wheel centre Y
  wheelRad=1/2*wheelW
  mseWheelXPos=0
  mseWheelYPos=0
  mseWhlTheta=0
  mPos=[-1,-1]
  
  # Right ribbon properties
  rRibX=wheelX+wheelW
  rRibY=winY
  rRibW=winX-rRibX
  
  # Gradient wheel properties
  gWhlX=15/14*rRibX
  gWhlY=14/15*rRibY 
  gWhlW=3/5*rRibX
  gWhlH=3/5*rRibX
  gWhlXC=gWhlX+gWhlW/2 # Wheel centre X
  gWhlYC=gWhlY-(1/2*gWhlW) # Wheel centre Y
  gWhlRad=1/2*gWhlW
  mseGWhlXPos=0
  mseGWhlYPos=0
  mseGWhlTheta=0
  
  mseInGWhlBnds=False
  mseInCWhlBnds=False
  wheelFlag=False
  gradWhlFlag=False
  
  previewClr=[0,0,0]
  slxnClr=[0,0,0]

# Handles device input behaviour in colour menu.
  def input(self,env):
    self.mPos[0]=get_mouse()[0]
    self.mPos[1]=abs(env.winY-get_mouse()[1]) # Band aid solution for mouse inversion issue.
    self.mseCWhlCheck(self.mPos)
    self.mseGWhlCheck(self.mPos)
    if env.key=="center":
      if self.mseInCWhlBnds:
        self.slxnClr=self.previewClr
      elif self.mseInGWhlBnds:
        self.slxnClr=self.previewClr
    elif env.key=="esc":
      self.exit(env)
    return

# Tracks mouse with relation to colour wheel.
  def mseCWhlCheck(self,mPos):
    if sqrt((mPos[0]-self.wheelXC)**2+(self.wheelYC-mPos[1])**2)<=self.wheelRad:
      self.mseInCWhlBnds=True
      self.mseWheelXPos=mPos[0]-self.wheelXC
      self.mseWheelYPos=-(self.wheelYC-mPos[1])
      self.mseWhlTheta=degrees(atan2(self.mseWheelYPos,self.mseWheelXPos))
    else:
      self.mseInCWhlBnds=False
    return

# Tracks mouse with relation to gradient wheel.
  def mseGWhlCheck(self,mPos):
    if sqrt((mPos[0]-self.gWhlXC)**2+(self.gWhlYC-mPos[1])**2)<=self.gWhlRad and self.slxnClr!=[]:
      self.mseInGWhlBnds=True
      self.mseGWhlXPos=mPos[0]-self.gWhlXC
      self.mseGWhlYPos=-(self.gWhlYC-mPos[1])
      self.mseGWhlTheta=degrees(atan2(self.mseGWhlYPos,self.mseGWhlXPos))
      if self.mseGWhlTheta<0:
        self.mseGWhlTheta=360+self.mseGWhlTheta
    else:
      self.mseInGWhlBnds=False
    return

# Exit colour menu
  def exit(self,env):
    if self.slxnClr!=env.clrHist[0]:
      env.colour=self.slxnClr
      env.clrHist.insert(0,env.colour)
    if len(env.clrHist)>10:
      env.clrHist.pop(len(env.clrHist)-1)
    env.state=0
    self.wheelFlag=False

class Help:
  def input(self,env):
    if env.key=="esc" or env.key=="h":
      env.state=0
    return

class SlxnMode:
  currObj=[]
  currClr=[]
  slxnClr=[255,0,255]
  mStep=0.5
  
  def input(self,env):
    if self.currObj==[]:
      self.setInitSlxn(env)
    if env.key=="?!":
      self.exit(env)
    elif env.key=="left":
      self.moveObj(0,-self.mStep)
    elif env.key=="right":
      self.moveObj(0,self.mStep)
    elif env.key=="up":
      self.moveObj(1,self.mStep)
    elif env.key=="down":
      self.moveObj(1,-self.mStep)
    elif env.key=="+":
      self.currObj.colour=self.currClr
      self.currObj=self.cycleObj(1,env.objArr)
      self.currClr=self.currObj.colour
      self.currObj.colour=self.slxnClr
    elif env.key=="-":
      self.currObj.colour=self.currClr
      self.currObj=self.cycleObj(-1,env.objArr)
      self.currClr=self.currObj.colour
      self.currObj.colour=self.slxnClr
    elif env.key=="x":
      self.mirrorObj(0)
    elif env.key=="y":
      self.mirrorObj(1)
    elif env.key=="*":
      self.cycleZ(1,env.objArr)
    elif env.key=="/":
      self.cycleZ(-1,env.objArr)
    elif env.key=="del" or env.key=="esc":
      env.objArr.remove(self.currObj)
      self.setInitSlxn(env)
    return
  
  def cycleObj(self,dir,objarr):
    return objarr[(objarr.index(self.currObj)+dir)%len(objarr)]
  
  def setInitSlxn(self,env):
    try:
      self.currObj=env.objArr[len(env.objArr)-1]
      self.currClr=self.currObj.colour
      self.currObj.colour=self.slxnClr
    except:
      self.exit(env)
  
  def exit(self,env):
    try:
      self.currObj.colour=self.currClr
    except:
      1
    env.slxnMode=-1
    self.currObj=[]
    self.currClr=[]
  
  def moveObj(self,dir,step=1):
    if dir==0:
      if self.currObj.type=="polygon":
        for idx in range(len(self.currObj.x)):
          self.currObj.x[idx]+=step
      elif self.currObj.type=="line":
        self.currObj.x+=step
        self.currObj.x2+=step
      else:
        self.currObj.x+=step
    elif dir==1:
      if self.currObj.type=="polygon":
        for idx in range(len(self.currObj.y)):
          self.currObj.y[idx]+=step
      elif self.currObj.type=="line":
        self.currObj.y+=step
        self.currObj.y2+=step
      else:
        self.currObj.y+=step
  
  def mirrorObj(self,dir):
    if dir==0:
      if self.currObj.type=="polygon":
        for idx in range(len(self.currObj.x)):
          self.currObj.x[idx]*=-1
      elif self.currObj.type=="line":
        self.currObj.x*=-1
        self.currObj.x2*=-1
#      elif self.currObj.type=="arc":
#        
      else:
        self.currObj.x*=-1
    elif dir==1:
      if self.currObj.type=="polygon":
        for idx in range(len(self.currObj.y)):
          self.currObj.y[idx]*=-1
      elif self.currObj.type=="line":
        self.currObj.y*=-1
        self.currObj.y2*=-1
      else:
        self.currObj.y*=-1
  
  def cycleZ(self,dir,objarr):
    objIdx=objarr.index(self.currObj)
    holdObj=objarr[(objIdx+dir)%len(objarr)]
    objarr[(objIdx+dir)%len(objarr)]=self.currObj
    objarr[objIdx]=holdObj
    

# 
