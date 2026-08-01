#=======================
from ti_game import *
from ti_system import *
from conv_asc import *
#=======================
def hs_export(list):
  expArr=[]
  nmAsc=[]
  for i in range(0,len(list)):
    nmAsc=to_ascii(list[i].name)
    for j in range(0,len(nmAsc)):
      expArr.append(nmAsc[j])
    expArr.append(list[i].score)
  return expArr

def hs_import(hsData):
  impLst=[]
  nmLst=[]
  for i in range(0,len(hsData),4):
    for j in range(i,i+3):
      nmLst.append(hsData[j])
    impLst.append(hscore(to_char(nmLst),hsData[i+3]))
    nmLst=[]
  return impLst
