#!/usr/bin/env python3

import sys
import proxy
import requests
import time
import logging
logging.basicConfig(level=logging.INFO)

# Create a new proxy manually
proxy.create(ip="192.168.1.100", port="8128", user="vvv_proxy", password="password")

# Add another proxy manually
proxy.create(ip="192.168.1.101", port="8128", user="vvv_proxy", password="password")

# Read proxies from file
proxy.load_config("proxy_list.yaml")

#List proxies
ips = proxy.list()

for ip in ips:
    print(ip)

#Write proxies to file
#proxy.save_config("proxy_list.yaml")

# Check if round-robin proxying works correctly
for _ in range(0, len(proxy.list())):
    r = requests.get("http://icanhazip.com", proxies=proxy.round_robin())
    content = r.text.strip()
    logging.info(f"Current IP detected: {content} (These should all be different)")

# Reserve a proxy out of pool
my_proxy = proxy.reserve_random_proxy()

# Test reserved proxy
r = requests.get("http://icanhazip.com", proxies=proxy.round_robin())
content = r.text.strip()
logging.info(f"Current Reserved IP: {content}")

# Put reserved proxy back into pool
proxy.put(my_proxy)

# Verify previous reserved proxy is now empty
logging.info(f"Previous Reserved Proxy is: {my_proxy}")
