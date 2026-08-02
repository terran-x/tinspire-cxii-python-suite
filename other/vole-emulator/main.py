################
# VOLE EMULATOR
################
# Vole is a hypothetical CPU presented as a learning
# aid in "Computer Science: An overview, 13th Ed."
# (ISBN-10: 1-292-26342-3)
################
from CPU import *
from programs import *
################
# Set up CPU with vole specs.
vole=CPU(16,8,256,8)

def runTest():
  # Store values for program manipulation.
  vole.mainMem[0x6c]=0xff
  vole.mainMem[0x6d]=0xa
  # Initialise program counter register.
  vole.progCounter=0x0
  # Store program in RAM.
  vole.storeProg(progFormat(TEST))
  # Start CPU
  vole.run()
  # Display result
  print(vole.mainMem[0x6e])
  # Clear CPU
  vole.clear()

# Framework for "for loop"
def runLoop():
  vole.progCounter=0xa4
  vole.storeProg(progFormat(FORLOOP),0xa4)
  vole.run()
  print(vole.registers[0])

# Final question from Ex 2.3 (self-writing code)
#vole.progCounter=0xf0
#vole.storeProg(progFormat("0x10b0 0x20f8 0x1000 0x20f9 0xffff"),0xf0)
#vole.run()
#print(hex(int("0b"+vole.mainMem[0xf8])),hex(int("0b"+vole.mainMem[0xf9])))

## 2.4- Ex12
#vole.progCounter=0x00
#vole.storeProg(progFormat("0x103c 0x115b 0x7201 0x9202 0x22e1 0xb000"),0x00)
#vole.run()
#print(zeroPad(bin(vole.mainMem[0xe1])[2:],8))

# 
