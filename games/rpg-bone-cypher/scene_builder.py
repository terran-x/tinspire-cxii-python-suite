# §εηε•βμιζδεř
####################
from random import *
from ti_draw import *
from ti_lists import *
from matrices import *
####################
# Tiles
NOPATH=-2
EMPTY=-1
ENTRY=1
EXIT=2
PATH=3

# CORE BUILD FUNCTIONS
####################
# Creates a matrix of 'EMPTY' elements.
def newGridMtx(rows,cols):
  matrix=[]
  for i in range(rows):
    matrix.append([])
    for j in range(cols):
      matrix[i].append(EMPTY)
  return matrix

# Randomly creates entry/exit points on matrix perimeter.
def setEntryExit(mtx):
  rows=len(mtx)-1
  cols=len(mtx[0])-1
  cEndIdx=[0,cols]
  rEndIdx=[0,rows]
  colIdx=0
  rowIdx=0
  if random()<.5:
# Column entry with exit on opposing end column.
    colIdx=choice(cEndIdx)
    entry=[randint(0,rows),colIdx]
    exit=[randint(0,rows),cEndIdx[1-cEndIdx.index(colIdx)]]
  else:
# Row entry with exit on opposing end row.
    rowIdx=choice(rEndIdx)
    entry=[rowIdx,randint(0,cols)]
    exit=[rEndIdx[1-rEndIdx.index(rowIdx)],randint(0,cols)]
  return [entry,exit]

# Procedurally generates a path between coordinates.
def pathfind(coords,mtx,hist=[]):
  rowIdx=coords[0]
  colIdx=coords[1]
  dirs=[]
  if hist==[]:
    hist=coords
# Check adjoining tiles for exit or else clear movement.
  if rowIdx<len(mtx)-1:
    if mtx[rowIdx+1][colIdx]==EXIT:
      return
    elif mtx[rowIdx+1][colIdx]==EMPTY:
      dirs.append("down")
  if rowIdx>0:
    if mtx[rowIdx-1][colIdx]==EXIT:
      return
    elif mtx[rowIdx-1][colIdx]==EMPTY:
      dirs.append("up")
  if colIdx<len(mtx[0])-1:
    if mtx[rowIdx][colIdx+1]==EXIT:
      return
    elif mtx[rowIdx][colIdx+1]==EMPTY:
      dirs.append("right")
  if colIdx>0:
    if mtx[rowIdx][colIdx-1]==EXIT:
      return
    elif mtx[rowIdx][colIdx-1]==EMPTY:
      dirs.append("left")
# Randomly selects next available move.
  if dirs!=[]:
    nextMove=choice(dirs)
    hist.append([rowIdx,colIdx])
    if nextMove=="down":
      mtx[rowIdx+1][colIdx]=PATH
      pathfind([rowIdx+1,colIdx],mtx,hist)
    elif nextMove=="up":
      mtx[rowIdx-1][colIdx]=PATH
      pathfind([rowIdx-1,colIdx],mtx,hist)
    elif nextMove=="right":
      mtx[rowIdx][colIdx+1]=PATH
      pathfind([rowIdx,colIdx+1],mtx,hist)
    elif nextMove=="left":
      mtx[rowIdx][colIdx-1]=PATH
      pathfind([rowIdx,colIdx-1],mtx,hist)
# Backtrack if no move possible until viable tile found.
  else:
    mtx[rowIdx][colIdx]=NOPATH
    hist.pop()
    return pathfind(hist[len(hist)-1],mtx,hist)
  return mtx

# Builds a scene grid matrix.
def buildGridMtx(rows,cols):
# Create a new grid matrix.
  mtx=newGridMtx(rows,cols)
# Set entry/exit points.
  doors=setEntryExit(mtx)
  mtx[doors[0][0]][doors[0][1]]=ENTRY
  mtx[doors[1][0]][doors[1][1]]=EXIT
# Procedural generation of an essential path.
  mtx=pathfind([doors[0][0],doors[0][1]],mtx)
