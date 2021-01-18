set -u # makes bash stop at undefined variables and helps you to stay sane in the face of typos
function tmux_named_session_command {
	local key_strokes="${1}"
	local session_name="${2}"
	local comm="tmux new-session -s ${session_name} -d;
	tmux send-keys -t ${session_name} ${key_strokes};
	tmux attach -t ${session_name};"
	echo "${comm}"
}
function tmux_unnamed_session_command {
	local key_strokes="${1}"
	local comm="tmux new-session  -d;
	tmux send-keys  ${key_strokes};
	tmux attach ;"
	echo "${comm}"
}
function ssh_maker {
	local ssh_host_name="${1}"
	local tmux_comm="${2}"
	local command="ssh -t ${ssh_host_name} \"${tmux_comm}\"" 
	echo "${command}"
}

function make_remote_tmux_command {
	local ssh_host_name="${1}"
	local key_strokes="${2}"
	if [ $# -eq 3 ]
	then
		local session_name="${3}"
		local tmux_comm="$(tmux_named_session_command "'pwd' 'C-m' ${key_strokes}" "${session_name}")" 
		echo "$(ssh_maker ${ssh_host_name} "${tmux_comm}")"
	elif [ $# -eq 2 ]
	then
		local tmux_comm="$(tmux_unnamed_session_command "'pwd' 'C-m' ${key_strokes}")" 
		echo "$(ssh_maker ${ssh_host_name} "${tmux_comm}")"
	else
		echo 'You must provide 2 or 3 arguments'
		exit 1
	fi
}	

function tmux_matagorda_bgc_md2 {
	if [ $# -eq 1 ]
	then
		eval "$(make_remote_tmux_command "matagorda-from-home" "'conda activate bgc_md2' 'C-m'" "${1}")"
	
	elif [ $# -eq 0 ]
	then
		eval "$(make_remote_tmux_command "matagorda-from-home" "'conda activate bgc_md2' 'C-m'" )"
	else
		echo "only 0 or 1 elements allowed"
		exit 1
	fi
}
# after you sourced this file you can call the functions like this
#tmux_matagorda_bgc_md2            
#tmux_matagorda_bgc_md2 'test'
