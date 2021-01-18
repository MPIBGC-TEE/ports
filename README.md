
Table of Contents
=================

   * [Purpose](#purpose)
      * [1. Separation of concerns](#1-separation-of-concerns)
      * [2. Explicitness](#2-explicitness)
      * [3. Deduplication](#3-deduplication)
   * [Used tech](#used-tech)
      * [Ports](#ports)
      * [(DASK) clusters](#dask-clusters)
      * [Tmux](#tmux)
      * [SSH local port forwarding](#ssh-local-port-forwarding)
   * [Examples](#examples)
      * [Requirement to run the examples](#requirement-to-run-the-examples)
      * [Order](#order)

Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc)

# Purpose
The package contains examples to facilitate remote computing on matagorda and Antakya mainly concerned with the use of
[bgc_md2](https://github.com/MPIBGC-TEE/bgc_md2).
It serves as a gentle use-case-specific introduction to some of the tools (ssh,tmux,ipython,dask.distributed.LocalCluster).
Its **main purpose** however is to **isolate this site and user specific code here and keep it out of bgc_md2** (and our other packages).
In particular the purpose is threefold:
## 1. Separation of concerns
To actually run our [bgc_md2](https://github.com/MPIBGC-TEE/bgc_md2) notebooks we are concerned with three very different things,
of which only one really belongs to [bgc_md2](https://github.com/MPIBGC-TEE/bgc_md2) .
The other too threaten its long term integrity:
   1. code USING a dask cluster (99.9 percent of the notebook / script code
      This is the only code that definitely belongs to `bgc_md2` and the only one that
      is portable.
   1. code to ADMINISTER the dask cluster (SET UP/START/STOP/CONFIG)
      In many use cases this would even be handled by other people (the cluster admins).
      Ideally bgc_md2 code should run on **any** dask cluster and should not depend on its creation.
      In our case this is not entirely true, since some notebooks use timeouts for computations
      which excludes clusters with deamonized workers. So our notebooks have to have
      code that starts a dask cluster with the right properties.
      If it can not be avoided entirely, (dask)cluster administration specific code should be kept at a minimum,
      to keep the framework useable elsewhere
   1. code that is entirely specific to a group of users like the whole module
      https://github.com/MPIBGC-TEE/bgc_md2/blob/master/src/bgc_md2/sitespecificHelpers.py
      or the user specific parts of `prepare_cluster` in
      https://github.com/MPIBGC-TEE/bgc_md2/blob/master/src/bgc_md2/models/CARDAMOM/CARDAMOMlib.py
      This code had only intermediate purpose (to avoid spreading of a
      preliminary solution to all notebooks) and has lost its temporary
      justification by the new approach proposed here, which outsources these aspects and only requires
      a minimal and obvious bit of code in the notebooks.

## 2. Explicitness
To be self contained the notebooks have to have a minimum of code that does not belong to `bgc_md2`,
for instance code that starts a cluster if none is found already running.
This code should not be buried in a library, but visible in plain sight of future users of the notebooks so that it
can be easily replaced according to the needs of their computer/cluster.

## 3. Deduplication
This will be achieved by the advanced examples mainly by code that is well separated from the package and completely
under user control. Some duplication will remain, where it would conflict with a clear separation of `bgc_md2` or
reduce explicitness. For instance it is likely that many notebooks will share  a common first cell that
ensures the existence of a running dask cluster and connects to it. Although some of the code in these cells could be put into
a library function, this would most likely lead to a function returning the cluster connection thereby
1. burdening our libraries with code that does not really belong to bgc_md2 (separation of concerns)
1. obscuring the fact that any cluster would do (reducing explicitness)

The purpose is achieved by some small helper functions that translate the jupyter provided urls and generate and run ssh forwarding commands for the users. This is completely optional and does not necessitate any additional agreement between the users but keeps this kind of code out of our main packages (bgc_md2,CompartmentalSystems) and visible if it is used.
The main usage example is [ex0_c](examples/ex0_c).

# Involved technology and tools
## Ports
Server applications provide their services to ports.  
Examples are jupyter notebook servers, dask dashboards but also normal web servers (port80) and secure shells(22).
The 2^16 ports are a system resource shared by all users and applications.
There are some guidelines about who should listen where
https://en.wikipedia.org/wiki/Port_(computer_networking).
By default the two server application we need use use either a fixed default port  (8888 for the jupyter notebook
server and 8787 for the dask dashboard server) or (in case somebody has already started one of them on the same
machine )an unpredictable dynamic port from the dynamic range.
This semi predictable situation makes a completely manual solution very painful but a complete automation very complex.
The code in this package goes for a solution that necessitates and allows user interaction, but makes it a lot less painful.

Its main advantage is that no policies or contracts between users are necessary. Even the package itself does not have to be used by all the matagorda, Antakya users. If you use it in a notebook (usually 2 lines of code ) I would even recommend to turn it into a comment afterwards.  

## (DASK) clusters
To keep our bgc_md2 notebooks scalable to supercomputers (with many network connected nodes **without shared memory**) we always use **distributed** schedulers.
Even though Antakya and matagorda are just multisocket multicore machines that theoretically could share their memory between their cores, a real cluster has the workers running on different machines. To simulate the situation on a real cluster we use `dask.distributed.LocalCluster` instances.
The same dask cluster can be used by many clients (in many notebooks) simultaneously, so how many dask clusters should we run?
There are some possibilities.
* One,
    This would be the optimal solution for a high performance computing scenario where a
    single dask cluster per (machine or hardware cluster) is shared by all users and all clients, since a single
    cluster can handle any number of clients and can share the available resources
    between them.
    A single cluster shared by all users would however again
    necessitate some maintainance and precautions. In case of a failure it affects
    all users and makes it difficult to switch off without fear of interrupting someone else's work.
* As many as we have (active) notebooks..,
    This happenes automatically if the notebooks just start a cluster without checking if one is already running.
    If we run many clusters we will have to make sure that they do not assume the complete resources of the machine, especially
    memory wise.
    There is no mechanism built into dask that prevents you from starting 1000 clusters, every single one assuming that the whole machine belongs to it. This will not cause problems as long as all the  computations together do not **use up** the resources of the workers but if they do you can provoke the underlying operating system (in this case the linux kernel) **to kill them**. This way you can indirectly **cause somebody else's running scripts/notebooks to fail** (e.g by exceeding the memory limits of the machine, even if you don't do it alone but other users *"helped"* to overload the machine.  

* Reused clusters (one/two per user)?
    This is a compromise to gain flexibility at
    the cost of perfect resource distribution as long as the number of users is
    very small. In practice it turns out that this setup is not much safer against
    oversubscribing (memory wise) but can be useful for running tests quickly.
    (If a notebook connects to an existing dask cluster one does not have to tear down and setup the complete set of workers all the time.
    which can take more time than a small piece of actual code)
    This makes testing dask code nearly as fast as normal python code. Therefore some of the examples (1-4) use this technique.
    The disadvantage is that, especially for some of our notebooks that require a cluster started with certain arguments (Holgers CARDAMOM notebooks)
    it is essecntial to provide the code to start such a cluster in the notebook. (Otherwise it would require the user to **know** that the notebook requires a **special** cluster while  the code to start it would be hidden)

## Tmux
To achieve robustness and general independence from network connections to the server we use a **t**erminal **mu**ltiple**x** er for all text based output on the server [tmux](https://github.com/tmux/tmux/wiki). From the perspective of the server the tmux server looks like a local console window running on the server, to which it can send its output regardless of any network connection.
The network connection is only necessary when we connect to the tmux server from the terminal on a different machine.
Two tmux commands that you will find using a lot in our scenario are `tmux ls` (list sessions) and `tmux attach -t ${NameOfYourSession}`. You can give names to sessions and even windows (examples) which makes finding the right session
after a disconnect much easier. You can even automate tmux sessions by the `send_keys` subcommand. (examples)


## SSH local port forwarding
* Since we use 'local ssh port forwarding' the start messages from a jupyter server about where to point the browser
  are most likely wrong, because they refer to the  port on the remote server. The server has no information to
  which local port is forwarded.
* The institutes login node `login.bgc-jena.mpg.de` prohibits port forwarding so that some copy and paste code from
  the internet will not work and not all the online information about local port forwarding is applicable.
  The examples will therefore require either a vpn connection or some
  tweaking of your ~/.ssh/config file.
* sometimes forwarding of ports has to be canceled to free them for new use (especially if you have used the `-f` flag),
  which can be undone by adding  the `-O cancel` to the command that created the tunnel:
  E.g. the forwarding created by:
  `ssh -L 8080:localhost:8911 matagorda-from-home` can be undone by
  `ssh -O cancel -L 8080:localhost:8911 matagorda-from-home`
  (Just stopping (Ctrl C) or killing ssh processes also works but has potentially unintended victims)     

## Jupyter notebooks
  * Passwords: You can use [jupyter password authentication](https://jupyter-notebook.readthedocs.io/en/stable/public_server.html#adding-hashed-password-to-your-notebook-configuration-file), which might be helpful for the following reasons.
    * your browser can remember the passwords
    * Due to the different ports on the client the normal links (containing the adress and token) printed out in
      the server  terminal  by the `jupyter notebook`  command do not work .
    * You might want to reconnect to a long running notebook, and would have to scroll back to the initially printed tokens.

## ipython
  * For long computations with uncertain success it is usefull to use the `ipython` interpreter.


# Examples

## Requirements to run the examples
* clone this repository on your local computer, matagorda and antakya
  (The examples contain code that runs on the servers (matagorda and antakya) and
  also code that runs on your local machine, so it will be convenient not to have to copy it around. The examples will assume
  the code to be checked out in  (`~/ports/`) and installed  both on the client (your computer) and on the server (there preferably into the `bgc_md2` environment). To install run `python setup.py develop` in `~/ports/`.
  `bgc_md2` does *intentionally* not depend on this package.
  However a small part of its functionality is useful in notebooks to make your live a bit easier.
  (We could easily leave the two lines as comments in all our notebooks).
  If you want to use the example shell scripts you source them from your `~/.bashrc`

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

  Host    antakya-from-home
	  ProxyCommand ssh -q -W %h:%p login
	  HostName antakya.bgc-jena.mpg.de
          User YourMatagordaLogin
  ```
  This will make it work even if you do not have a vpn connection to the institute (using login as jumphost).
  It will also work insinde the institute or the vpn. (although you don't need `login` )

* It is assumed that you have created a conda environment `bgc_md2` that contains
    `ipython`, `jupyter` `numpy` and `dask`.


## Order
* [ex0](examples/ex0)
* [ex0_b](examples/ex0_b)
* [ex0_c](examples/ex0_c)


We start with the manual unautomated examples [ex0](examples/ex0) (for ipython) and [ex0_b](examples/ex0_b) (for a notebook) that
demonstate the commands (on client and server) necessary to
* connect via ssh from a client machine over the network
* open a tmux session on the server.
* activate the (conda) environment
* start an ipython session (or jupyter notebook)
* find out about the ports that the jupyter server and dask.sheduler chose to serve the notebooks and dashboards.
* redirect the web output of the dask dashboard (and jupyter server) to a port on the local machine
* start the browser on the local client with the correct port number.

The annoying aspects of this manual approach will be apparent in [ex0](examples/ex0) and [ex0_b](examples/ex0_b) and motivate the little tools shown in  [ex0_c](examples/ex0_c). The automation does not depend on any agreement between users and scales easily to many notebooks/sessions running on both machines by many users.

## static examples (not recommended for use but instructive)

The examples [ex1](examples/ex1), [ex2](examples/ex2),[ex3](examples/ex3).[ex4](examples/ex4)
show how to automate the original strategy that depends on a fixed devision of ports between the users and remote controlling jupyter, scheduler and dashboard ports via environment variables.
This is possible if the number of notebooks, clusters and dashboards is small but for several notebooks running their own clusters the solution becomes quickly more complicated than the problem.
Especially if a user starts different notebooks using different clusters from ONE jupyter server we can not control the port choice remotely via environment variables, since all the notebooks will share the environment the server has been started in.
So unfortunately the solution does not scale.
