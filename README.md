-*- mode:org; fill-column:70; coding:utf-8; -*-
* python-hosts-tool
Manage /etc/hosts in an organized way by Python

Read more: https://www.dennyzhang.com/hostsfile_issues/
* How to Install
pip install python-hosts==0.3.7

git clone git@github.com:DennyZhang/python-hosts-tool.git
* How to Use
** Principle:
- Be safe: When remove, make sure it's an exact match; When add, make sure no conflicts
- Can audit: backup old version, if we have changed it
** Use Case: Add a list of new hosts entries
** Use Case: Remove given pattern of new hosts entries
** Use Case: Examine unexpected hosts entries
** Use Case: Beautify /etc/hosts
* todo items
** TODO Send PR for safe delete to python-hosts
https://github.com/jonhadfield/python-hosts

https://pypi.python.org/pypi/python-hosts/0.3.7
