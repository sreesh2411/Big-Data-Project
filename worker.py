

import socket
import sys
import json
import threading
import time

work_id = int(sys.argv[2])
port1 = int(sys.argv[1])


def init():
    global s
    s = socket.socket()
    port = port1
    s.bind(('', port)) 
    print ("socket binded to %s" %(port))
    s.listen(1)   
    print ("socket is listening")

def send(request):
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
		soc.connect(("localhost", 5001))
		message=json.dumps(request)
		soc.send(message.encode())
init()
#print(port)
resources={}
def rec():
    try: 
        while True:
            c, addr = s.accept()            
            a=c.recv(1024)
            b=json.loads(a)
            #resources[b[0]]=b[1]   
            assigned = threading.Thread(target=run, args=(b,))
            assigned.start()
        s.close()
    except:
        s.close()
def run(b):                  
            time.sleep(b[1])
            send(b[0])

                
                
    
            

t1=threading.Thread(name="input",target=rec)
t1.start()
t1.join()