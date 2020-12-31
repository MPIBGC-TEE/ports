import os
from dask.distributed import LocalCluster, Client
# check if we have wishes regarding port numbers expressed in environment variables
env = os.environ
my_dashboard_address = env['my_dashboard_address'] if 'my_dashboard_address' in env.keys() else '0' 
my_scheduler_port = env['my_scheduler_port'] if 'my_scheduler_port' in env.keys() else '0'
# in case we have executed the script / cell before (in the same ipython/ jupyter kernel) we continue to use the existing client
print(my_dashboard_address)
print(my_scheduler_port)
#input()
#
if 'client' not in dir():
    #if 'my_scheduler_port' in env.keys():
    try:
        client = Client('localhost:'+env['my_scheduler_port'],timeout=2)
        cluster = client.cluster
    except Exception:
        # ok no cluster talking to us, so we will start one
        cluster = LocalCluster(
            scheduler_port=int(my_scheduler_port),
            dashboard_address=my_dashboard_address
        )
        # @Holger: for the cardamon notebooks
        # The function prepare_cluster should  no longer reference 
        # any ports or names internally (because they have nothing to do wiht bgc_md2 , let alone 
        # CARDAMOM but it should accept the two arguments and pass them on.
        #
        # cluster = prepare_cluster(
        #    scheduler_port=my_scheduler_port,
        #    dashboard_adress=my_dashboard_address
        #)
        client = Client(cluster)

print(cluster)
