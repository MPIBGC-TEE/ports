from dask.distributed import LocalCluster #, Client

# The following numbers are userspecific (for mm), 
my_dashboard_address = 'localhost:8912'
my_scheduler_port =8900
cluster = LocalCluster(
    scheduler_port=int(my_scheduler_port),
    dashboard_address=my_dashboard_address,
    memory_limit='500MB' # this will be passed on to the worker
)
