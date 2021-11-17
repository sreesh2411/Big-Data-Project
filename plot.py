import matplotlib.pyplot as plt
import json
import numpy as np
files=['RR_Log.txt','Random_Log.txt','LL_Log.txt']
time=[]
# for i in range(len(files)):
#     with open(files[i],"r") as f:
#         time.append(json.load(f))
with open(files[1],"r") as f:
        time.append(json.load(f))
#time[0]=sorted(time[0])
x=[float(i) for i in time[0]]
array=np.array(list(time[0].values()))
plt.figure(figsize = (20,20))
plt.plot(x,array.T[0])
plt.plot(x,array.T[1])
plt.plot(x,array.T[2])
plt.xlabel('Time (in seconds)')
plt.ylabel('No. of tasks')
plt.legend(['Worker 1','Worker 2','Worker 3'])
plt.grid()
plt.show()