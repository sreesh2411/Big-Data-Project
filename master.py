import sys
import socket
import json
import threading
import time
import random
from threading import Lock
lock = Lock()
#lock1= Lock()
w=dict()
dependencies={}
queue=[]
log={}
sch=sys.argv[1]



if sch == "RR":
    taskfile='RR_Tasks.txt'
elif sch == "Random":
    taskfile='Random_Tasks.txt'
elif sch == "LL":
    taskfile='LL_Tasks.txt'

if sch == "RR":
    jobfile='RR_Jobs.txt'
elif sch == "Random":
    jobfile='Random_Jobs.txt'
elif sch == "LL":
    jobfile='LL_Jobs.txt'

if sch == "RR":
    logfile='RR_Log.txt'
elif sch == "Random":
    logfile='Random_Log.txt'
elif sch == "LL":
    logfile='LL_Log.txt'

timeis=dict()
timejob=dict()
def rem(id):
    for i in w:
        if(id in w[i][0]):
            w[i][0][w[i][0].index(id)]=None
def ifempty(ie):
    if(None in w[ie][0]):
        return True
    else:
        return False

def readfile():    
    with open("config.json","r") as f:
        workers=json.loads(f.read())
    for i in workers["workers"]:
        w[i['worker_id']]=([None for i in range(i["slots"])],i["port"]) 
    print(w)

def init1():
    global s 
    s = socket.socket()
    port = 5000
    s.bind(('', port))        
    print ("socket binded to %s" %(port))
    s.listen(1)   
    print ("socket is listening")
def init2():
    global so
    so = socket.socket()
    port = 5001
    so.bind(('', port))        
    print ("socket binded to %s" %(port))
    so.listen(3)   
    print ("socket is listening")
    
def send_request(request,work_port):
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
		soc.connect(("localhost", work_port))
		message=json.dumps(request)
		soc.send(message.encode())

loop=0
global start
start=time.time()
prev=0
def requ():
        global start
        global loop

        
        while True:
            
            c, addr = s.accept()
            start=time.time()
            a=c.recv(1024)
            b=json.loads(a)
            # if(start==0):     
            #     start=time.time()
            #     print(start)
            temp=[]
            temp.append(dict((i["task_id"],i["duration"]) for i in b['map_tasks']))
            temp.append(dict((i["task_id"],i["duration"]) for i in b['reduce_tasks']))
            dependencies[b["job_id"]]=temp
            timejob[b["job_id"]]=time.time()
            #print(i)
            lock.acquire()
            for g in temp[0]:
                  queue.append([g,temp[0][g]])
            # print(1,queue)
            lock.release()
        s.close()
def rec():
    global start
    global prev
    # prev=start
    
    while True:
                
            #print(dependencies)
            c, addr = so.accept()
            #timeit=time.time()
            a=c.recv(1024)
            b=json.loads(a)
            timeis[b]=time.time()-timeis[b]
            # prev=timeit
            #b=json.loads(a)
            print('out',b)
            #print(queue)
            #print(w)
            rem(b)
            
            #lock.acquire()
            deptem=dependencies.copy()
            for d in deptem:
                if b in deptem[d][0]:
                    #print(dependencies[d])
                    dependencies[d][0].pop(b)
                    if len(dependencies[d])==2:
                        if dependencies[d][0] == {}:
                            lin=0
                            lock.acquire()
                            dependencies[d].remove({})
                            for c in deptem[d][0]:
                                queue.insert(lin,[c,dependencies[d][0][c]])
                                lin+=1
                            lock.release()
                            break
                    if len(dependencies[d])==1:
                        if dependencies[d][0] == {}:
                            dependencies[d].remove({})
                            timejob[d]=time.time()-timejob[d]                            
                            dependencies.pop(d)
                            #lock.release()
                            break
            
            if queue==[]:
                log[time.time()-start]=[len([i for i in w[1][0] if i != None]),
                                        len([i for i in w[2][0] if i != None]),
                                        len([i for i in w[3][0] if i != None])]
            if (dependencies=={} and queue==[]):
                with open(taskfile,"w") as f:
                    json.dump(timeis,f,indent=4,sort_keys=True)
                with open(jobfile,"w") as f:
                    json.dump(timejob,f,indent=4,sort_keys=True)
                with open(logfile,"w") as f:
                    json.dump(log,f,indent=4,sort_keys=True)
                    
                        
            
    so.close()
    
