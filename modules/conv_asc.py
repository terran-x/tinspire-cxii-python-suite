######
def to_ascii(string):
  ascArr=[]
  for i in range(0,len(string)):
    ascArr.append(ord(string[i]))
  return ascArr

def to_char(array):
  chrStr=""
  for i in range(0,len(array)):
    chrStr+=chr(array[i])
  return chrStr

# 
