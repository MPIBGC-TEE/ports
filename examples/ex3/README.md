Like the previous example runs one scheduler(cluster) and uses it in different to run the  
scripts (or %load them into ipython).  
The python code did not change at all (symlinks)

The portnumbers `my_scheduler_port` and `my_dashboard_port`
are still set by the client_ssh_command as environment variables on the remote
machine.
But this time also starts a tmux session, activates the conda environment and starts the ipython interpreter.
The commands in `server_start_ipython.sh` are no longer necessary.

The little scripts `client_ssh_command.sh` and `client_start_browser.sh` are now functions in client_commands.sh


To start 3 different ipython sessions on matagorda do the following:
* On your local computer open 3 terminals

* in every one of the three execute
  ```bash
  cd ports/examples/ex3
  source client_commands.sh
  client_ssh_command
  ```
  This forwards the dashboard port to your local machine and opens an ipython
  interpreter in a tmux session on matagorda (a different one in every
  terminal)

* in one of the three

  ```ipython
  %cd ~/ports/examples/ex3
  %load server_start_cluster_on_port.py
  ```
  This will start the cluster and makes it server the dashboard

* Open another (fourth) terminal
  ```bash
  source client_commands.sh
  client_start_browser
  ```
  This will start the browser listening on the local port the dashboard has been forwarded to.  

* you can use the cluster in the other two terminals as usual.
  ```ipython
  %cd ~/ports/examples/ex3
  %load server_use_cluster_1.py
```

  ### Wishlist
  * We also want to use jupyter (notebook or lab) which will need another port specification on both
  the local and the remote machine as well as another browser command.
