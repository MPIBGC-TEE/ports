# The following numbers are user specific (for mm), 
local_jupyter_port=8881 
remote_jupyter_port=8922

local_dashboard_port=8781
remote_dashboard_port=8911

remote_scheduler_port=8900 

function ssh-tmux-ipython {
	local remote_commands="\
	export my_scheduler_port=${remote_scheduler_port};
	export my_dashboard_address=localhost:${remote_dashboard_port};
	tmux new-session -d ;
	tmux rename-window -t 0 'Main';
	tmux send-keys -t 'Main' 'ipython' C-m
	tmux attach-session -t  $SESSION:0"
	
	
	local ssh_command="ssh -L ${local_dashboard_port}:localhost:${remote_dashboard_port} matagorda-from-home -t '${remote_commands};'"
	echo $ssh_command
	eval "${ssh_command}"
};

function ssh-tmux-jupyter-notebook {
	local remote_commands="\
	export my_scheduler_port=${remote_scheduler_port};
	export my_dashboard_address=localhost:${remote_dashboard_port};
	tmux new-session -d ;
	tmux rename-window -t 0 'jupyter-server';
	tmux send-keys -t 'jupyter-server' 'jupyter Space notebook Space --port=${remote_jupyter_port} Space --port-retries=0 Space --no-browser' C-m
	tmux attach-session -t  $SESSION:0"
	
	
	local ssh_command="ssh -L ${local_dashboard_port}:localhost:${remote_dashboard_port} -L ${local_jupyter_port}:localhost:${remote_jupyter_port} matagorda-from-home -t '${remote_commands};'"
	echo $ssh_command
	eval "${ssh_command}"
};

function browser_dashboard {
	firefox "localhost:${local_dashboard_port}"
	# on mac open "http:localhost:${local_dashboard_port}"
};

function browser_jupyter {
	firefox "localhost:${local_jupyter_port}"
	# on mac open "http:localhost:${local_dashboard_port}"
};
