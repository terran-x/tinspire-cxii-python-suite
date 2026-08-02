# Matrix manipulation functions and subroutines
#================================
from math import *
from sys import *
#================================
# Performs matrix multiplication.
def mtxMult(mtx1,mtx2):
  mtx3=[]
  sum=0
  mtx2=fmtColMtx(mtx2)
  
  if len(mtx1[0])==len(mtx2):
    for i in range(len(mtx1)):
      mtx3.append([])
      for j in range(len(mtx2[0])):
        for k in range(len(mtx2)):
          sum+=mtx1[i][k]*mtx2[k][j]
        mtx3[i].append(sum)
        sum=0
    return fmtColMtx(mtx3,2)
  else:
    print_exception(IndexError("Mtx 1 columns must equal mtx 2 rows"))
    return False

# Scalar multiplication of matrix.
def sclrMult(sclr,mtx):
  rMtx=[]
  mtx=fmtColMtx(mtx)
  for i in range(len(mtx)):
    rMtx.append([])
    for j in range(len(mtx[0])):
      rMtx[i].append(sclr*mtx[i][j])
  return rMtx

# Reformats single row/single col matrices.
def fmtColMtx(mtx,mode=1):
  mtx=mtx.copy()
  # Row matrix→Col matrix
  if mode==1:
    for i in range(len(mtx)):
      if type(mtx[i])!=list:
        mtx[i]=[mtx[i]]
  # Col matrix→Row matrix
  elif mode==2:
    for i in range(len(mtx)):
      if len(mtx[i])==1 and type(mtx[i])==list:
        mtx[i]=mtx[i][0]
  return mtx

# Matrix transposition (rows↔columns)
def tpose(mtx):
  mtx=fmtColMtx(mtx)
  tMtx=[]
  for i in range(len(mtx[0])):
    tMtx.append([])
    for j in range(len(mtx)):
      tMtx[i].append(mtx[j][i])
  return tMtx

# Creates submatrix of target matrix.
def submtx(mtx,r1=1,c1=1,r2=None,c2=None):
  sMtx=[]
  mtx=fmtColMtx(mtx)
  if r1>=1 and c1>=1:
    if r2==None:
      r2=len(mtx)
    if c2==None:
      c2=len(mtx[0])
    for i in range(r1-1,r2):
      sMtx.append([])
      for j in range(c1-1,c2):
        sMtx[i-(r1-1)].append(mtx[i][j])
    return sMtx
  else:
    print_exception(IndexError("Invalid dimensions"))
    return False

# Creates submatrix of a target matrix with target row and col removed.
def submtx2(mtx,i0=1,j0=1):
  if i0<1 or j0<1:
    print_exception(IndexError("Invalid dimensions"))
    return False
  sMtx=[]
  for i in range(len(mtx)):
    sMtx.append([])
    for j in range(len(mtx[0])):
      if i+1!=i0 and j+1!=j0:
        sMtx[i].append(mtx[i][j])
  sMtx.remove([])
  return sMtx

# Finds determinant of n*n matrix.
def det(mtx):
  d=0
  if not is_sqr(mtx):
    print_exception(ValueError("Matrix not square"))
    return False
  if len(mtx)==1:
    d=fmtColMtx(fmtColMtx(mtx),2)[0]
    return d
  for i in range(len(mtx)):
    d+=mtx[i][0]*((-1)**(i))*(det(submtx2(mtx,i+1,1)))
  return d

# Checks if matrix is n*n.
def is_sqr(mtx):
  return len(mtx)==len(fmtColMtx(mtx)[0])

# Checks for singular matrix
def is_snglr(mtx):
  return det(mtx)==0

# Inverts a target matrix.
def invert(mtx):
  if is_snglr(mtx):
    print_exception(ValueError("Matrix is singular"))
    return False
  iMtx=[] # Inverse of target matrix.
  cMtx=[] # Target matrix cofactor matrix.
  mtxDet=det(mtx) # Determinant of target matrix.
  for i in range(len(mtx)):
    cMtx.append([])
    for j in range(len(mtx[0])):
      cMtx[i].append(cofactor(mtx,i+1,j+1))
  iMtx=sclrMult((1/mtxDet),tpose(cMtx))
  return iMtx

# Calculates cofactor of target matrix element.
def cofactor(mtx,i0=1,j0=1):
  return (-1)**(i0+j0)*det(submtx2(mtx,i0,j0))

# 
