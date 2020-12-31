This example runs one scheduler(cluster) and uses it in different sessions or scripts.
Here all the port numbers are hardcoded. This leads to duplication:
* between the dashboard port number in the ```client_ssh_command.sh''' and ```server_start_cluster_on_port.py'''
* between the scheduler port number in the ```server_start_cluster_on_port.py''' and the scripts ```server_use_cluster_1.py''' and ```	server_use_cluster_2.py''' that use the scheduler


