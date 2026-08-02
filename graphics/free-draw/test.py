#================================
#                                 TO-DO
#================================
#**Add zoom feature✓
#**Fix drawing tools: rectangle inversion✓ arc
#**Add drawing tools: brush✓, line thickness✓, 
#**                                   point2point polygon✓, fill, eraser
#**Store colours✓
#**Menu options: New canvas, Additional save slots
#**Selection tool/group selection
#**Transformations: linear, mirror, scale, rotate
#**XY mobility for images (in export functions)✓
#**Fix: Z-order when saving/loading✓
#**        Display HUD and zoom level when zoomed✓
#================================
#                              TESTING
#================================
#from math import *
#from ti_system import *
#from ti_draw import *
from ti_st import *

# Intersperses one list into another.
def intersperse(arr1,arr2):
  newArr=[]
  if len(arr1)==len(arr2):
    for i in range(len(arr1)):
      newArr.append(arr1[i])
      newArr.append(arr2[i])
  return newArr

# Prints saved drawing data.
def printDrawData():
  print("Circles")
  print(str(readSTLst("circles")).replace(" ",""))
  print("Rectangles")
  print(str(readSTLst("rectangles")).replace(" ",""))
  print("Lines")
  print(str(readSTLst("lines")).replace(" ",""))
  print("Arcs")
  print(str(readSTLst("arcs")).replace(" ",""))
  print("Polygons")
  print(str(readSTLst("polygons")).replace(" ",""))
  print("z-Order")
  print(str(readSTLst("zOrder")).replace(" ",""))
  print("Palette")
  print(str(readSTLst("palette")).replace(" ",""))

#circles=[]
#rectangles=[]
#lines=[]
#arcs=[]
#polygons=[]
#zOrder=[]
#palette=[]

#from ti_st import *
#writeSTLst("circles",circles)
#writeSTLst("rectangles",rectangles)
#writeSTLst("lines",lines)
#writeSTLst("arcs",arcs)
#writeSTLst("polygons",polygons)
#writeSTLst("zorder",zOrder)
#writeSTLst("palette",palette)
#

# 
