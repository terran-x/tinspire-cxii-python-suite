####################
from ti_draw import *
from bc_images import *
####################
def show():
  wX=get_screen_dim()[0]
  wY=get_screen_dim()[1]
  scale=1
  set_window(-wX/scale,wX/scale,-wY/scale,wY/scale)
  clear()
  use_buffer()
#  wrs(0,0)
#  wlp_rs(13,0)
  set_color(0,255,0)
#  draw_line(0,-wY/scale,0,wY/scale)
#  draw_rect(13-15,0-15,30,30)
  paint_buffer()

show()
