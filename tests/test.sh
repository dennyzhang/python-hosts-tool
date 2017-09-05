#!/bin/bash -e
##-------------------------------------------------------------------
## @copyright 2017 DennyZhang.com
## Licensed under MIT 
##   https://raw.githubusercontent.com/DennyZhang/devops_public/master/LICENSE
##
## File : test.sh
## Author : Denny <contact@dennyzhang.com>
## Description :
## --
## Created : <2017-08-15>
## Updated: Time-stamp: <2017-09-04 18:52:17>
##-------------------------------------------------------------------
cd ..

python ./python-hosts-tool.py --action add --add_hosts_file ./tests/test_hosts --dry_run

# Update /etc/hosts by adding hosts binding
python ./python-hosts-tool.py --action add --add_hosts_file ./tests/test_hosts

# Remove binding
python ./python-hosts-tool.py --action remove --remove_hosts_file ./tests/test_hosts

# Examine /etc/hosts
python ./python-hosts-tool.py --action examine --examine_hosts_file ./tests/test_hosts
## File : test.sh ends
