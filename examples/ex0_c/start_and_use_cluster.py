# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.6.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# +
import dask.array
from dask.distributed import LocalCluster,Client 
if 'cluster' not in dir():
    cluster = LocalCluster()

client = Client(cluster)

# +
try:
    from ports.server_helpers import print_commands
    print_commands(cluster,local_port=8880)
    
except ImportError as e:
    pass  # module doesn't exist,dont make a fuss 

# +
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
