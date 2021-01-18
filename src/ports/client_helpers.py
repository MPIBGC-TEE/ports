from subprocess import check_call, run, Popen, PIPE, check_output
import multiprocessing as mp

def f(q):
    rec=run(['nc', '-l', '2400'],capture_output = True)
    #print('f','rec',type(rec),int(rec.stdout))
    q.put(rec.stdout)



def remote_result(remote_command, ssh_host_name):
    q = mp.Queue()
    p = mp.Process(target=f, args=(q,))
    p.start()

    #remote_command = "echo '8888 8911 8912'| nc -q1 localhost 2300"
    send_command = remote_command + "| nc -q1 localhost 2300"
    check_call(
        [ 'ssh','-R', ' 2300:localhost:2400', ssh_host_name, send_command ]
    )
    res =str(q.get(), 'utf8')
    p.join()
    return res


def list_notebook_servers(ssh_host_name):
    output = check_output(f"ssh -G {ssh_host_name} | grep '^user '", shell=True)
    remote_login = str(output.strip(), 'utf8').split(' ')[1]
    #
    # find the pids of jupyter notebook instances of this user
    s_n = remote_result(
        f"ps -u {remote_login}" + "|awk '/jupyter-note/{print $1}'",
        ssh_host_name
    )
    pids_n = [int(bs) for bs in s_n.split()]
    #
    # find the pids of jupyter lab instances of this user
    s_l = remote_result(
        f"ps -u {remote_login}" + "|awk '/jupyter-lab/{print $1}'",
        ssh_host_name
    )
    pids_l = [int(bs) for bs in s_l.split()]

    pids = pids_n + pids_l
    print(ssh_host_name, pids)

    port_numbers = [] if len(pids) == 0 else [
        int(
            remote_result(
                f"netstat -tulpen|grep {pid}"+"|awk '/127.0.0.1/{print $4}'",
                ssh_host_name
            ).strip().split(':')[1]
        )
        for pid in pids
    ]
    return port_numbers


def jupyter_forwarding(localBasePort=8889):
    # The choice localPors 8889 is not necessary but not far fetched since a
    # localy started jupyter will serve to 8888 by default.  So we count from
    # there.
    #
    ssh_host_names = ['matagorda-from-home', 'antakya-from-home']
    port_dict = {
        host: list_notebook_servers(host) 
        for host in ssh_host_names
    }
    #
    # filter out the host: ports combies where ports is not empth
    combies = [
        (host, port)
        for host in ssh_host_names if len(port_dict[host]) > 0 
        for port in port_dict[host]
    ]
    print(combies)

    localPorts= [
        localBasePort+offset
        for offset,_ in enumerate(combies)
    ]

    
    command_tuples = [
        (
            'ssh',
            '-L',
            f'{localPorts[offset]}:localhost:{combi[1]}',
            combi[0],
            '-N'
        )
        for offset, combi in enumerate(combies)
    ]
    commands = [' '.join(tup) for tup in command_tuples]
    print('#####################################')
    print('The following commands are active as long as this script runs:')
    print('\n'.join(commands))

    urls  = [f'localhost:{lp}' for lp in localPorts]
    print('#####################################')
    print('Point your browser to:')
    print('\n'.join(urls))
    def g_maker(command_tuple):
        def g():
            run(command_tuple)
        return g
    processes = [mp.Process(target=g_maker(command_tuple)) for command_tuple in command_tuples]

    for p in processes:
        p.start()

    for p in processes:
        p.join()


