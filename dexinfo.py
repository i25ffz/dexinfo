'''
Created on 2014-06-24

@author: Fufz
'''

import os, sys, re

maps = {}
clses = {}

def get_name(pkg):
    if pkg in clses:
        return clses[pkg]
    else:
        return pkg

def fill_pkg(mapping, depth):
    r = re.compile(r'.*->.*:')
    mapf = open(mapping)
    for cls in mapf:
        if r.match(cls):
            clsnms = cls.split('->')
            # print cls, clsnms[0], clsnms[1],len(clsnms)
            if len(clsnms) == 2:
                pkgnms0 = clsnms[0].strip().split('.')
                # delete last char ':'
                pkgnms1 = clsnms[1].strip()[:-1].split('.')
                k0 = v0 = ''
                if len(pkgnms0) > depth:
                    k0 = '.'.join(pkgnms1[0:depth])
                    v0 = '.'.join(pkgnms0[0:depth])
                else:
                    k0 = '.'.join(pkgnms1)
                    v0 = '.'.join(pkgnms0)
                # print k0, v0
                if k0 != v0 and k0 not in clses:
                    clses[k0] = v0

if __name__ == '__main__':
    argc = len(sys.argv)
    if argc < 3:
        print 'usage: %s dex mapping [depth]' % sys.argv[0]
        sys.exit(1)

    # fill args
    cmd = 'dexinfo %s' % sys.argv[1]
    mapping = sys.argv[2]
    if argc >= 4:
        depth = int(sys.argv[3])
    else:
        depth = 3

    # fill pkg
    fill_pkg(mapping, depth)

    output = os.popen(cmd)
    for line in output:
        if line.startswith('[] Class') and line.find(': L') > 0:
            # get class names && size
            line = line[line.find(': L') + 3:]
            # delete the last "\n" char
            line = line[:-1]

            #get class name and size
            values = line.split(';')

            clsname = values[0].split('/')
            if len(clsname) > depth:
                pkg = '.'.join(clsname[0:depth])
            else:
                pkg = '.'.join(clsname)
            # insert or update pkg size
            if pkg in maps:
                maps[pkg] += int(values[1])
            else:
                maps[pkg] = int(values[1])
    # print map
    for (k, v) in maps.items():
        print get_name(k) + ',' + str(v)