# Rewrites dead paths into empty space.
  for row in mtx:
    for i in range(len(row)):
      if row[i]==NOPATH:
        row[i]=EMPTY
  return mtx

# SCENE DRAWING FUNCTIONS
####################
# Converts scene grid matrix to a grid array containing
# properties of the individual grid tiles.
def matrixToGrid(mtx,tilesize=60,x=0,y=0,tileClr=\
             [EMPTY,[140,140,140],\
             PATH,[150,80,30],\
             ENTRY,[0,220,0],EXIT,[220,0,0]]):
  tileGrid=[]
  tileRow=[]
  rows=len(mtx)
  cols=len(mtx[0])
  w=tilesize*cols # Grid width
  h=tilesize*rows # Grid height
  for i in range(rows):
    for j in range(cols):
# Pixel addresses located at lwr left corner of each grid tile.
      tileRow.append({"type":mtx[i][j],"pxl_address":\
      [x-w/2+j*tilesize,((y+h/2)-tilesize)-i*tilesize],"tile_address":\
      [i,j],"size":tilesize,"colour":tileClr[tileClr.index(mtx[i][j])+1]})
    tileGrid.append(tileRow)
    tileRow=[]
  return tileGrid

# Transposes grid data into an image and compiles
# the image drawing data into a list.
def gridToImage(pathVtcs,grid):
  drawData=[]
  polyData=[]
  # Rewrote matrixToGrid() so grid keeps matrix structure
  # for easier addressing; must reflatten to avoid rewriting
  # following functions.
  grid=flattenAll(grid)
  pthClr=[]
  for tile in grid:
    if tile["type"]==PATH:
      pthClr=tile["colour"]
    elif tile["type"]==ENTRY or tile["type"]==EXIT:
      drawData.append("set_color("+str(tile["colour"][0])\
      +","+str(tile["colour"][1])+","+str(tile["colour"][2])+")")
      drawData.append("fill_rect("+str(tile["pxl_address"][0])+\
      ","+str(tile["pxl_address"][1])+","+str(tile["size"])+\
      ","+str(tile["size"])+")")
  for vtcs in pathVtcs:
    polyData.append(polyDraw(vtcs,pthClr))
  for data in polyData:
    for line in data:
      drawData.append(line)
  return drawData

# Translates coordinate list into polygon drawing data.
def polyDraw(vtcs,clr=[0,0,0]):
  xLst=[]
  yLst=[]
  polyData=[]
  for vtx in vtcs:
    xLst.append(vtx[0])
    yLst.append(vtx[1])
  polyData.append("set_color("+str(clr[0])+","+str(clr[1])\
  +","+str(clr[2])+")")
  polyData.append("fill_poly("+str(xLst)+","+str(yLst)+")")
  return polyData

# EFFICIENCY FUNCTIONS
####################
# The following group of functions extract vertices from
# joined grid tiles to draw a single polygon rather than
# individual tiles.
####################
# Groups matrix cells that are adjacent to eachother.
# Cells are identified by target value.
def groupCells(mtx,target,scandir=0):
  group=[] # Groups adjacent cells.
  cellGroups=[] # Holds cell groups.
  if scandir==1: # horizontal=0, vertical=1
    mtx=tpose(mtx)
  for row in range(len(mtx)):
    for col in range(len(mtx[row])):
      if mtx[row][col]==target:
        if scandir==0:
          group.append([row,col])
        elif scandir==1:
          group.append([col,row])
      elif group!=[]:
        cellGroups.append(group)
        group=[]
    if group!=[]:
      cellGroups.append(group)
      group=[]
  return cellGroups

# Replace cell group with corresponding grid tiles.
def cellsToTiles(cellgroup,grid):
  # Rewrote matrixToGrid() so grid keeps matrix structure
  # for easier addressing; must reflatten to avoid rewriting
  # following functions.
  grid=flattenAll(grid)
  tileGroup=cellgroup.copy()
  for row in range(len(tileGroup)):
    for idx in range(len(tileGroup[row])):
      for tile in grid:
        if tile["tile_address"]==tileGroup[row][idx]:
          tileGroup[row][idx]=tile
  return tileGroup

