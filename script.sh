#!/run/current-system/sw/bin/bash
session=$1
tmux new-session -d -s $session
tmux rename-window -t 0 "Main"
tmux send-keys -t 'Main' 'conda-shell' C-m
tmux send-keys -t 'Main' 'conda activate bgc_md2' C-m
tmux send-keys -t 'Main' 'export my_scheduler_port=8900' C-m
tmux send-keys -t 'Main' 'export my_dashboard_address=localhost:8911' C-m
tmux send-keys -t 'Main' 'ipython' C-m
tmux attach-session -t  $SESSION:0
