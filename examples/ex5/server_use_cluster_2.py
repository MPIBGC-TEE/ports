from dask.distributed import Client
import os
env = os.environ
my_scheduler_port = env['my_scheduler_port_1'] 
my_scheduler_address = 'localhost:'+my_scheduler_port
client = Client(my_scheduler_address)
print(client)

# do something with the client
import dask.array
import numpy as np
import time 

sn=200
n=400
def f(arr):
    for i in range(40): # keep busy
        res = np.matmul(arr, arr)
    return res

args = [i*np.eye(n) for i in range(sn)]


def computation():
    ts = time.time()
    big_future = client.scatter(args)
    futures = client.map(f, big_future)
    results = [fut.result() for fut in futures]
    results
    print(time.time()-ts)


computation()
