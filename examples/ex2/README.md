This example runs one scheduler(cluster) and uses it in different sessions or scripts.
The portnumbers `my_scheduler_port` and `my_dashboard_port` are set by the `client_ssh_command.sh` as environment variables on the **remote** machine.
The python code on the remote machine looks for them using `os.environ` and starts the cluster accordingly.
This code will fail if the environment variables are not set.

* Open first terminal on the client

    * `source  client_ssh_command.sh` which will open a terminal on the server
    * In the server terminal
    ```
    cd ~/ports/examples/ex2
    conda activate bgc_md2
    ipython
    ```
    (content of `server_start_ipython.sh`)
    * start and use the cluster
    ```
    %load server_start_cluster_on_port.py
    %load server_use_cluster_1.py
    ```
* open second console on the client
    *
    ```
    source client_ssh_command.sh
    ```
    * on the server (same effect as  `cd ~/ports/examples/ex2; source server_start_ipython.sh` )
    ```
    cd ~/ports/examples/ex2
    conda activate bgc_md2
    ipython
    ```
    * This time we only have to run the client code
    ```
    %load server_use_cluster_2.py
    ``
    
### Wishlist:
1. If we put the code into the notebooks users have to see that they have to set
   the environment variables. It would be polite to allow the cluster to be started if no variable had been set.
1. It is a bit tiresome to have to call the ssh command and then in the remote shell have to activate the conda environment and  start the ipython session. Since the ssh command already executes code why not go the whole way and start the ipython shell in the activated environment?
1. Since we might start a very long computation and might lose connection meanwhile we could actually go one step further and start a tmux session remotely, activate the environment and start an ipython instance...
1. The local port is still duplicated between the browser start and the local port forward ssh command.  