# Gets vertices for a line of tiles.
def getLineVertices(tiles):
  vertices=[]
  lineLen=len(tiles)
  s=tiles[0]["size"]
# Height/width of line of tiles.
  w=s+s*(tiles[lineLen-1]["tile_address"][1]-tiles[0]["tile_address"][1])
  h=s+s*(tiles[lineLen-1]["tile_address"][0]-tiles[0]["tile_address"][0])
  x=tiles[0]["pxl_address"][0]
# Use lowest tile's pxl address if grouped vertically.
  if h<=w:
    y=tiles[0]["pxl_address"][1]
  else:
    y=tiles[lineLen-1]["pxl_address"][1]
  vertices.append([x,y])
  vertices.append([x,y+h])
  vertices.append([x+w,y])
  vertices.append([x+w,y+h])
  return vertices

# Gets the pixel addresses for the critical vertices in a
# tile grid.
def getCritVertices(mtx,grid):
  critVtcs=[]
  lineVtcs=[]
  vtcsH=[]
  vtcsV=[]
# Scan and group tiles horizontally.
  tileGrpH=cellsToTiles(groupCells(mtx,PATH),grid)
# Create set of vertices for horizontally grouped tiles.
  for tiles in tileGrpH:
    lineVtcs=getLineVertices(tiles)
    for vtc in lineVtcs:
      vtcsH.append(vtc)
# Scan and group tiles vertically.
  tileGrpV=cellsToTiles(groupCells(mtx,PATH,1),grid)
# Create set of vertices for vertically grouped tiles.
  for tiles in tileGrpV:
    lineVtcs=getLineVertices(tiles)
    for vtc in lineVtcs:
      vtcsV.append(vtc)
# Find intersection of both vertice sets as those are critical.
  critVtcs=lIntersection(vtcsH,vtcsV)
  return critVtcs

# Put critical vertices in correct order.
def sortVertices(vtcs,grid):
  vtcsSrtd=[]
  lastVtx=[]
  currVtx=[]
  nxtVtcs=[]
  clmFlg=0
  startIdx=0
# Start at vertex that isn't a chequered tile vertex and store.
  currVtx=vtcs[startIdx]
  nTypes=tileNodeTypes(currVtx,grid)
  while nTypes[0]!=nTypes[1] and nTypes[2]!=nTypes[3]:
    startIdx+=1
    currVtx=vtcs[startIdx]
    nTypes=tileNodeTypes(currVtx,grid)
  vtcsSrtd.append(currVtx)
  
  for i in range(len(vtcs)):
# Check if tiles surrounding vertex node are chequered,
# then find next vertices on same row or col depending
# on row/col switch state.
    nTypes=tileNodeTypes(currVtx,grid)
    if nTypes[0]!=nTypes[1] and nTypes[2]!=nTypes[3]:
      clmFlg=not clmFlg
      for j in range(len(vtcs)):
        if vtcs[j]!=currVtx and vtcs[j][clmFlg]==currVtx[clmFlg]:
          nxtVtcs.append(vtcs[j])
      clmFlg=not clmFlg
# Next vertex is above. 
      if lastVtx[1]<currVtx[1]:
# Sort low to high by ordinates to get closest vertex first.
          nxtVtcs=sortByOrds(nxtVtcs)
          for vtx in nxtVtcs:
            if vtx[1]>currVtx[1]:
              lastVtx=currVtx
              currVtx=vtx
              break
# Next vertex is below.
      elif lastVtx[1]>currVtx[1]:
# Sort high to low by ordinates to get closest vertex first.
          nxtVtcs=sortByOrds(nxtVtcs)
          nxtVtcs.reverse()
          for vtx in nxtVtcs:
            if vtx[1]<currVtx[1]:
              lastVtx=currVtx
              currVtx=vtx
              break
# Next vertex is left.
      elif lastVtx[0]>currVtx[0]:
# Sort high to low by abscissas to get closest vertex first.
        nxtVtcs.sort()
        nxtVtcs.reverse()
        for vtx in nxtVtcs:
          if vtx[0]<currVtx[0]:
            lastVtx=currVtx
            currVtx=vtx
            break
