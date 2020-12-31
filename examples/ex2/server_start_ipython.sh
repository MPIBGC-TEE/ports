# don't execute but source this script with: source server_start_ipython.sh
# the next four lines would only be necessary if the 
# my_scheduler_port=8900 
# my_dashboard_port=8911
# export my_scheduler_port=${my_scheduler_port};
# export my_dashboard_address=localhost:${my_dashboard_port}
conda activate bgc_md2
ipython 
