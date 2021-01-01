This example runs one scheduler(cluster) and uses it in the same session. 
Here we let the dask cluster find a port where it can serve the dashboard.

## 0. Example without any infrastructure.
* open a terminal and open a shell on the remote machine:
  ```ssh matagorda-from-home```
* start a tmux session on matagorda  
  ``` tmux ```
* activate the conda env
  `conda activate bgc_md2`
* start an ipython session
  ```ipython```
* start a cluster and ask for the (dynamic) dashboard address
  ```python
  %laod server_start_cluster.py
  ```
  (Hit enter twice...)
* open another terminal
  and forward a local port (we arbitrarily chose 8080)  on your machine to the dashboard port returned by  the previous command (here 36167 but this will be chosen by ``` LocalCluster()''' and can possibly be different from session to session  )
  ```
  ssh -L 8080:localhost:36167 matagorda-from-home
  ```
* point your browser to `http://localhost:8080` and see the dashboard.

* create a client and run some code (watch the dashboard)
  ```ipython
  %load ~/ports/examplex/ex0/server_use_cluster_1.py
  ```
* Run some more code (watch the dashboard)
  ```ipython
  %load ~/ports/examplex/ex0/server_use_cluster_2.py
  ```