# Next vertex is right.
      elif lastVtx[0]<currVtx[0]:
# Sort low to high by abscissas to get closest vertex first.
        nxtVtcs.sort()
        for vtx in nxtVtcs:
          if vtx[0]>currVtx[0]:
            lastVtx=currVtx
            currVtx=vtx
            break
    else:
      for j in range(len(vtcs)):
        if vtcs[j]!=currVtx and vtcs[j][clmFlg]==currVtx[clmFlg]:
          nxtVtcs.append(vtcs[j])
      clmFlg=not clmFlg
# The path to the next vertex must not bisect two like tiles-
# check surrounding tile types if multiple vertices.
      if len(nxtVtcs)>1:
        if clmFlg:
  # Next vertex is above. 
          if nTypes[0]!=nTypes[1]:
  # Sort low to high by ordinates to get closest vertex first.
            nxtVtcs=sortByOrds(nxtVtcs)
            for vtx in nxtVtcs:
              if vtx[1]>currVtx[1]:
                lastVtx=currVtx
                currVtx=vtx
                break
  # Next vertex is below.
          elif nTypes[2]!=nTypes[3]:
  # Sort high to low by ordinates to get closest vertex first.
            nxtVtcs=sortByOrds(nxtVtcs)
            nxtVtcs.reverse()
            for vtx in nxtVtcs:
              if vtx[1]<currVtx[1]:
                lastVtx=currVtx
                currVtx=vtx
                break
        else:
  # Next vertex is left.
          if nTypes[0]!=nTypes[2]:
  # Sort high to low by abscissas to get closest vertex first.
            nxtVtcs.sort()
            nxtVtcs.reverse()
            for vtx in nxtVtcs:
              if vtx[0]<currVtx[0]:
                lastVtx=currVtx
                currVtx=vtx
                break
  # Next vertex is right.
          elif nTypes[1]!=nTypes[3]:
  # Sort low to high by abscissas to get closest vertex first.
            nxtVtcs.sort()
            for vtx in nxtVtcs:
              if vtx[0]>currVtx[0]:
                lastVtx=currVtx
                currVtx=vtx
                break
      else:
        currVtx=nxtVtcs[0]
      nxtVtcs=[]
# End loop once profile complete.
    if currVtx==vtcs[startIdx]:
      break
    else:
      vtcsSrtd.append(currVtx)
# Remove any duplicate vertices
  return rmDup(vtcsSrtd)

# Takes an intersection pixel address and checks
# connected tile types. Reads L→R,T→B.
def tileNodeTypes(pxladd,grid,mask=EMPTY):
  types=[mask,mask,mask,mask]
# Test if pixel address matches a tile corner.
  for tile in grid:
    if pxladd==[tile["pxl_address"][0],tile["pxl_address"][1]+tile["size"]]:
      types[3]=tile["type"]
    elif pxladd==[tile["pxl_address"][0]+tile["size"],tile["pxl_address"][1]+tile["size"]]:
      types[2]=tile["type"]
    elif pxladd==[tile["pxl_address"][0],tile["pxl_address"][1]]:
      types[1]=tile["type"]
    elif pxladd==[tile["pxl_address"][0]+tile["size"],tile["pxl_address"][1]]:
      types[0]=tile["type"]
# Hide entry/exit for profile calculation.
  for idx in range(len(types)):
    if types[idx]==ENTRY or types[idx]==EXIT:
      types[idx]=mask
  return types

# Splits vertice set for each independent path.
def splitPathVtcs(allVtcs,grid):
  # Rewrote matrixToGrid() so grid keeps matrix structure
  # for easier addressing; must reflatten to avoid rewriting
  # following functions.
  grid=flattenAll(grid)
  allPathVtcs=[]
  remVtcs=allVtcs
  while remVtcs!=[]:
    pathVtcs=sortVertices(remVtcs,grid)
    remVtcs=listDiff(remVtcs,pathVtcs)
    allPathVtcs.append(pathVtcs)
  return allPathVtcs