def dep():
    global loops
    loop=0
    global start
    start=time.time()
    # log[time.time()-start]=[len([i for i in w[1][0] if i != None]),
    #                         len([i for i in w[2][0] if i != None]),
    #                         len([i for i in w[3][0] if i != None])]
    while True:
        
        lock.acquire()
        if(queue!=[]):
            
            #print(w)
            #print(1)
            if sch=="RR":
                    if(ifempty(1) | ifempty(2) | ifempty(3)):
                        for h in range(len(w)):
                            if(None in w[(loop)%3+1][0]):
                                #print(loop)
                                
                                w[(loop%3)+1][0][w[(loop%3)+1][0].index(None)]=queue[0][0]
                                timetemp=queue[0][0]
                                #print(w[1][0],w[2][0],w[3][0])
                                mess=[queue[0][0],queue[0][1]]
                                queue.remove(queue[0])
                                # lock.release()
                                #print(mess,w[(loop%3)+1][1])
                                send_request(mess,w[(loop%3)+1][1])
                                print(w)
                                timeis[timetemp]=time.time()
                                loop+=1
                                #time.sleep(1)
                                
                                break
                            loop+=1
                        lock.release()
                    else:
                        lock.release()
            elif sch=="Random":
                    if(ifempty(1) | ifempty(2) | ifempty(3)):
                        temr=w.keys()
                        tt1=list(temr)
                        # random.shuffle(tt1)
                        # print(tt1)
                        ret=random.choice(tt1)
                        if(ifempty(ret)):
                            w[ret][0][w[ret][0].index(None)]=queue[0][0]
                            timetemp=queue[0][0]
                            #print(w)
                            mess=[queue[0][0],queue[0][1]]
                            queue.remove(queue[0])
                            #print(mess,w[ret][1])
                            send_request(mess,w[ret][1])
                            print(w)
                            timeis[timetemp]=time.time()
                            #lock.release()
                        lock.release()
                    else:
                        lock.release()
            elif sch=="LL":                    
                    if(ifempty(1) | ifempty(2) | ifempty(3)):
                        free=1
                        for ll in w:
                            if w[ll][0].count(None) > w[free][0].count(None):
                                free=ll
                        w[free][0][w[free][0].index(None)]=queue[0][0]
                        timetemp=queue[0][0]
                        
                        #print(w)
                        mess=[queue[0][0],queue[0][1]]
                        queue.remove(queue[0])
                        lock.release()
                        send_request(mess,w[free][1])
                        print(w)
                        timeis[timetemp]=time.time()
                    else:
                        lock.release()
                        time.sleep(1)
            log[time.time()-start]=[len([i for i in w[1][0] if i != None]),
                              len([i for i in w[2][0] if i != None]),
                              len([i for i in w[3][0] if i != None])]            
        

            
            
        else:
            lock.release()

# def par():
#     log=dict()
#     end=0
#     while True:
#         if(ifempty(1) | ifempty(2) | ifempty(3)):
#             temp=dict()
#             temp[1]=[len([i for i in w[1][0] if i != None]),time.time()]
#             temp[2]=[len([i for i in w[2][0] if i != None]),time.time()]
#             temp[3]=[len([i for i in w[3][0] if i != None]),time.time()]
        
    

        
readfile()
init1()
init2()
t1=threading.Thread(name="requests thread",target=requ)
t2=threading.Thread(name="rec thread",target=rec)
t3=threading.Thread(name="queue thread",target=dep)
# t4=threading.Thread(name="disp thread",target=log)
t1.start()
t2.start()
t3.start()
# t4.start()
t1.join()
t2.join()
t3.join()
# t4.join()