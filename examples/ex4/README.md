Like the previous example but with renamed and additional functions in `client_shell_commands.sh`
Have a look and try them out:
```bash
cd ~/ports/examples/ex4
source client_shell_commands.sh
ssh-tmux-jupyter-notebook
```

in another shell
```bash
cd ~/ports/examples/ex4
source client_shell_commands.sh
browser_jupyter
```
With jupyter (in the browser) open `~/ports/examples/ex4/server_start_cluster_on_port.py`

in a new cell
```ipython
%load server_use_cluster_1.py
```

(you can load `server_use_cluster_2.py` into another or the same notebook)

You can also use a `ssh-tmux-ipython` in another client shell (after sourcing
`client_shell_commands.sh`)
