################
from math import *
################
# Pads bit streams to target length
def zeroPad(target,length,l=1):
  if l:
    return (length-len(target))*"0"+target[:length]
  else:
    return target[:length]+(length-len(target))*"0"

# Format machine language programs for storing.
def progFormat(program):
  program=program.split(" ")
  for i in range(len(program)):
    program[i]=zeroPad(bin(int(program[i]))[2:],16)
  return program

#  Decimal to binary floating-point.
def encodeFloat(decml,expLen=3,fltSz=8):
  sign=str(10**(copysign(1,decml)*-1))[0] #-1→1;1→0
  intgr=abs(trunc(decml))
  frxn=abs(decml)-intgr
  cutoff=20 # Incase of nonterminating result.
  bias=2**(expLen-1)
  exp=0
  mant=""
  intbits=""
  frxnbits=""
  # Integer to bit string.
  while intgr!=0:
    intbits+=str(intgr%2)
    intgr//=2
  intbits=reverseStr(intbits)
  # Fraction to bit string.
  while frxn!=0 and len(frxnbits)<cutoff:
    frxnbits+=str(trunc(2*frxn))
    frxn=2*frxn-trunc(2*frxn)
  # Encode exponent.
  if len(intbits)>0:
    exp=len(intbits)
  else:
    exp=frxnbits.find("1")*-1
  exp=zeroPad(bin(int(exp+bias))[2:],expLen)
  # Encode mantissa
  if len(frxnbits)>0:
    if len(intbits)==0:
      mant=zeroPad(frxnbits[frxnbits.find("1"):],fltSz-expLen-1,0)
    else:
      mant=zeroPad(intbits+frxnbits,fltSz-expLen-1,0)
  return sign+exp+mant

# Binary floating-point to decimal.
def decodeFloat(bitStr,expLen=3):
  sign=bitStr[0]
  exp=bitStr[1:1+expLen]
  mant=bitStr[1+expLen:]
  bias=2**(expLen-1)
  binFloat=0
  # Convert binary exponent to decimal value.
  exp=int("0b"+exp)-bias
  # Convert mantissa to decimal.
  for i,b in enumerate(mant):
    binFloat+=(2**-(i+1))*int(b)
  # Correct order of magnitude.
  binFloat*=(2**exp)
  return (-1)**int(sign)*binFloat

# Can be achieved using slice with step=-1 in full python.
def reverseStr(str):
  revStr=""
  for i in range(len(str)-1,-1,-1):
    revStr+=str[i]
  return revStr

# 
