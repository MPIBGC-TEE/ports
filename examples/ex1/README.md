This example runs one scheduler(cluster) and uses it in different sessions or scripts.
The small shell scripts are not necessary,but will become part of a bigger one later
* open first console on the client
  * on the client ( content of `client_ssh_command.sh`)
  ```
  localPort=8081
  remoteDashboardPort=8911
  ssh -L ${localPort}:localhost:${remoteDashboardPort} matagorda-from-home

  ```

  * on the server (content of `server_start_ipython.sh` )
  ```
  conda activate bgc_md2
  ipython
  ```
  *
  ```
  %load server_start_cluster_on_port.py
  %load server_use_cluster_1.py
  ```

* open second console on the client
  * on the client ( content of `client_ssh_command.sh`)
    ```
    localPort=8081
    remoteDashboardPort=8911
    ssh -L ${localPort}:localhost:${remoteDashboardPort} matagorda-from-home

    ```
  * on the server (content of `server_start_ipython.sh` )
    ```
    conda activate bgc_md2
    ipython
    ```
  * This time we only have to run the client code
    ```
    %load server_use_cluster_2.py
    ```


### Wishlist
* Here all the port numbers are hard coded. This leads to duplication:
   * between the dashboard port number in the `client_ssh_command.sh` and ```server_start_cluster_on_port.py```
   * between the scheduler port number in the ```server_start_cluster_on_port.py``` and the scripts `server_use_cluster_1.py` and 	`server_use_cluster_2.py` that use the scheduler.
   We are obviously looking for a way to avoid this. Could we possibly use our ssh command on the client to prepare the environment on the server side?
