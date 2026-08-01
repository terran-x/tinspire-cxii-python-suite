class hscore:
  def __init__(self,nm="AAA",scr=0):
    self.name=nm
    self.score=scr
  
  def __lt__(self,other):
    return self.score<other.score
  def __gt__(self,other):
    return self.score>other.score
  def __le__(self,other):
    return self.score<=other.score
  def __ge__(self,other):
    return self.score>=other.score
  def __eq__(self,other):
    return self.score==other.score
  def __ne__(self,other):
    return self.score!=other.score

class scoreboard:
  def __init__(self,name="",scrlst=[],maxState=5):
    self.name=name
    self.entries=maxState
    self.scores=scrlst
    if len(self.scores)<self.entries:
      for i in range(0,self.entries-len(self.scores)):
        self.scores.append(hscore())

  def sort(self):
    hold=0
    for i in range(0,len(self.scores)-1):
      for j in range(0,len(self.scores)-1):
        if self.scores[j+1]>self.scores[j]:
          hold=self.scores[j]
          self.scores[j]=self.scores[j+1]
          self.scores[j+1]=hold

  def trim(self):
    tempArr=[]
    if len(self.scores)>self.entries:
      for i in range(0,self.entries):
        tempArr.append(self.scores[i])
      self.scores=tempArr

  def update(self,scrObj):
    self.scores.append(scrObj)
    self.sort()
    self.trim()
    for i in range(0,len(self.scores)):
      if self.scores[i]==scrObj:
        return 1
    return 0

def help():
  print("hscore(\"name\",\"score\")-<class>")
  print("scoreboard(\"name\",\"score array\",\"max entries\")-<class>")
  print("  --sort()-<function>")
  print("  --trim()-<function>")
  print("  --update(\"hscore object\")-<function>")
