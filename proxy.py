#!/usr/bin/env python3

import time
import yaml
import random as rand
from copy import deepcopy

class proxy(dict):

    def __init__(self, **kwargs):
        self.ip = kwargs['ip']
        self.port = kwargs['port']
        self.user = kwargs['user']
        self.password = kwargs['password']
        self.last_access = None
        self.creation_time = time.time()
        self['http'] = f"socks5://{self.user}:{self.password}@{self.ip}:{self.port}"
        self['https'] = f"socks5://{self.user}:{self.password}@{self.ip}:{self.port}"

    def __getattribute__(self, attr):
        if attr == 'get':
            self.last_access = time.time()
        return object.__getattribute__(self, attr)

    def last_access(self):
        return self.last_access


PROXY_LIMIT = 100
proxies = {}
proxies_available = []
current_proxy_pos = 0

def load_config(filename):
    with open(filename, "r") as infile:
        config = yaml.safe_load(infile)

    for row in config['proxies']:
        create(ip=row['ip'], port=row['port'], user=row['user'], password=row['password'])

def save_config(filename):
    obj = {}
    obj['proxies'] = p = []
    for proxy in proxies.values():
        p.append({'ip': proxy.ip, 'port': int(proxy.port), 'user': proxy.user, 'password': proxy.password})
    with open(filename, "w") as outfile:
        yaml.dump(obj, outfile, default_flow_style=False)

def create(ip: str, port: int, user: str, password: str) -> proxy:
    if ip in proxies:
        return
    new_proxy = proxy(ip=ip, port=port, user=user, password=password)
    proxies[ip] = new_proxy
    proxies_available.append(ip)
    return new_proxy

def remove(ip: str) -> None:
    del proxies[ip]
    proxies_available.remove(ip)

def reserve_random_proxy():
    ip = rand.choice(proxies_available)
    proxies_available.remove(ip)
    dup = deepcopy(proxies[ip])
    return dup

def random():
    ip = rand.choice(proxies_available)
    return proxies[ip]

def round_robin():
    global current_proxy_pos
    new_position = current_proxy_pos % len(proxies_available)
    ip = proxies_available[new_position]
    current_proxy_pos += 1
    return proxies[ip]

def put(returned_proxy):
    proxies_available.append(returned_proxy.ip)
    returned_proxy.clear()

def list():
    return proxies_available
