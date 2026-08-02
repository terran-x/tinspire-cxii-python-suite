# Inbuilt function "draw_text()" autoscales for window size, no
# no way to get win size or scaled text size so can only
# scale popups for native win size (318x212).
#===============
from ti_draw import *
from ti_system import *
#===============
class window:
  def __init__(self,x,y,w,h,bgc=[255,255,255],ftc=[0,0,0]):
    self.x=x
    self.y=y
    self.width=w
    self.height=h
    self.bg_colour=bgc
    self.font_colour=ftc

class msgbox(window):
  def __init__(self,x,y,w,h,cap="",bgc=[240,240,240],ftc=[0,0,0]):
    window.__init__(self,x,y,w,h,bgc,ftc)
    self.caption=cap
    self.caparray=[]

  # Runs message box
  def run(self):
    while 1:
      key=get_key()
      self.show()
      if key=="esc":
        return 0
      elif key=="enter":
         return 1
    return

# Display messagebox window (318x212 win size).
  def show(self):
    self.caparray=self.trimCap() # Caption array
    sDim=string_size(self.caparray[0]) # String dimensions
    capLnHt=self.capHtScale()*sDim[1] # Caption line height
    capHt=len(self.caparray)*capLnHt # Caption height
    # Draw popup window and frame
    use_buffer()
    clear_rect(self.x-.5*self.width,self.y-.5*self.height,self.width,self.height)
    set_color(self.bg_colour[0],self.bg_colour[1],self.bg_colour[2])
    fill_rect(self.x-.5*self.width,self.y-.5*self.height,self.width,self.height)
    set_color(self.font_colour[0],self.font_colour[1],self.font_colour[2])
    draw_rect(self.x-.5*self.width,self.y-.5*self.height,self.width,self.height)
    draw_rect(self.x-.47*self.width,self.y-.47*self.height,.94*self.width,.94*self.height)
    # Draw caption
    for i in range(len(self.caparray)):
      sDim=string_size(self.caparray[i])
      draw_text(self.x-.5*sDim[0],self.y+.5*capHt-capLnHt*(1+i),self.caparray[i])
    
    paint_buffer()
    return

  # Trim caption to fit window horizontally
  def trimCap(self):
    rs=self.caption # Remaining string
    ts=self.caption # Trimmed string
    tsArr=[] # Trimmed string array
    w=.85*self.width # String boundary width
    
    while string_size(rs)[0]>w:
      ts=rs
      while string_size(ts)[0]>w:
        if ts.rfind(" ")!=-1 and ts.rfind(" ")!=0:
          ts=ts[:ts.rfind(" ")]
        else:
          ts=ts[:len(ts)-1]
      tsArr.append(ts.strip())
      rs=rs[len(ts):]
    tsArr.append(rs.strip())
    return tsArr

# Scale caption vertically.
  def capHtScale(self):
    wBdrHt=.9*self.height
    capHt=len(self.caparray)*string_size(self.caparray[0])[1]*0.8
    if capHt>wBdrHt:
      return (wBdrHt/capHt)*.8
    else:
      return .8

class inputbox(window):
  def __init__(self,x,y,w,h,cap="",inp="",inpsz=100,bgc=[240,240,240],ftc=[0,0,0]):
    window.__init__(self,x,y,w,h,bgc,ftc)
    self.caption=cap
    self.caparray=[]
    self.input=inp
    self.inputsize=inpsz

# Display inputbox window (318x212 win size).
  def show(self):
    self.caparray=self.trimCap() # Caption array
    sDim=string_size(self.caparray[0]) # String dimensions
    capLnHt=self.capHtScale()*sDim[1] # Caption line height
    capHt=len(self.caparray)*capLnHt # Caption height
    # Draw popup window and frame
    use_buffer()
    clear_rect(self.x-.5*self.width,self.y-.5*self.height,self.width,self.height)
    set_color(self.bg_colour[0],self.bg_colour[1],self.bg_colour[2])
    fill_rect(self.x-.5*self.width,self.y-.5*self.height,self.width,self.height)
    set_color(self.font_colour[0],self.font_colour[1],self.font_colour[2])
    draw_rect(self.x-.5*self.width,self.y-.5*self.height,self.width,self.height)
    draw_rect(self.x-.47*self.width,self.y-.47*self.height,.94*self.width,.94*self.height)
    # Draw caption
    for i in range(len(self.caparray)):
      sDim=string_size(self.caparray[i])
      draw_text(self.x-.5*sDim[0],(.15*self.height+self.y)+.5*capHt-capLnHt*(1+i),self.caparray[i])
    # Draw input box
    set_color(255,255,255)
    fill_rect(self.x-.4*self.width,self.y-.4*self.height,.8*self.width,sDim[1])
    set_color(0,0,0)
    draw_rect(self.x-.4*self.width,self.y-.4*self.height,.8*self.width,sDim[1])
    draw_text(self.x-.4*self.width+1,self.y-.4*self.height+1,self.trimInpStr(.8*self.width))
    
    paint_buffer()
    return

  # Runs input box
  def run(self):
    while 1:
      key=get_key()
      self.show()
      if key=="esc":
        break
        return 0
      elif key!="" and len(key)==1 and len(self.input)<self.inputsize:
        if 32<=ord(key)<=57 or 97<=ord(key)<=122 or 61<=ord(key)<=90:
          self.input+=key
      elif key=="del" and len(self.input)>0:
        self.input=self.input[:len(self.input)-1]
      elif key=="enter":
         return self.input
    return

  # Trims input string to fit input box
  def trimInpStr(self,boxW):
    trimStr=self.input
    while string_size(trimStr)[0]>=boxW:
      trimStr=trimStr[1:]
    return trimStr


  # Trim caption to fit window horizontally
  def trimCap(self):
    rs=self.caption # Remaining string
    ts=self.caption # Trimmed string
    tsArr=[] # Trimmed string array
    w=.85*self.width # String boundary width
    
    while string_size(rs)[0]>w:
      ts=rs
      while string_size(ts)[0]>w:
        if ts.rfind(" ")!=-1 and ts.rfind(" ")!=0:
          ts=ts[:ts.rfind(" ")]
        else:
          ts=ts[:len(ts)-1]
      tsArr.append(ts.strip())
      rs=rs[len(ts):]
    tsArr.append(rs.strip())
    return tsArr

# Scale caption vertically.
  def capHtScale(self):
    wBdrHt=.6*self.height
    capHt=len(self.caparray)*string_size(self.caparray[0])[1]*0.8
    if capHt>wBdrHt:
      return (wBdrHt/capHt)*.8
    else:
      return .8

def help():
  print("msgbox(x,y,width,height,caption,bg_colour,text_colour)")
  print("msgbox.run()")
  print("inputbox(x,y,width,height,caption,input_text,max_input_size,bg_colour,text_colour)")
  print("inputbox.run()")
  return

# 
