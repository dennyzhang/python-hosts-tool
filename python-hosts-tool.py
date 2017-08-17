#!/usr/bin/python
##-------------------------------------------------------------------
## @copyright 2017 DennyZhang.com
## Licensed under MIT
##   https://raw.githubusercontent.com/DennyZhang/devops_public/master/LICENSE
##
## File : python-hosts-tool.py
## Author : Denny <denny@dennyzhang.com>
## Created : <2017-05-03>
## Updated: Time-stamp: <2017-08-16 21:18:59>
## Description :
##    Load an extra hosts binding into /etc/hosts
## Sample:
##        # Add a list of new hosts entries
##        python ./python-hosts-tool.py --action add --add_hosts_file ./tests/test_hosts
##
##        # Add a list of new hosts entries in dry-run mode. No real changes
##        python ./python-hosts-tool.py --action add --add_hosts_file ./tests/test_hosts --dry_run
####
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
def save_change(hosts, has_changed, dry_run):
    if has_changed is True:
        if dry_run is True:
            logging.info("Skip changes, since --dry_run option is enabled")
        else:
            backup_file_with_timestamp("/etc/hosts")
            hosts.write()
    else:
        logging.info("OK: no changes has happened. Skip updating /etc/hosts")


def add_hosts(hosts_origin, hosts_extra, dry_run):
    origin_entries = hosts_origin.entries
    extra_entries = hosts_extra.entries
    has_changed = False
    current_hostname = socket.gethostname()
    for entry in extra_entries:
        if entry.entry_type in ['comment', 'blank']:
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
                if current_hostname in entry.names:
                    hosts_origin.add([entry])
                else:
                    print("not equal: l[0]: %s, entry: %s" % (l[0], entry))
                    logging.error("Conflict: Fail to add %s" % (entry))
                    sys.exit(1)
        else:
            logging.error("Original hosts file has duplicate entries. entry: %s,\nmatched:%s" \
                          % (entry, l))
            sys.exit(1)

    save_change(hosts_origin, has_changed, dry_run)
        
def remove_hosts(hosts_origin, hosts_extra, dry_run):
    origin_entries = hosts_origin.entries
    extra_entries = hosts_extra.entries
    has_changed = False
    for entry in extra_entries:
        if entry.entry_type in ['comment', 'blank']:
            continue
        l = get_hosts_entries(hosts_origin, address=entry.address, names=entry.names)
        if len(l) == 0:
            continue
        elif len(l) == 1:
            if is_equal(l[0], entry) is True:
                has_changed = True
                logging.info("Remove entry: %s" % (entry))
                hosts_origin.remove_all_matching(address=entry.address)
            else:
                print("not equal: l[0]: %s, entry: %s" % (l[0], entry))
                logging.error("Conflict: Fail to remove %s" % (entry))
                sys.exit(1)
        else:
            logging.error("Original hosts file has duplicate entries. entry: %s,\nmatched:%s" \
                          % (entry, l))
            sys.exit(1)
    save_change(hosts_origin, has_changed, dry_run)

def examine_hosts(hosts_origin, hosts_extra, dry_run):
    origin_entries = hosts_origin.entries
    extra_entries = hosts_extra.entries
    unexpected_entries = []
    skip_list = ["localhost", "127.0.0.1", "255.255.255.255", "127.0.1.1"]
    skip_list += ["ip6-localnet", "ip6-mcastprefix", "ip6-allnodes", "ip6-allrouters", "ip6-allhosts", "ip6-localhost"]
    # Get current hostname
    skip_list.append(socket.gethostname())
    for entry in origin_entries:
        if entry.entry_type in ['comment', 'blank']:
            continue

        if entry.address in skip_list:
            continue

        has_matched = False
        for name in entry.names:
            if name in skip_list:
                has_matched = True
                break
        if has_matched is True:
            continue

        l = get_hosts_entries(hosts_extra, address=entry.address, names=entry.names)
        if len(l) == 0:
            unexpected_entries.append(entry)
        elif len(l) == 1:
            if is_equal(l[0], entry) is True:
                continue
            else:
                logging.warning("Detect Conflict for %s" % (entry))
                unexpected_entries.append(entry)
        else:
            logging.error("Original hosts file has duplicate entries. entry: %s,\nmatched:%s" \
                          % (entry, l))
            sys.exit(1)
    if len(unexpected_entries) != 0:
        func = lambda entry: str(entry)
        logging.error("Unexpected binding in your hosts file: \n%s" % "\n".join(map(func, unexpected_entries)))
        sys.exit(1)
    else:
        logging.info("OK: no unexpected binding in your hosts file")


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
    parser.add_argument('--dry_run', dest='dry_run', action='store_true', default=False, \
                        help="Dryrun without real changes")

    l = parser.parse_args()
    action = l.action
    dry_run = l.dry_run
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

    fun_name = eval("%s_hosts" % (action))
    fun_name(hosts_origin, hosts_extra, dry_run)
## File : python-hosts-tool.py ends
