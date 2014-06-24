'''
Created on 2014-06-24

@author: Fufz
'''

import os, sys

maps = {}

if __name__ == '__main__':
    argc = len(sys.argv)
    if argc < 2:
        print 'usage: %s dex depth' % sys.argv[0]
        sys.exit(1)

    cmd = 'dexinfo %s' % sys.argv[1]
    if argc == 3:
        depth = int(sys.argv[2])
    else:
        depth = 3

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
                pkg = '.'.join(clsname[0 : depth])
            else:
                pkg = '.'.join(clsname)
            # insert or update pkg size
            if maps.has_key(pkg):
                maps[pkg] += int(values[1])
            else:
                maps[pkg] = int(values[1])
    # print map
    for (k, v) in  maps.items():
        print k + ',' + str(v)