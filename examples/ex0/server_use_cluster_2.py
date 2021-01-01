
sn=200
n=400
def f(arr):
    for i in range(40): # keep busy
        res = np.matmul(arr, arr)
    return res

args = [i*np.eye(n) for i in range(sn)]


def computation2():
    ts = time.time()
    big_future = client.scatter(args)
    futures = client.map(f, big_future)
    results = [fut.result() for fut in futures]
    results
    print(time.time()-ts)


computation2()
