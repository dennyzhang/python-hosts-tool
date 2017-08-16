# python-hosts-tool
Manage /etc/hosts in an organized way by Python

Read more: https://www.dennyzhang.com/hostsfile_issues/

# How to Install

```
pip install python-hosts==0.3.7
git clone git@github.com:DennyZhang/python-hosts-tool.git
```

# Principle:
- Be safe: When remove, make sure it's an exact match; When add, make sure no conflicts
- Can audit: backup old version, if we have changed it

# How to Use

```
##        # Add a list of new hosts entries
##        python ./python-hosts-tool.py --action add --add_hosts_file ./tests/test_hosts
##
##        # Remove a list of existing hosts
##        python ./python-hosts-tool.py --action remove --remove_hosts_file ./tests/test_hosts
##
##        # Examine hosts file, and detect unexpected changes
##        python ./python-hosts-tool.py --action examine --examine_hosts_file ./tests/test_hosts
```
# todo items
** TODO Send PR for safe delete to python-hosts
https://github.com/jonhadfield/python-hosts

https://pypi.python.org/pypi/python-hosts/0.3.7
