# The following numbers are userspecific (for mm), 
localPort=8081
my_scheduler_port=8900 
my_dashboard_port=8911
remote_commands="\
export my_scheduler_port=${my_scheduler_port};
export my_dashboard_address=localhost:${my_dashboard_port};
tmux new-session -d ;
tmux rename-window -t 0 'Main';
tmux send-keys -t 'Main' 'conda-shell' C-m
tmux send-keys -t 'Main' 'ipython' C-m
tmux attach-session -t  $SESSION:0"


ssh_command="ssh -L ${localPort}:localhost:${my_dashboard_port} matagorda-from-home -t '${remote_commands};'"

function client_ssh_command {
	echo $ssh_command
	eval "${ssh_command}"
};

function client_start_browser {
	firefox "localhost:${localPort}"
	# on mac open "http:localhost:${localPort}"
};
