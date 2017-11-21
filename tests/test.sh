#!/bin/bash -e
##-------------------------------------------------------------------
## @copyright 2017 DennyZhang.com
## Licensed under MIT 
##   https://www.dennyzhang.com/wp-content/mit_license.txt
##
## File : test.sh
## Author : Denny <https://www.dennyzhang.com/contact>
## Description :
## --
## Created : <2017-08-15>
## Updated: Time-stamp: <2017-11-13 11:01:17>
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
