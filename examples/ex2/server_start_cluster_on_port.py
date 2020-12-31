from dask.distributed import LocalCluster 
import os
env = os.environ
my_dashboard_address = env['my_dashboard_address'] if 'my_dashboard_address' in env.keys() else '0' 
my_scheduler_port = env['my_scheduler_port'] if 'my_scheduler_port' in env.keys() else '0'
cluster = LocalCluster(
    scheduler_port=int(my_scheduler_port),
    dashboard_address=my_dashboard_address,
    memory_limit='500MB'  # this will be passed on to the workers
)
