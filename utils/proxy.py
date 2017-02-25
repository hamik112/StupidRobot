#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# --------------------------------
# | Author:   钱磊(Qian Lei)
# | Email:    qianlei90@gmail.com
# | Date:     2017-02-23 19:18:19
# | Version:  1.0
# --------------------------------
#

import requests
from random import choice

from selenium import webdriver

from config import AMAZON_URL, PROXY_CHECK_REQUESTS_TIMEOUT


def delete_proxy_from_pool(ip):
    requests.get('http://127.0.0.1:8000/delete', params={'ip': ip}).json()


def get_proxy_from_pool():
    proxies = requests.get('http://127.0.0.1:8000', params={'protocol': 1, 'types': 0}).json()
    random_proxy = choice(proxies)
    return random_proxy[0], random_proxy[1]


def check_proxy_in_requests(ip, port):
    try:
        r = requests.get(AMAZON_URL, timeout=PROXY_CHECK_REQUESTS_TIMEOUT,
                         proxies={'https': 'https://{ip}:{port}'.format(ip=ip, port=port)})
    except Exception:
        delete_proxy_from_pool(ip)
        return False
    if r.status_code != requests.codes.ok:
        delete_proxy_from_pool(ip)
        return False
    return True


def get_proxy():
    while True:
        proxy_ip, proxy_port = get_proxy_from_pool()
        #  if not check_proxy_in_requests(proxy_ip, proxy_port):
        #      continue
        return proxy_ip, proxy_port
