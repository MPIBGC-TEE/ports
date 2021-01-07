This is a full flegded example running two notebooks with a dask dashboard each on each server matagorda  
For every server four ports have to be forwarded which results in eight local ports
being used by different browser windows.
If you open a local jupyter servers with their own dask dashbaoards this number increases to 12!
The functions have again be renamed and generalized to make them shorter
Have a look and try them out:

```bash
cd ~/ports/examples/ex5
source client_commands.sh
matagorda_notebook_1

```


in another shell
```bash
cd ~/ports/examples/ex4
source client_commands.sh
browse_matagorda_jupyter_1
```
With jupyter (in the browser) open `~/ports/examples/ex4/server_start_cluster_on_port.py`

in a new cell
```ipython
%load server_use_cluster_1.py
```

(you can load `server_use_cluster_2.py` into another or the same notebook)

You can also use a `ssh-tmux-ipython` in another client shell (after sourcing
`client_shell_commands.sh`)
