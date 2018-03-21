#!/usr/bin/python
##-------------------------------------------------------------------
## File : get_ssh_list_from_url.py
## Author : Denny
## Description :
## --
## Created : <2017-06-08>
## Updated: Time-stamp: <2018-03-21 00:48:25>
##-------------------------------------------------------------------
import sys, os
import requests
import argparse

def get_ip_list_from_url(http_url):
    http_repsonse = requests.get(http_url)

    content = http_repsonse.content
    status_code= http_repsonse.status_code

    if status_code != 200:
        print("ERROR: http request(%s) failed. Status_code: %s, content:%s" \
              % (http_url, status_code, content))
        sys.exit(1)
    content = content.strip()

    return content.split("\n")

# Sample: python ./get_ssh_list_from_url.py --http_url "https://www.test.com/querycluster/all"
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--http_url', default='',
                        required=True, help="URL to return a ip list", type=str)
    parser.add_argument('--ssh_port', default='2702',
                        required=False, help="sshd port to connect", type=str)
    l = parser.parse_args()
    http_url = l.http_url
    ssh_port = l.ssh_port

    ip_list = []
    for ip in get_ip_list_from_url(http_url):
        ip_list.append("%s:%s" % (ip, ssh_port))
    print("\n".join(ip_list))
## File : get_ssh_list_from_url.py ends
