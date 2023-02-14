# Multi-threaded SOCKS5 Proxy Checker

This is a python script that checks the availability of SOCKS5 proxies from a list of proxies and saves the available ones in a separate file. The script uses multiple threads to perform the checks concurrently, making the process faster.

## Requirements
- Python 3.x

## Usage

python socks5_checker.py [options]


### Options
- `--list`: Provide the path to the list of proxies. Default is 'list.txt'
- `-t`: Number of threads to use. Default is 10.
- `-v`: Verbose output. Show progress while checking proxies.

### Example

`python socks5_checker.py --list proxy_list.txt -t 50 -v`

### List Format
The list should contain one proxy per line, in the format `IP:PORT`. If the proxy requires a username and password, the line should be in the format `IP:PORT:USERNAME:PASSWORD`.

## Output
The available proxies will be saved in the file `out.txt`. The script will overwrite the file if it already exists.

## Note
This script only supports SOCKS5 proxies, not HTTP proxies.
