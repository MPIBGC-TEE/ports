## 0c. Notebook example with a bit of supporting infrastructure
Instead of ex0_b we run two jupyter notebook servers on each machine which will choose at least
one arbitrary port number since the default is not available twice.
You can even do this on antakya and matagorda
So we have up to four unpredictable port-numbers and  ssh port commands to adjust
This time this will be done by a small command line tool that is the main content of this
python package (which has to be installed)

* open a terminal and open a shell on the remote machine:
  `ssh matagorda-from-home`
* start a tmux session on matagorda
  `tmux `
* activate the conda env
  `conda activate bgc_md2`
* start a jupyter notebook/lab server
  `jupyter notebook --no-browser`

* repeat the previous steps (start another jupyter-notebook server (possibly in another environment))
  and then repeat again on antakya so that you have at least 4 sessions running...
  
* open another (local) terminal and
  activate the conda environment in which you installed the `ports` package.
  For simplicity lets assume you  put it in  `bgc_md2` (on your local machine)
  ```bash
  conda activate bgc_md2
  jupyter_forwarding
  ```
  This command will
  * find your running `jupyter-notebook` and `jupyter-lab`servers on matagorda and Antakya,
  * determine the port they are serving to,
  * create the ssh commands for the tunnels to your local ports
  * start those commands in separate processes that will run as long
    as you don not  stop the script with `Ctrl-C`
  * print out the urls under which you can reach them.

  The only thing you have to do is to copy and paste the printed addresses into your browser.

* paste the adresses into your browser's address line.


* Start the notebook  
  ```
  '~/ports/examples/ex0_c/start_and_use_cluster.py'
  ```
* change the local port in the second cell if you have to
* execute the code (also the first cell otherwise you will get an error)
  This will print out an ssh command to forward to a local port
  and a link.

* execute the suggested ssh command in a new shell on your client.
* click the link
* execute the last cell of the link


**NOTE** :
```python
try:
    from ports.server_helpers import print_commands
    print_commands(cluster,local_port=8880)

except ImportError as e:
    pass  # even it the module doesn't exist, dont make a fuss
```
Is what could go into our `bgc_md2` notebooks and preferably live in a separate
cell at the top.  ( It avoids a dependency on the `ports` package but allows us to use it for our convenience )
This piece of code works also in python scripts or ipython sessions.







Wishlist?:
  * Automate the `tmux` and `conda activate` and `jupyter` commands.
  How this can be done (in a generalizable way) is shown in this [script](send_keys_quoted.sh), but since it
  is a thing of personal preference it is only provided as a blueprint.
