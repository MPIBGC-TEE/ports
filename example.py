from dask.distributed import LocalCluster, Client
import os
# check if we have wishes regarding port numbers expressed in environment variables
env = os.environ
my_dashboard_port = env['my_dashboard_port'] if 'my_dashboard_port' in env.keys() else ':0' 
my_scheduler_port= env['my_scheduler_port'] if 'my_scheduler_port' in evn.keys() else 0
# in case we have executed the script / cell before (in the same ipython/ jupyter kernel) we continue to use the existing client
if not 'client' in dir(): 
    # so we haven't run this part yet but maybe we have a scheduler running (started by another notebook
    # or script and we have told ourselves about it via an exported environment variable
    if my_scheduler_port != 0:
        my_cluster_address = 'localhost:'+env['my_scheduler_port']
        try:
            client = Client(my_cluster_address,timeout=1)
            # in this case we have no influence on the dashboard
            # since it is a property of the allready running cluster
            cluster = client.cluster
        except: ConnectionRefusedError
            # ok no cluster talking to us, so we will start one
            cluster = LocalCluster(
                scheduler_port=my_scheduler_port,
                dashboard_adress=my_dashboard_address
            )
            # @Holger: for the cardamon notebooks
            # The function prepare_cluster should  no longer reference 
            # any ports or names internally (because they have nothing to do wiht bgc_md2 , let alone 
            # CARDAMOM but it should accept the  two arguments and pass them on.
            #
            #
            # cluster = prepare(
            #    scheduler_port=my_scheduler_port,
            #    dashboard_adress=my_dashboard_address
            #)

    else:
        #no information about a running  cluster
        cluster = LocalCluster(
            dashboard_adress=my_dashboard_address
        )
        # or if one needs something special    
        # cluster = prepare(
        #    dashboard_adress=my_dashboard_address
        #)

    client = Client(cluster)

# here the normal code starts
