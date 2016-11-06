#!/usr/bin/env python

import os
import pwd
import grp
import spwd
import yaml

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
    # RSA ssh key, if it exists
    pubkey = "/home/" + user + "/.ssh/id_rsa.pub"
    if os.path.isfile(pubkey):
        key = open(pubkey, 'r')
        for line in key:
            key_data = line.split(' ')
            data['accounts'][user]['ssh_key'] = key_data[1]
        key.close

# Out it comes
print yaml.dump(data, default_flow_style=False)
