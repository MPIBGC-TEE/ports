from dask.distributed import LocalCluster

cluster = LocalCluster(
    memory_limit='500MB' # this will be passed on to the worker
)
cluster.dashboard_address
