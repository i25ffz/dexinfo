'''
Created on 2014-06-24

@author: Fufz
'''

import os, sys, re, getopt

class DexParser:
    def __init__(self):
        self.depth = 2
        self.classes = {}
        self.infos = {}

    def init(self, mapping, depth):
        # reset the depth
        self.depth = depth

        if not os.path.isfile(mapping):
            return

        lines = open(mapping)
        r = re.compile(r'.*->.*:')
        for cls in lines:
            if r.match(cls):
                clsnms = cls.split('->')
                # print cls, clsnms[0], clsnms[1],len(clsnms)
                if len(clsnms) == 2:
                    pkgnms0 = clsnms[0].strip().split('.')
                    # delete last char ':'
                    pkgnms1 = clsnms[1].strip()[:-1].split('.')
                    k0 = v0 = ''
                    if len(pkgnms0) > self.depth:
                        k0 = '.'.join(pkgnms1[0:self.depth])
                        v0 = '.'.join(pkgnms0[0:self.depth])
                    else:
                        k0 = '.'.join(pkgnms1)
                        v0 = '.'.join(pkgnms0)
                    # print k0, v0
                    if k0 != v0 and k0 not in self.classes:
                        self.classes[k0] = v0

    def parse(self, dex):
        cmd = 'dexinfo %s' % dex
        output = os.popen(cmd)
        for line in output:
            if line.startswith('[] Class') and line.find(': L') > 0:
                # get class names && size
                line = line[line.find(': L') + 3:]
                # delete the last "\n" char
                line = line[:-1]

                # get class name and size
                values = line.split(';')

                clsname = values[0].split('/')
                if len(clsname) > self.depth:
                    pkg = '.'.join(clsname[0:self.depth])
                else:
                    pkg = '.'.join(clsname)
                # insert or update pkg size
                if pkg in self.infos:
                    self.infos[pkg] += int(values[1])
                else:
                    self.infos[pkg] = int(values[1])
            else:
                if line.startswith('LinearAlloc'):
                    print line

    def print_info(self):
        # print map
        for (k, v) in self.infos.items():
            if k in self.classes:
                print self.classes[k] + ',' + str(v)
            else:
                print k + ',' + str(v)

if __name__ == '__main__':
    argc = len(sys.argv)
    if argc < 2:
        print 'usage: %s dex [-m,--mapping= mapping.txt] [-d,--depth= depth]' % sys.argv[0]
        sys.exit(1)

    # get opts
    opts, args = getopt.getopt(sys.argv[2:], 'm:d:', ['mapping=', 'depth='])
    mapping = ''
    depth = 2
    for o, a in opts:
        if o in ('-m', '--mapping'):
            mapping = a
        if o in ('-d', '--depth'):
            depth = int(a)

    # parse dex and print information
    parser = DexParser()
    parser.init(mapping, depth)
    parser.parse(sys.argv[1])
    parser.print_info()
