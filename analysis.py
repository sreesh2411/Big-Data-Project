
import json
tasks=["RR_Tasks.txt","Random_Tasks.txt","LL_Tasks.txt"]
jobs=["RR_Jobs.txt","Random_Jobs.txt","LL_Jobs.txt"]
for i in tasks:
    with open(i,"r") as f:
        task=json.loads(f.read())
        total=[]
        for j in task:
            total.append(task[j])
        total=sorted(total)
        if len(total)%2 == 0:
            median=(total[int(len(total)/2)]+total[int((len(total)/2)+1)])/2
        else:
            median=total[int((len(total)+1)/2)]
        mean=sum(total)/len(total)
        print(i)
        print("mean :",mean)
        print("median :",median)
            