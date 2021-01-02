
## 0b. Notebook example without any infrastructure.
Instead of ex0 we run a jupyter notebook server which will also choose an arbitrary port if the default is not available.
So we have two unpredictable portnumbers and have two manual ssh port commands to adjust

* open a terminal and open a shell on the remote machine:
  ```ssh matagorda-from-home```
* start a tmux session on matagorda  
  ``` tmux ```
* activate the conda env
  `conda activate bgc_md2`
* start a jupyter notebook/lab server 
  ```jupyter notebook --no-browser```
* open another (local) terminal 
  and forward a local port (we arbitrarily chose 8080)  on your machine to the 
  notebook server port number returned by  the previous command (e.g. 34234 but this will be
  chosen by 'jupyter notebook' and will likely differ between sessions. **replace 34234 with the actual number contained in th by jupyter output in the tmux window**)  
  ```
  ssh -L 8080:localhost:34234 matagorda-from-home
  ```

* point your browser to `http://localhost:8080` to see the notebook.

* In the notebook start a cluster and ask for the (dynamic) dashboard address
  ```ipython
  %laod server_start_cluster.py
  ```
  (Hit enter twice...)
* In your local terminal forward a local port (we arbitrarily chose 8081)  on your machine to the dashboard port returned by  the previous command (here 36167 but this will be chosen by `LocalCluster()` and can also differ 
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

  Wishlist:
  * Set the two port numbers beforehand ato avoid the maunual interaktion.
