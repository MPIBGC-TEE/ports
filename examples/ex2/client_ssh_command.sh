# The following numbers are userspecific (for mm), 
localPort=8081
my_scheduler_port=8900 
my_dashboard_port=8911
remote_commands="\
export my_scheduler_port=${my_scheduler_port};
export my_dashboard_address=localhost:${my_dashboard_port}; 
exec bash -l"

ssh_command="ssh -L ${localPort}:localhost:${my_dashboard_port} matagorda-from-home -t '${remote_commands}'"
echo $ssh_command
eval "${ssh_command}"



