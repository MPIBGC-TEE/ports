# preliminary information 

* Server applications provide their services to ports  
  Examples are jupyter notebook servers, dask dashboards 

* the 2^16 ports are a system resource shared by all users and applications
  There are some guidelines about who should listen where https://en.wikipedia.org/wiki/Port_(computer_networking)
  but for our purposes
  its a matter of choice and mainly a question of keeping out of each others way.

* The same dask cluster can be used by many clients (in many notebooks) simultanuously
* Several dask clusters per machine are possible, but the fewer the better.
  The optimal solution for a high performance computing scenario would be a
  single cluster per machine shared by all users and all clients, since a single
  cluster can handle any number of clients and can share the available resources
  between them. If its the only cluster on the machine it could use all the
  available resources and distribute them efficiently between all the clients.
  A single cluster shared by all user would however again
  necessiate some maintainance and precautions. In case of a failure it would
  affect all users and make it difficult to switch off without fear of
  interrupting someone else's work.  If we run many clusters we will have to make
  sure that they do not assume the complete resources of the machine, especially
  memory wise.  
  One cluster per user is again a compromise to gain flexibility at
  the cost of perfect resource distribution as long as the number of users is
  very small.

* To achieve robustness and general independence from network connections to the server we use a terminal multiplexer for all text based output on the server (tmux)
  From the perspective of the server the tmux server looks like a local (server) 
  konsole window it can send its output to regardless of any network connection.
  The network connection is only necessary when can connect to the tmux server from 
  a different machine.

# Example using ipython 

## port consumption
The only ports we have to worry about are the 
* dask cluster/sheduler port
  We do not actively communicate with the cluster but fixing its ports provides 
  the possibility to detect the presence of a running cluster and reuse it from 
  several ipython sessions. This is 
  * faster since startup and tear down of a cluster take some seconds
  * more efficient because we dont have to share resources (especially memory) 
  q  manually between different ipython sessions.

* the port of the dask dashboard(s) 

## code examples
### ipython in a tmux session

#### Plan:
*  We start with a minimal python code that we want to run.
*  We show the commands (on client and server) necessary to 
  * open a tmux window
  * activate the (conda) environment
  * start an ipython session 
  * connect via ssh from a client machine over the network 
  * redirect the web output of the dask dashboard to a port on the local machine
  * start the browser on the local client with the correct port number.
*  We then build a single shell command executable on the client that
   automates all the above steps.

## The python code:
```python
import os
from dask.distributed import LocalCluster, Client

if os.environ.hasmy_scheduler_port]
my_scheduler_port 



# Motivational Example with notebooks: most general usage scenario:#
Assume you have two or more different conda environments on matagorda and
running at least one notebook for each.  This has the following consequences:
Since the jupyter (notebook or lab) server is started in the same conda env
that is used by the code in the notebooks you wll have to start two different
jupyter servers on matagorda.  They will use two different ports jsp1, jsp2 on
matagorda.  If the notebooks use a dask clients every client will use its own
dashboard with its own port.  All clients may (and should) use the same
scheduler or cluster.  

 We have the following summary of port consumption on one machine for one user:
 ```n_envs + n_client + n_cluster```   where 
 - `n_envs` is the number of conda environments with their respective jupyterservers
 - `n_clients` is the number of clients (and equal to the number of notebooks that use dask)

To be able to connect to these servers with the browser on your local machine you will have to forward the two ports. 
  
