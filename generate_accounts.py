#!/usr/bin/env python

import os
import pwd
import grp
import spwd
import yaml
import re

# A data structure
data = { 'accounts': {} }

# First, get a list of users:
users = []
for p in pwd.getpwall():
    if p.pw_uid >= 1000 and p.pw_name != "nobody":
        users.append(p.pw_name)

for user in users:
    # passwd data
    p = pwd.getpwnam(user)
    data['accounts'][user] = {}
    data['accounts'][user]['uid'] = p.pw_uid
    data['accounts'][user]['comment'] = p.pw_gecos
    data['accounts'][user]['home_dir'] = p.pw_dir
    data['accounts'][user]['shell'] = p.pw_shell
    # shadow data
    s = spwd.getspnam(user)
    data['accounts'][user]['password'] = s.sp_pwd
    # group data
    data['accounts'][user]['groups'] = []
    for g in grp.getgrall():
        if user in g.gr_mem:
            data['accounts'][user]['groups'].append(g.gr_name)
    # Get SSH keys from authorized_keys
    authorized_keys = "/home/" + user + "/.ssh/authorized_keys"
    if os.path.isfile(authorized_keys):
        data['accounts'][user]['ssh_keys'] = {}
        keys = open(authorized_keys, 'r')
        for line in keys:
            line = line.strip()
            key_data = line.split(' ')
            data['accounts'][user]['ssh_keys'][key_data[2]] = \
                { 'type': key_data[0], 'key': key_data[1] }
        keys.close

# Out it comes
print yaml.dump(data, default_flow_style=False)
