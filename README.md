


## Purpose
The package contains examples to facilitate remote computing on matagorda and Antakya mainly concerned with the use of 
[bgc_md2](https://github.com/MPIBGC-TEE/bgc_md2). 
It serves as a gentle use case specific introduction to some of the tools (ssh,tmux,ipython,dask.distributed.LocalCluster). 
Its **main purpose** however is to isolate this site and user specific code.
This is important for the following reasons:
### 1. Separation of concerns
To actually run our [bgc_md2](https://github.com/MPIBGC-TEE/bgc_md2) notebooks we are concerned with three very different things,
of which only one really belongs to [bgc_md2](https://github.com/MPIBGC-TEE/bgc_md2) . 
The other too threaten its long term integrity:
   1. code USING a dask cluster (99.9 percent of the notebook / script code 
      This is the only code that definitely belongs to `bgc_md2' and the only one that
      is portable.
   1. code to ADMINISTER the dask cluster (SET UP/START/STOP/CONFIG) 
      In many use cases this would even be handled by other people (the cluster admins). 
      Ideally bgc_md2 code should run on any dask cluster and not depend on it.
      In our case this is not entirely true, since some notebooks use timeouts for computations
      which excludes clusters with deamonized workers. So our notebooks have to have
      code that starts a dask cluster with the right properties.
      If it can not be avoided entirely, (dask)cluster administration specific code should be kept at a minimum,
      to keep the framework useable elsewhere
   1. code that is entirely specific to a group of users like the whole module
      https://github.com/MPIBGC-TEE/bgc_md2/blob/master/src/bgc_md2/sitespecificHelpers.py
      or the user specific parts of `prepare_cluster' in
      https://github.com/MPIBGC-TEE/bgc_md2/blob/master/src/bgc_md2/models/CARDAMOM/CARDAMOMlib.py
      This code had only intermediate purpose (to avoid spreading of a
      preliminary solution to all notebooks) and has lost its temporary
      justification by the new approach proposed here, which outsources these aspects and only requires
      a minimal and obvious bit of code in the notebooks.
### 2. Explicitness
To be self contained the notebooks have to have a minimum of code that does not belong to `bgc_md2`,
for instance code that starts a cluster if none is found already running.
This code should not be buried in a library, but visible in plain sight of future users of the notebooks so that it
can be easily replaced according to their needs. 

### 3. Deduplication
This will be achieved by the advanced examples mainly by code that is well separated from the package and completely
under user control. Some duplication will remain, where it would conflict with a clear separation of `bgc_md2` or 
reduce explicitness. For instance it is likely that many notebooks will share  a common first cell that 
ensures the existence of a running dask cluster and connects to it. Although some of these cells could be put into 
a library function, this would most likely lead to a function returning the cluster connection thereby 
1. burdening our libraries with code that does not realy belong to bgc_md2 (separation of concerns)
1. obscuring the fact that any cluster would do (reducing explicitness)

## Some bits of information that affects us 
### Ports ###
Server applications provide their services to ports.  
Examples are jupyter notebook servers, dask dashboards but also normal web servers (port80). 
The 2^16 ports are a system resource shared by all users and applicationsThere are some guidelines about who should listen where
https://en.wikipedia.org/wiki/Port_(computer_networking). 
By default the two server application we need use use either a fixed default port  (8888 for the jupyter notebook
server and 8787 for the dask dashboard server) or (in case somebody has already started one of them on the same
machine ) 
an unpredictable dynamic port from the dynamic range.
We could forward this port after the app chose it but could not automate the process.
Our strategy will therefore be to specify to which ports the notebook and the dashboard will be served to and plumb
our forwarding accordingly. The only thing to avoid is that two people try to use the same port.
A simple scheme of a personalized port range will avoid this.
  
### (DASK) clusters
To keep our examples scaleable to supercomputers (with many network connected nodes **without shared memory**) we always use
`dask.distributed.LocalCluster` instances, (even though Antakya and matagorda are just multisocket multicore machines).
The same dask cluster can be used by many clients (in many notebooks) simultanuously, so how many dask clusters should we run? 
There are some possibilities.
* One,
    This would be the optimal solution for a high performance computing scenario where a 
    single dask cluster per (machine or hardware cluster) is shared by all users and all clients, since a single
    cluster can handle any number of clients and can share the available resources
    between them. 
    A single cluster shared by all user would however again
    necessiate some maintainance and precautions. In case of a failure it affects
    affect all users and makes it difficult to switch off without fear of
    interrupting someone else's work. 
* As many as we have (active) notebooks..,
    If we instead run many clusters we will have to make
    sure that they do not assume the complete resources of the machine, especially
    memory wise. 
* One cluster per user 
    This is a compromise to gain flexibility at
    the cost of perfect resource distribution as long as the number of users is
    very small. In practice It turns out that this setup is not much safer against
    oversubscribing (memory wise) but this can be usefull for running small tests.
    (If a notebook connects to an existing dask cluster one does not have to tear down and setup the complete set of workers all the time.
    which can take 20 seconds...)
    This makes testing dask code nearly as fast as normal python code. Therefore many of the examples use this technique.
    Especially for some of our notebooks, which require a cluster started with certain arguments (Holgers CARDAMOM notebooks) 
    it is essecntial to provide the code to start such a cluster in the notebook. (the opposite would require the user to "know" that the notebook requires a special running cluster.

### Tmux ###
To achieve robustness and general independence from network connections to the server we use a terminal multiplexer for all text based output on the server [tmux](https://github.com/tmux/tmux/wiki). From the perspective of the server the tmux server looks like a local console window running on the server, to which it can send its output regardless of any network connection.
The network connection is only necessary when we connect to the tmux server from the terminal on a different machine.
Two tmux commands that you will find using a lot in our scenario are `tmux ls` (list sessions) and `tmux attach -t ${NameOfYourSession}`

### SSH local port forwarding
* Since we use 'local ssh port forwarding' the start messages from a jupyter server about where to point the browser
  are most likely wrong, because they refer to the  port on the remote server. The server has no information to 
  which local port is forwarded. 
* The institutes login node ```login.bgc-jena.mpg.de''' prohibits port forwarding so that some copy and paste code from
  the internet will not work and not all the online information about local port forwarding is applicable.
  The examples will therefore require either a vpn connection or some
  tweaking of your ~/.ssh/config file .


# Examples 

The purpose of the examples is to show:
* what is necessarry to run and use dask clusters on several remote machines
* how to control which ports are being used and how to use this ability to implement a convention about who uses which ports
* how to automate and deduplicate these things
* what minimum of code is necessary in the notebooks to allow this way of remote control.

## Requirement to run the examples
* clone this repository on your local computer and matagorda. (The examples contain code that runs on the server(matagorda) and 
  also code that runs on your local machine, so it will be convenient not to have to copy it around. The examples will assume
  the code to be checked out in you home (`~/ports/`).
  
* Add the following to your `~/.ssh/config` with  YourInstituteLogin and  YourMatagordaLogin
  replaced by the correct values:
  ```sshconfig
  Host    login
	  HostName login.bgc-jena.mpg.de
          User YourInstituteLogin

  Host    matagorda-from-home
	  ProxyCommand ssh -q -W %h:%p login
	  HostName matagorda.bgc-jena.mpg.de
          User YourMatagordaLogin
  ```
  This will make it work even if you do not have a vpn connection to the institute (using login as jumphost).

## Order of the examples:
* [ex0](examples/ex0)
* [ex1](examples/ex1)
* [ex2](examples/ex2)
* [ex3](examples/ex3)
* [ex4](examples/ex4)
* [ex5](examples/ex5)

We start with a  manual unautomated example [ex0](examples/ex0), that 
demonstates the commands (on client and server) necessary to 
* open a tmux window
* activate the (conda) environment
* start an ipython session (or notebook)
* connect via ssh from a client machine over the network 
* redirect the web output of the dask dashboard (and jupyter server) to a port on the local machine
* start the browser on the local client with the correct port number.
We show the annoying aspects of it and use them to motivate gradual improvements leading to the next implementation.
The example code will be improved over several intermediate iterations (ex1 to ex4) that can later be discarded and are only there
to show the development of the final solution, which would be a bit hard to read ohterwise.
At the end we will have built some functions executable on the client that automate all the above steps.
But even this final code [ex5](#examples/ex5) is not intended to be used as a black box. 




% 
% # Motivational Example with notebooks: most general usage scenario:#
% Assume you have two or more different conda environments on matagorda and
% running at least one notebook for each.  This has the following consequences:
% Since the jupyter (notebook or lab) server is started in the same conda env
% that is used by the code in the notebooks you wll have to start two different
% jupyter servers on matagorda.  They will use two different ports jsp1, jsp2 on
% matagorda.  If the notebooks use a dask clients every client will use its own
% dashboard with its own port.  All clients may (and should) use the same
% scheduler or cluster.  
% 
%  We have the following summary of port consumption on one machine for one user:
%  ```n_envs + n_client + n_cluster```   where 
%  - `n_envs` is the number of conda environments with their respective jupyterservers
%  - `n_clients` is the number of clients (and equal to the number of notebooks that use dask)
% 
% To be able to connect to these servers with the browser on your local machine you will have to forward the two ports. 
  
