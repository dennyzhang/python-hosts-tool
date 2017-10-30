<a href="https://github.com/DennyZhang?tab=followers"><img align="right" width="200" height="183" src="https://raw.githubusercontent.com/USDevOps/mywechat-slack-group/master/images/fork_github.png" /></a>

[![Build Status](https://travis-ci.org/DennyZhang/python-hosts-tool.svg?branch=master)](https://travis-ci.org/DennyZhang/python-hosts-tool) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

[![LinkedIn](https://raw.githubusercontent.com/USDevOps/mywechat-slack-group/master/images/linkedin.png)](https://www.linkedin.com/in/dennyzhang001) [![Github](https://raw.githubusercontent.com/USDevOps/mywechat-slack-group/master/images/github.png)](https://github.com/DennyZhang) [![Twitter](https://raw.githubusercontent.com/USDevOps/mywechat-slack-group/master/images/twitter.png)](https://twitter.com/dennyzhang001) [![Slack](https://raw.githubusercontent.com/USDevOps/mywechat-slack-group/master/images/slack.png)](https://goo.gl/ozDDyL)

- File me [tickets](https://github.com/DennyZhang/python-hosts-tool/issues) or star [the repo](https://github.com/DennyZhang/python-hosts-tool)

# python-hosts-tool
Manage /etc/hosts in an organized way by Python

Read more: https://www.dennyzhang.com/audit_hostsfile

# Principle:
- **Be safe**: When remove, make sure it's an exact match; When add, make sure no conflicts
- **Can audit**: backup old version, if we have changed it

# Online Usage
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

# How to Install
```
pip install python-hosts==0.3.7
# get the tool
wget -O python-hosts-tool.py \
    https://raw.githubusercontent.com/DennyZhang/python-hosts-tool/master/python-hosts-tool.py

# Or git clone
git clone git@github.com:DennyZhang/python-hosts-tool.git
```

# How to Use
- Sample content of [./tests/test_hosts](./tests/test_hosts)
```
cat ./tests/test_hosts
45.33.87.75 www.dennytest.com
104.236.158.226 repo.dennytest.com
```

- Run command

# How To Run test
```
cd tests
sudo bash -ex ./test.sh
```
# TODO Items

- Send PR for safe delete to python-hosts

https://github.com/jonhadfield/python-hosts

https://pypi.python.org/pypi/python-hosts/0.3.7

Code is licensed under [MIT License](https://www.dennyzhang.com/wp-content/mit_license.txt).
