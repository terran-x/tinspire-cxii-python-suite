#################
#Developer tools
################
import __main__
import array
import binascii
import builtins
import cmath
import collections
import ctypes
import errno
import gc
import hashlib
import heapq
import math
import micropython
import random
import re
import sys
import ti_picture
import ti_st
import ti_system
import time
import ti_draw
import ti_innovator
####################
def pyref():
  mdls=["__main__ ","array","binascii","builtins","cmath","collections","ctypes","errno","gc","hashlib","heapq","int","math","micropython","random","re","str","sys","ti_draw","ti_innovator","ti_picture","ti_st","time","ALL"]
  for i in range(0,len(mdls)/2):
    cstr=str(i+1)+". "+mdls[i]
    while ti_draw.string_size(cstr)[0]<100:
      cstr+=" "
    print(cstr+str(int(len(mdls)/2+i+1))+". "+mdls[int(len(mdls)/2+i)])
    
  slxn=input("Enter selection: ")
  if slxn=="1":
    help(__main__)
  elif slxn=="2":
    help(array)
  elif slxn=="3":
    help(binascii)
  elif slxn=="4":
    help(builtins)
  elif slxn=="5":
    help(cmath)
  elif slxn=="6":
    help(collections)
  elif slxn=="7":
    help(ctypes)
  elif slxn=="8":
    help(errno)
  elif slxn=="9":
    help(gc)
  elif slxn=="10":
    help(hashlib)
  elif slxn=="11":
    help(heapq)
  elif slxn=="12":
    help(1)
  elif slxn=="13":
    help(math)
  elif slxn=="14":
    help(micropython)
  elif slxn=="15":
    help(random)
  elif slxn=="16":
    help(re)
  elif slxn=="17":
    help("")
  elif slxn=="18":
    help(sys)
  elif slxn=="19":
    help(ti_draw)
  elif slxn=="20":
    help(ti_innovator)
  elif slxn=="21":
    help(ti_picture)
  elif slxn=="22":
    help(ti_st)
  elif slxn=="23":
    help(time)
  elif slxn=="24":
    help(__main__)
    help(array)
    help(binascii)
    help(builtins)
    help(cmath)
    help(collections)
    help(ctypes)
    help(errno)
    help(gc)
    help(hashlib)
    help(heapq)
    help(1)
    help(math)
    help(micropython)
    help(random)
    help(re)
    help("")
    help(sys)
    help(ti_draw)
    help(ti_innovator)
    help(ti_picture)
    help(ti_st)
    help(time)
  else:
    print("Enter index within range")

# Function runtime tester
def func_spd_test(func,iter=1):
  rslts=[]
  for i in range(iter):
    start=time.ticks_ms()
    exec(func)
    rslts.append(time.ticks_ms()-start)
  print(str((sum(rslts)/len(rslts))-0.5)+"ms per call") # 0.5 is avg runtime for exec()
  return

# Print functions within a module
def dthelp():
  vars=locals()
  for key in vars.keys():
    if type(vars[key]).__name__=="function":
      print(key)

# 
