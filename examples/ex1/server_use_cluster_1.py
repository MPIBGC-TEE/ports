from dask.distributed import Client
# check if we have wishes regarding port numbers expressed in environment variables
#
my_scheduler_port = 8900
my_scheduler_address='localhost:'+str(my_scheduler_port)
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
    darr = dask.array.stack(args)
    res_arr = darr.map_blocks(f)
    res_arr.compute()
    print(time.time()-ts)


computation()
