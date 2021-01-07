browser="firefox" # on mac possibly "open" 


local_antakya_jupyter_port_1=8880
local_antakya_dashboard_port_1=8780
local_antakya_jupyter_port_2=8881
local_antakya_dashboard_port_2=8781


local_matagorda_jupyter_port_1=8890
local_matagorda_dashboard_port_1=8790
local_matagorda_jupyter_port_2=8891
local_matagorda_dashboard_port_2=8791

remote_jupyter_port_1=8921
remote_jupyter_port_2=8922

remote_dashboard_port_1=8911
remote_dashboard_port_2=8912

remote_scheduler_port_1=8901
remote_scheduler_port_2=8902

function ssh_ipython {
	local remote_ssh_hostname=$1;
	local local_dashboard_port_1=$2;
	local local_dashboard_port_2=$3;
	local remote_commands="\
	export my_scheduler_port_1=${remote_scheduler_port_1};
	export my_scheduler_port_2=${remote_scheduler_port_2};
	export my_dashboard_address_1=localhost:${remote_dashboard_port_1};
	export my_dashboard_address_2=localhost:${remote_dashboard_port_2};
	tmux new-session -d ;
	tmux rename-window -t 0 'Main';
	tmux send-keys 'conda Space activate Space bgc_md2' C-m;
	tmux send-keys -t 'Main' 'ipython' C-m;
	tmux attach-session -t  $SESSION:0"


	local ssh_command="ssh \
		-L ${local_dashboard_port_1}:localhost:${remote_dashboard_port_1} \
		-L ${local_dashboard_port_2}:localhost:${remote_dashboard_port_2} \
		${remote_ssh_hostname} -t '${remote_commands};'"
	echo ${ssh_command}
};

# forward jupyter and dashboard ports
# the argument is the ssh name according to your .ssh/entrie
function ssh_jupyter {
	local remote_ssh_hostname=$1;
	local local_jupyter_port=$2;
	local remote_jupyter_port=$3;
	local local_dashboard_port_1=$4;
	local local_dashboard_port_2=$5;
	
	local remote_commands="\
	export my_scheduler_port_1=${remote_scheduler_port_1};
	export my_scheduler_port_2=${remote_scheduler_port_2};
	export my_dashboard_address_1=localhost:${remote_dashboard_port_1};
	export my_dashboard_address_2=localhost:${remote_dashboard_port_2};
	tmux new-session -d ;
	tmux rename-window -t 0 'jupyter-server';
	tmux send-keys 'conda Space activate Space bgc_md2' C-m;
	tmux send-keys -t 'jupyter-server' 'jupyter Space notebook Space --port=${remote_jupyter_port} Space --port-retries=0 Space --no-browser' C-m;
	tmux attach-session -t  $SESSION:0"
	
	local ssh_command="ssh \
		-L ${local_jupyter_port}:localhost:${remote_jupyter_port} \
		-L ${local_dashboard_port_1}:localhost:${remote_dashboard_port_1} \
		-L ${local_dashboard_port_2}:localhost:${remote_dashboard_port_2} \
		${remote_ssh_hostname} -t '${remote_commands};'"
	echo ${ssh_command}
}

function browse_port {
	local port=$1
	${browser} "localhost:${port}" &
}


#####################################################
#####################################################
# from here on we use the general functions 
# in functions that serve as abbreviatiated commands
#####################################################

#####################################################
# antakya
function antakya_ipython {
	local command=$(ssh_ipython \
		"antakya-from-home" \
		${local_antakya_dashboard_port_1} \
		${local_antakya_dashboard_port_2} \
	)
	echo ${command}
	eval "${command}"

}

function antakya_notebook_1 {
	ssh_command=$(ssh_jupyter \
		"antakya-from-home" \
		${local_antakya_jupyter_port_1} \
		${remote_jupyter_port_1} \
		${local_antakya_dashboard_port_1} \
		${local_antakya_dashboard_port_2}\
	)
	echo $ssh_command
	eval "${ssh_command}"
	#eval "${ssh_command} &" 
	#browser_antakya_jupyter_1 &
	#fg
}	

function antakya_notebook_2 {
	ssh_command=$(ssh_jupyter "antakya-from-home" \
		${local_antakya_jupyter_port_2} \
		${remote_jupyter_port_2} \
		${local_antakya_dashboard_port_1} \
		${local_antakya_dashboard_port_2}\
	)
	echo $ssh_command
	eval "${ssh_command}"
}
#
#
#####################################################
# matagorda
function matagorda_ipython_1 {
	local command=$(ssh_ipython \
		"matagorda-from-home" \
		${local_matagorda_dashboard_port_1}
		${local_matagorda_dashboard_port_2}
	)
	echo ${command}
	eval "${command}"

}

function matagorda_notebook_1 {
	ssh_command=$(ssh_jupyter \
		"matagorda-from-home" \
		${local_matagorda_jupyter_port_1} \
		${remote_jupyter_port_1} \
		${local_matagorda_dashboard_port_1} \
		${local_matagorda_dashboard_port_2}\
	)
	echo $ssh_command
	eval "${ssh_command}"
}

function matagorda_notebook_2 {
	ssh_command=$(ssh_jupyter "matagorda-from-home" \
		${local_matagorda_jupyter_port_2} \
		${remote_jupyter_port_2} \
		${local_matagorda_dashboard_port_1} \
		${local_matagorda_dashboard_port_2} \
	)
	echo $ssh_command
	eval "${ssh_command}"
}


######################################################
# local
function browse_matagorda_dashboard_1 {
	browse_port ${local_matagorda_dashboard_port_1}
}

function browse_matagorda_dashboard_2 {
	browse_port ${local_matagorda_dashboard_port_2}
}

function browse_matagorda_jupyter_1 {
	browse_port ${local_matagorda_jupyter_port_1}
}

function browse_matagorda_jupyter_2 {
	browse_port ${local_matagorda_jupyter_port_2}
}

function browse_antakya_dashboard_1 {
	browse_port ${local_antakya_dashboard_port_1}
}

function browse_antakya_dashboard_2 {
	browse_port ${local_antakya_dashboard_port_2}
};

function browse_antakya_jupyter_1 {
	browse_port ${local_antakya_jupyter_port_1}
};

function browse_antakya_jupyter_2 {
	browse_port ${local_antakya_jupyter_port_2}
};
