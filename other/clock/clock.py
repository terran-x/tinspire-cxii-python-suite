#To set the time use "set_time()" function
#in shell, after importing "ti_time".
#==================
from ti_time import *
from ti_draw import *
from sys import *
from ti_system import *
#==================
def main():
  try:
    get_time()
  except:
    clear_history()
    set_time()
  
  set_window(0,get_screen_dim()[0],0,get_screen_dim()[1])
  while 1:
    keypress()
    drawClock(get_time(),get_date())
  return

def keypress():
  key=get_key()
  if key=="esc":
    exit()
  return 0

def drawClock(time,date):
  scrDim=get_screen_dim()
  
  clear()
  use_buffer()
  set_color(0,0,0)
  fill_rect(0,0,scrDim[0],scrDim[1])
  set_color(0,255,0)
  draw_text((scrDim[0]-string_size(time)[0])/2,scrDim[1]/2+string_size(time)[1],get_time())
  draw_text((scrDim[0]-string_size(date)[0])/2,scrDim[1]/2,get_date())
  paint_buffer()

main()

# 
