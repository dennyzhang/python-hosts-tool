#!/usr/bin/python
##-------------------------------------------------------------------
## @copyright 2017 DennyZhang.com
## Licensed under MIT
##   https://raw.githubusercontent.com/DennyZhang/devops_public/master/LICENSE
##
## File : python-hosts-tool.py
## Author : Denny <denny@dennyzhang.com>
## Created : <2017-05-03>
## Updated: Time-stamp: <2017-08-15 19:43:16>
## Description :
##    Load an extra hosts binding into /etc/hosts
## Sample:
##        # Add a list of new hosts entries
##        python ./python-hosts-tool.py --action add --add_hosts_file ./tests/test_hosts
##
##        # Remove a list of existing hosts
##        python ./python-hosts-tool.py --action remove --remove_hosts_file ./tests/test_hosts
##
##        # Examine hosts file, and detect unexpected changes
##        python ./python-hosts-tool.py --action examine --examine_hosts_file ./tests/test_hosts
##
## Read More: https://www.dennyzhang.com/hostsfile_issues
##-------------------------------------------------------------------
import os, sys
import argparse
import socket, datetime
from shutil import copyfile
from python_hosts import Hosts, HostsEntry

import logging
log_folder = "%s/log" % (os.path.expanduser('~'))
if os.path.exists(log_folder) is False:
    os.makedirs(log_folder)
log_file = "%s/%s.log" % (log_folder, os.path.basename(__file__).rstrip('\.py'))

logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s %(message)s')
logging.getLogger().addHandler(logging.StreamHandler())

################################################################################
# TODO: create PR to https://github.com/jonhadfield/python-hosts
def is_equal(entry1, entry2):
    return str(entry1) == str(entry2)

# TODO: create PR to https://github.com/jonhadfield/python-hosts
def get_hosts_entries(hosts, address=None, names=None):
    l = []
    for entry in hosts.entries:
        if entry.entry_type in ('ipv4', 'ipv6'):
            if address and address == entry.address:
                l.append(entry)
            else:
                if names:
                    for name in names:
                        if name in entry.names:
                            l.append(entry)
                            break
    return l
    
################################################################################
# TODO: move to common library
def backup_file_with_timestamp(filepath):
    # Backup file to the same folder by adding timestamp as postfix
    # Sample: /etc/hosts -> /etc/hosts.2017-08-15_182230
    backup_file = "%s.%s" % (filepath, \
                             datetime.datetime.utcnow().strftime("%Y-%m-%d_%H%M%S"))
    logging.info("Backup %s to %s" % (filepath, backup_file))
    # TODO: add error handling
    copyfile(filepath, backup_file)

################################################################################
def save_change(hosts, has_changed):
    if has_changed is True:
        backup_file_with_timestamp("/etc/hosts")
        hosts.write()
    else:
        logging.info("OK: no changes has happened. Skip updating /etc/hosts")


def add_hosts(hosts_origin, hosts_extra):
    origin_entries = hosts_origin.entries
    extra_entries = hosts_extra.entries
    has_changed = False
    for entry in extra_entries:
        if entry.entry_type == 'comment':
            continue

        l = get_hosts_entries(hosts_origin, address=entry.address, names=entry.names)
        if len(l) == 0:
            has_changed = True
            logging.info("Add entry: %s" % (entry))
            hosts_origin.add([entry])
        elif len(l) == 1:
            if is_equal(l[0], entry) is True:
                continue
            else:
                print("not equal: l[0]: %s, entry: %s" % (l[0], entry))
                logging.error("Conflict: Fail to add %s" % (entry))
        else:
            logging.error("Original hosts file has duplicate entries")
    save_change(hosts_origin, has_changed)

def remove_hosts(hosts_origin, hosts_extra):
    origin_entries = hosts_origin.entries
    extra_entries = hosts_extra.entries
    has_changed = False
    for entry in extra_entries:
        if entry.entry_type == 'comment':
            continue

        l = get_hosts_entries(hosts_origin, address=entry.address, names=entry.names)
        if len(l) == 0:
            continue
        elif len(l) == 1:
            if is_equal(l[0], entry) is True:
                has_changed = True
                print "address: %s" % (entry.address)
                print "names: %s" % (entry.names[0])
                print "hosts_origin: %s" % (hosts_origin)
                hosts_origin.remove_all_matching(address=entry.address, name=entry.names)
            else:
                print("not equal: l[0]: %s, entry: %s" % (l[0], entry))
                logging.error("Conflict: Fail to remove %s" % (entry))
        else:
            logging.error("Original hosts file has duplicate entries")
    save_change(hosts_origin, has_changed)

if __name__ == '__main__':
    # get parameters from users
    parser = argparse.ArgumentParser()
    parser.add_argument('--action', required=True, \
                        help="Supported action: add,remove,examine", type=str)
    parser.add_argument('--add_hosts_file', required=False, default="", \
                        help="Load extra hosts into /etc/hosts", type=str)
    parser.add_argument('--remove_hosts_file', required=False, default="", \
                        help="Remove extra hosts from /etc/hosts", type=str)
    parser.add_argument('--examine_hosts_file', required=False, default="", \
                        help="Detect unexpected binding in /etc/hosts", type=str)

    parser.add_argument('--skip_current_hostname', required=False, dest='skip_current_hostname', \
                        action='store_true', default=False, \
                        help="Skip any actions related to current hostname")

    l = parser.parse_args()
    action = l.action
    add_hosts_file = l.add_hosts_file
    remove_hosts_file = l.remove_hosts_file
    examine_hosts_file = l.examine_hosts_file

    # Convert a string to preexisting variable names
    # When action is add, extra_host_file points to add_hosts_file
    extra_hosts_file = eval("%s_hosts_file" % (action))

    # Parameter Check
    if action not in ['add', 'remove', 'examine']:
        logging.error("Not supported action: %s" % (action))
        sys.exit(1)

    if extra_hosts_file == "":
        logging.error("When action is %s, %s_hosts_file should be given" % (action, action))
        sys.exit(1)
    if os.path.exists(extra_hosts_file) is False:
        logging.error("File(%s) doesn't exist" % (extra_hosts_file))
        sys.exit(1)

    hosts_origin = Hosts(path='/etc/hosts')
    hosts_extra = Hosts(path=extra_hosts_file)

    if action == 'add':
        add_hosts(hosts_origin, hosts_extra)

    if action == 'remove':
        remove_hosts(hosts_origin, hosts_extra)
## File : python-hosts-tool.py ends
