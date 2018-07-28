import matplotlib.pyplot as plt
#import matplotlib.ticker
from matplotlib.ticker import FuncFormatter
import numpy as np
import subprocess

#load = {"frv27":[], "frv28":[], "frv29" : [], "frv30" : []}
load = {"frv71":[]}
time = []

def time_range (x,pos):
 try:
    return time[int(x)]
 except:
    return "NaN"

formatter = FuncFormatter(time_range)

#load_files = subprocess.check_output('ls *.txt', shell=True).strip().split()
load_files = ["frv71.txt"]

for load_file in load_files:
 load_name = load_file.split('.')[0]
 for line in open(load_file,'r'):
  try:
    time.append(line.strip().split('\t')[0].split()[3][:-3])
    load[load_name].append(line.strip().split('\t')[1].replace(',','.'))
  except:
    pass




fig, ax = plt.subplots()
ax.xaxis.set_major_formatter(formatter)

t = np.arange(0, len(load["frv71"]), 1)
y = np.arange(0, 51, 1)
#ax.xaxis.set_ticks(np.arange(min(t), max(t), 3600))
#ax.yaxis.set_ticks(y)
#plt.ylim([0,50])
plt.plot(t,load["frv71"], label="frv71",color='black')
#plt.plot(load["frv28"], label="frv28",color='blue')
#plt.plot(load["frv29"], label="frv29",color='green')
#plt.plot(load["frv28"], label="frv30",color='purple',alpha=50)
plt.legend()
plt.plot((min(t), max(t)+1000), (28,28), 'red', lw=4)
plt.xlabel('time')
plt.ylabel('load average')
plt.title('Load average of MXs')
plt.grid(True)
plt.savefig("test.png", dpi=300)
plt.show()
