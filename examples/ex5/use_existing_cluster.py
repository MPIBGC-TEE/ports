
import os
from dask.distributed import Client
# check if we have wishes regarding port numbers expressed in environment variables
env = os.environ
my_scheduler_port = env['my_scheduler_port'] if 'my_scheduler_port' in env.keys() else '0'
#
client = Client('localhost:'+env['my_scheduler_port'])

# do something with the client
import numpy as np
[fut.result()  for fut in client.map(f,[i*np.ones(100000) for i in range(1000)])]
