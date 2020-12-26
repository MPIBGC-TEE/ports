session="ipython"
tmux new-session -d -s $session
tmux rename-window -t 0 "Main"
tmux send-keys -t "Main" 'conda activate bgc_md2' C-m
#tmux send-keys -t "Main" 'export my_cluster_address=localhost:8900' C-m
#tmux send-keys -t "Main" 'export my_dashboard_port=localhost:8911' C-m
