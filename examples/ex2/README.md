This example runs one scheduler(cluster) and uses it in different sessions or scripts.
The portnumbers ```my_scheduler_port''' and ```my_dashboard_port''' are set by theclient_ssh_command as environment variables on the remote machine. 
The python code on the remote machine
looks for them using ```os.environ''' and starts the cluster accordingly.
This code will fail if the environment variables are not set.

Wishlist for refinement to be addressed by later examples:
1. If we put the code into the notebooks users have to see that they have to set 
   the environment variables. It would be polite to allow the cluster to be started if no variable had been set. 
1. It is a bit tiresome to have to call the ssh command and then in the remote shell have to activate the conda environment and  startthe ipython session. Since the ssh command already executes code why not go the whole way and start the ipython shell in the activated environment. 
1. Since we might lose connection we could actually go on step further and start a tmux session remotely, activate the environment and start an ipython instance...
1. The local port is still duplicated between the browser start and the local port forward ssh command.  
