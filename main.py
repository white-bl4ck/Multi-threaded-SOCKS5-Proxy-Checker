import argparse
import concurrent.futures
import requests
import time

def check_proxy(proxy, timeout):
    proxy_url = "http://{}:{}@{}:{}".format(proxy['username'], proxy['password'], proxy['host'], proxy['port'])
    proxies = {"http": proxy_url, "https": proxy_url}

    try:
        start = time.time()
        r = requests.get("http://httpbin.org/get", proxies=proxies, timeout=timeout)
        if r.status_code == 200:
            end = time.time()
            return (proxy, end - start)
        else:
            return None
    except:
        return None

def main(args):
    timeout = args.timeout
    num_threads = args.threads
    proxy_list = []
    with open(args.list, 'r') as f:
        for line in f:
            parts = line.strip().split(":")
            if len(parts) == 2:
                host, port = parts
                proxy_list.append({"host": host, "port": port, "username": None, "password": None})
            elif len(parts) == 4:
                username, password, host, port = parts
                proxy_list.append({"host": host, "port": port, "username": username, "password": password})

    available_proxies = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(check_proxy, proxy, timeout) for proxy in proxy_list]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                available_proxies.append(result)

    with open("out.txt", "a") as f:
        for proxy in available_proxies:
            f.write("{}:{} ({:.2f}s response time)\n".format(proxy[0]["host"], proxy[0]["port"], proxy[1]))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--list", type=str, required=True, help="File containing the list of proxies to check")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Number of threads to use for checking proxies")
    parser.add_argument("-to", "--timeout", type=int, default=5, help="Timeout in seconds for each proxy check")
    args = parser.parse_args()
    main(args)
