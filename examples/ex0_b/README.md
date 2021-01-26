
## 0b. Notebook example without any infrastructure.
Instead of ex0 we run a jupyter notebook server which will also choose an arbitrary port if the default is not available.
So we have two unpredictable port-numbers and have two manual ssh port commands to adjust

* open a terminal and open a shell on the remote machine:
  ```ssh matagorda-from-home```
* start a tmux session on matagorda  
  ``` tmux ```
* activate the conda env
  `conda activate bgc_md2`
* start a jupyter notebook/lab server
  ```jupyter notebook --no-browser```
* open another (local) terminal
  and forward a local port (we arbitrarily chose 8889)  on your machine to the
  notebook server port number returned by  the previous command (e.g. 34234 but this will be
  chosen by 'jupyter notebook' and will likely differ between sessions and also depends on the existence of other jupyter servers on the same machine (The first instance will choose 8888 but the second instance will already choose a random port). **replace 34234 with the actual number contained in th by jupyter output in the tmux window**)  
  ```
  ssh -L 8889:localhost:34234 matagorda-from-home
  ```

* point your browser to `http://localhost:8889` to see the notebook.

* In the notebook start a cluster and ask for the (dynamic) dashboard address
  ```ipython
  %laod server_start_cluster.py
  ```
  (Hit enter twice...)
* In your local terminal forward a local port (we arbitrarily chose 8789)  on your machine to the dashboard port returned by  the previous command (here 36167 but this will be chosen by `LocalCluster()` and can also differ
  ```
  ssh -L 8789:localhost:36167 matagorda-from-home
  ```
* point your browser to `http://localhost:8789` and see the dashboard.

* create a client and run some code (watch the dashboard)
  ```ipython
  %load ~/ports/examples/ex0/server_use_cluster_1.py
  ```
* Run some more code (watch the dashboard)
  ```ipython
  %load ~/ports/examples/ex0/server_use_cluster_2.py
  ```

  Wishlist:
  * Automate
    * the `tmux` and `conda activate` and `jupyter` commands.
    * the investigation of the jupyter port on the server,
    * the creation of the ssh forwarding command.
    * the running (and postrun cleanup) of the ssh command on the client.
  * Assist in
    * the creation of the client ssh forwarding command for the dashboard server.
    * the translation of the url to the dashboard
