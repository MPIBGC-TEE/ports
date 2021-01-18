from IPython.core.display import display, HTML
from subprocess import run

def print_commands(cluster, local_port=8880):
    # this function relies on the appropriate entries in the ./ssh-config of the client
    # matagorda-from-home
    # antakya-from-home
    hostname=str(run(['hostname'],capture_output=True).stdout,'utf8').strip().lower()
    remote_ssh_host = f'{hostname}-from-home'
    remote_port = (cluster.dashboard_link.split('/')[2]).split(':')[1]
    ssh_command_from_home = f'ssh -L {local_port}:localhost:{remote_port} {remote_ssh_host}'
    print("ssh command: "+ssh_command_from_home)

    url = f'http://localhost:{local_port}'
    print(f"""forwarded dashboard: {url}""")
    display(HTML(f"""forwarded dashboard: <a href={url}>{url}</a>"""))
