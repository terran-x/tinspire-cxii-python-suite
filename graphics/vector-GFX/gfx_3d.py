# Vector Graphics
#================================
from vector_objects import *
from ti_system import *
from ti_draw import *
from sys import *
from math import *
#================================
def animate(polygons):
  loopTime=0
  runTime=0
  delta=0
  theta=pi/18
  key=""
  winX=get_screen_dim()[0]
  winY=get_screen_dim()[1]
  set_window(-winX*0.5,winX*0.5,-winY*0.5,winY*0.5)
  while 1:
    loopTime=get_time_ms()
    runTime+=delta
    key=get_key()
    clear()
    use_buffer()
    for poly in polygons:
      if key=="up":
        poly.rotate(0,-theta)
      elif key=="down":
        poly.rotate(0,theta)
      elif key=="left":
        poly.rotate(1,-theta)
      elif key=="right":
        poly.rotate(1,theta)
      elif key=="-":
        poly.rotate(2,-theta)
      elif key=="+":
        poly.rotate(2,theta)
      elif key=="8":
        poly.rotate(0,theta,False)
      elif key=="2":
        poly.rotate(0,-theta,False)
      elif key=="4":
        poly.rotate(1,theta,False)
      elif key=="6":
        poly.rotate(1,-theta,False)
      elif key=="7":
        poly.rotate(2,-theta,False)
      elif key=="9":
        poly.rotate(2,theta,False)
      elif key==")" and poly.type=="cube":
        poly.size+=5
      elif key=="(" and poly.type=="cube":
        poly.size-=5
      elif key=="b":
        poly.translate(5,1)
      elif key=="p":
        poly.translate(-5,1)
      elif key=="h":
        poly.translate(-5,0)
      elif key=="j":
        poly.translate(5,0)
      poly.draw()
    if key=="=":
      if theta==pi/180:
        theta=pi/18
      else:
        theta=pi/180
    debug(winX,winY,polygons[1])
    paint_buffer()
    delta=(get_time_ms()-loopTime)/1000

def debug(wx,wy,shp):
  i=str(round(shp.lXYZ[0][0],2))+", "+str(round(shp.lXYZ[1][0],2))+", "+str(round(shp.lXYZ[2][0],2))
  j=str(round(shp.lXYZ[0][1],2))+", "+str(round(shp.lXYZ[1][1],2))+", "+str(round(shp.lXYZ[2][1],2))
  k=str(round(shp.lXYZ[0][2],2))+", "+str(round(shp.lXYZ[1][2],2))+", "+str(round(shp.lXYZ[2][2],2))
  gRX=str(round(degrees(shp.rotation[0]),2))
  gRY=str(round(degrees(shp.rotation[1]),2))
  gRZ=str(round(degrees(shp.rotation[2]),2))
  szi=string_size("i: "+i)
  szj=string_size("j: "+j)
  szk=string_size("k: "+k)
  set_color(255,0,0)
  draw_text(-wx*0.5,0.5*wy-szk[1],"i: "+i)
  draw_text(-wx*0.5,-0.5*wy+2*szk[1],"GlbXRot: "+gRX)
  set_color(0,255,0)
  draw_text(-wx*0.5,0.5*wy-2*szj[1],"j: "+j)
  draw_text(-wx*0.5,-0.5*wy+szk[1],"GlbYRot: "+gRY)
  set_color(0,0,255)
  draw_text(-wx*0.5,0.5*wy-3*szk[1],"k: "+k)
  draw_text(-wx*0.5,-0.5*wy,"GlbZRot: "+gRZ)

def main():
  polygons=[Cube(50),Axes(80,[0,0,0],[0,0,0],[0,0,255])]
  animate(polygons)

main()
