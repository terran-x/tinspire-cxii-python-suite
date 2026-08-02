################
from pFormat import *
from math import *
################
class CPU:
  def __init__(self,regNum,regSize,memCells,cellSize,\
            instrLen=16,opcodeLen=4):
    self.registers=self.initMem(regNum)
    self.mainMem=self.initMem(memCells)
    self.instructionSet=self.initRISC()
    self.memCellCount=memCells
    self.regCount=regNum
    self.registerSz=regSize
    self.memCellSz=cellSize
    self.instructionLength=instrLen
    self.opcodeLength=opcodeLen
    self.progCounter=None
    self.instructionReg=None
  
  # Initialise memory state.
  def initMem(self,memSize):
    memory=[]
    for i in range(memSize):
      memory.append(None)
    return memory
  
  # Clear registers and memory.
  def clear(self):
    self.registers=self.initMem(self.regCount)
    self.mainMem=self.initMem(self.memCellCount)
  
  # Initialise instruction set. Logic circuits simulated by
  # functions.
  def initRISC(self):
    def load(r,x,y):
      xy=int(x+y[2:])
      self.registers[r]=self.mainMem[xy]
    def loadI(r,x,y):
      xy=int(x+y[2:])
      self.registers[r]=xy
    def store(r,x,y):
      xy=int(x+y[2:])
      self.mainMem[xy]=self.registers[r]
    def move(r,s):
      self.registers[s]=self.registers[r]
    def add(r,s,t):
      self.registers[r]=self.registers[s]+self.registers[t]
    # msb is sign bit, exponent 3 bits, mantissa 4 bits.
    def addF(r,s,t):
      # Convert floating-point vals into decimals and sum.
      result=decodeFloat(self.registers[s])+\
           decodeFloat(self.registers[t])
      # Code decimal result to floating-point notation.
      self.registers[r]=encodeFloat(result)
    def or_(r,s,t):
      self.registers[r]=self.registers[s]|self.registers[t]
    def and_(r,s,t):
      self.registers[r]=self.registers[s]&self.registers[t]
    def xor(r,s,t):
      self.registers[r]=self.registers[s]^self.registers[t]
    # "a" in rotate is just a placeholder parameter
    def rotate(r,a,x):
      bitStr=zeroPad(bin(int(self.registers[r]))[2:],self.registerSz)
      for i in range(x):
        bitStr=bitStr[len(bitStr)-1]+bitStr[:len(bitStr)-1]
      self.registers[r]=int("0b"+bitStr)
    def jump(r,x,y):
      xy=int(x+y[2:])
      if self.registers[r]==self.registers[0]:
        self.progCounter=xy
    def halt():
      self.instructionReg=None
      self.progCounter=None
    return [lambda r,x,y:load(int(r),x,y),lambda r,x,y:loadI(int(r),x,y),\
    lambda r,x,y:store(int(r),x,y),lambda r,s,*a:move(int(r),int(s)),\
    lambda r,s,t:add(int(r),int(s),int(t)),lambda r,s,t:addF(int(r),int(s),int(t)),\
    lambda r,s,t:or_(int(r),int(s),int(t)),lambda r,s,t:and_(int(r),int(s),int(t)),\
    lambda r,s,t:xor(int(r),int(s),int(t)),lambda r,a,x:rotate(int(r),int(a),int(x)),\
    lambda r,x,y:jump(int(r),x,y),lambda *a:halt()]
  
  # Stores a program in main memory.
  def storeProg(self,prog,start=0):
    idx=start
    rSz=self.registerSz
    for lNum in range(len(prog)):
      # Handles line splitting when memory cell too small.
      while len(prog[lNum])/rSz>1:
        self.mainMem[idx]=prog[lNum][:rSz]
        prog[lNum]=prog[lNum][rSz:]
        idx+=1
      # Repetition necessary to replicate 'do...while',
      # got to be a better way.
      self.mainMem[idx]=prog[lNum][:rSz]
      prog[lNum]=prog[lNum][rSz:]
      idx+=1
  
  # Retrieves instruction from main memory.
  def getInstruction(self,start):
    instruction=""
    for idx in range(ceil(self.instructionLength/self.memCellSz)):
      # Converts in case of self writing code
      if type(self.mainMem[start+idx])!=str:
        self.mainMem[start+idx]=zeroPad(bin(int(self.mainMem[start+idx]))[2:],8)
      instruction+=self.mainMem[start+idx]
    return instruction
  
  # Executes instruction in instruction register.
  def executeInstruction(self):
    instrxn=self.instructionReg
    regBR=int(log(self.regCount,2)) # Register address bit range
    ocLen=self.opcodeLength
    opCode=int(str("0b"+instrxn[:ocLen]))
    memCode1=str("0b"+instrxn[ocLen:ocLen+regBR])
    memCode2=str("0b"+instrxn[ocLen+regBR:ocLen+2*regBR])
    memCode3=str("0b"+instrxn[ocLen+2*regBR:])
    # Logic circuit functions mapped to op-code.
    self.instructionSet[opCode](memCode1,memCode2,memCode3)
  
  # Run CPU.
  def run(self):
    while self.progCounter!=None:
      # Fetch instruction from program counter location 
      # and store into instruction register.
      self.instructionReg=self.getInstruction(self.progCounter)
      # Step program counter by # mem cells for one instruction.
      self.progCounter+=ceil(self.instructionLength/self.memCellSz)
      # Decode and execute instruction.
      self.executeInstruction()
# 
