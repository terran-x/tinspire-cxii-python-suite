#now=date(hr=get_time()[0:2],min=get_time()[3:5],sec=get_time()[6:],day=get_date()[0:2],mth=get_date()[3:5],yr=get_date()[6:])
#create a now date object
#==================
from time import *
from ti_system import *
from math import *
#==================
# Time setter.
def set_time():
  tme=input("Enter time (24-hour format, HH.MM.SS): ")
  dte=input("Enter date (DD/MM/YYYY): ")
  hr=int(tme[:tme.find(".")])
  tme=tme[tme.find(".")+1:]
  min=int(tme[:tme.find(".")])
  tme=tme[tme.find(".")+1:]
  sec=int(tme)
  day=int(dte[:dte.find("/")])
  dte=dte[dte.find("/")+1:]
  mth=int(dte[:dte.find("/")])
  dte=dte[dte.find("/")+1:]
  yr=int(dte)
  adjSecs=date().date_diff(date(hr,min,sec,day,mth,yr))-time()
  curDate=localtime(adjSecs+time())
  store_value("adjustment",adjSecs)
  timeStr=tFormat(curDate,1)+", "+tFormat(curDate,2)
  return timeStr

# Time getter.
def get_time():
  try:
    adjTime=recall_value("adjustment")
  except:
    adjTime=0
  curTime=localtime(int(adjTime)+time())
  tm=tFormat(curTime,1)
  return tm

# Date getter.
def get_date():
  try:
    adjDate=recall_value("adjustment")
  except:
    adjDate=0
  curDate=localtime(int(adjDate)+time())
  dt=tFormat(curDate,2)
  return dt

def tFormat(lTime,mode):
  if mode==1:
    s=str(lTime[5])
    m=str(lTime[4])
    h=str(lTime[3])
    if len(s)<2:
      s="0"+s
    if len(m)<2:
      m="0"+m
    if len(h)<2:
      h="0"+h
    time=h+":"+m+":"+s
    return time
  elif mode==2:
    d=str(lTime[2])
    m=str(lTime[1])
    y=str(lTime[0])
    if len(d)<2:
      d="0"+d
    if len(m)<2:
      m="0"+m
    date=d+"/"+m+"/"+y
    return date

# Fixed date object.
class date:
  def __init__(self,hr=localtime(0)[3],min=localtime(0)[4],sec=localtime(0)[5],day=localtime(0)[2],mth=localtime(0)[1],yr=localtime(0)[0]):
    self.time=[int(hr),int(min),int(sec)]
    self.date=[int(day),int(mth),int(yr)]

  def __gt__(self,other):
    for i in range(len(self.date),0,-1):
      if self.date[i-1]>other.date[i-1]:
        return True
      elif self.date[i-1]<other.date[i-1]:
        return False
    for i in range(len(self.time)):
      if self.time[i]>other.time[i]:
        return True
      elif self.time[i]<other.time[i]:
        return False
    return False

# Calculates seconds between epoch (0 AD) and date obj.
  def epoch_secs(self):
    daysInMth=[31,28,31,30,31,30,31,31,30,31,30,31]
    ly=0
    epSecs=0
    
    # Leap year check. -1 if cur year=leap year.
    if self.date[2]%4==0:
      ly=int(floor(self.date[2]/4))-1
      daysInMth[1]=29
    else:
      ly=int(floor(self.date[2]/4))
    
    # Years to seconds and sum.
    epSecs+=(self.date[2]*365*24*60*60)+(ly*24*60*60)
    # Months to seconds and sum.
    for i in range(self.date[1]-1):
      epSecs+=daysInMth[i]*24*60*60
    # Days to seconds and sum.
    epSecs+=(self.date[0]-1)*24*60*60
    # Hours to seconds and sum.
    epSecs+=(self.time[0])*60*60
    # Minutes to seconds and sum.
    epSecs+=self.time[1]*60
    # Sum seconds.
    epSecs+=self.time[2]
    
    return epSecs

# Date difference in seconds.
  def date_diff(self,other):
    return int(fabs(self.epoch_secs()-other.epoch_secs()))

def help():
  mthds=["Date functions: ","set_time()","get_time()","get_date()","","Date class:","date(hour,min,secs,day,month,year)","date.epoch_secs()","date.date_diff(other)"]
  for i in range(0,len(mthds)):
    print(mthds[i])
  return
