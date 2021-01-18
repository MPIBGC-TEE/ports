
## 0. Example without any infrastructure.
This example runs one scheduler(cluster) and uses it in the same session.
Here we let the dask cluster find a port where it can serve the dashboard.
So we can not know the port number in advance. This has the unwelcome effect that we always have to
adapt the portforwarding command.

### steps
* open a terminal and open a shell on the remote machine:
  ```
  ssh matagorda-from-home
  ```
* start a tmux session on matagorda and change in this directory.  
  ```
  cd  ~/ports/examples/ex_0
  tmux
  ```
* activate the conda env
  ```
  conda activate bgc_md2
  ```
* start an ipython session
  ```
  ipython
  ```
* start a cluster and ask for the (dynamic) dashboard address
  ```ipython
  %load server_start_cluster.py
  ```
  (Hit enter twice...)
* open another terminal
  and forward a local port (we arbitrarily chose 8081)  on your machine to the dashboard port returned by  the previous command (e.g. 36167 but you have to **replace** this with the one chosen by `LocalCluster()` which will generally differ from session to session  )
  ```
  ssh -L 8081:localhost:36167 matagorda-from-home
  ```
* point your browser to `http://localhost:8081` and see the dashboard.

* create a client and run some code (watch the dashboard)
  ```ipython
  %load ~/ports/examplex/ex0/server_use_cluster_1.py
  ```
* Run some more code (watch the dashboard)
  ```ipython
  %load ~/ports/examplex/ex0/server_use_cluster_2.py
  ```

### Wishlist:
Wishlist:
* Automate
  * the `tmux` and `conda activate` commands.
* Assist in
  * the creation of the client ssh forwarding command for the dashboard server.
  * the translation of the url to the dashboard
* make the python code execuatable as a script with
```python server_start_cluster.py``` or
```ipython -i server_start_cluster.py```
