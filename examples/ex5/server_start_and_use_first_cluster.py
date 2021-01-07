from dask.distributed import LocalCluster 
import os
env = os.environ
my_dashboard_address = env['my_dashboard_address_1'] if 'my_dashboard_address_1' in env.keys() else '0' 
my_scheduler_port = env['my_scheduler_port_1'] if 'my_scheduler_port_1' in env.keys() else '0'
cluster = LocalCluster(
    scheduler_port=int(my_scheduler_port),
    dashboard_address=my_dashboard_address,
    memory_limit='500MB'  # this will be passed on to the workers
)

# now use it
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
    darr = dask.array.stack(args)
    res_arr = darr.map_blocks(f)
    res_arr.compute()
    print(time.time()-ts)


computation()
