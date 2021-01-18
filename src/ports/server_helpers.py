from IPython.core.display import display, HTML
from subprocess import run

def print_commands(cluster, local_port=8880):
    hostname=str(run(['hostname'],capture_output=True).stdout,'utf8').strip()
    remote_host = hostname
    remote_port = (cluster.dashboard_link.split('/')[2]).split(':')[1]
    ssh_command = f'ssh -L {local_port}:localhost:{remote_port} {remote_host}' 
    ssh_command_from_home = f'ssh -L {local_port}:localhost:{remote_port} {remote_host}_from_home'
    print("ssh command from institute: "+ssh_command)
    print("ssh command from home: "+ssh_command_from_home)
    
    url = f'http://localhost:{local_port}'
    print(f"""forwarded dashboard: {url}""")
    display(HTML(f"""forwarded dashboard: <a href={url}>{url}</a>"""))
