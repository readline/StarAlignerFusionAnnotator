#!/usr/bin/env python
# =============================================================================
# Filename: star-fusion-filter.py
# Version: 
# Author: Kai Yu - finno@live.cn
# https://github.com/readline
# Last modified: 2015-06-30 14:58
# Description: 
# 
# =============================================================================
import os, sys

def main():
    try:
        inpath = sys.argv[1]
        outpath= sys.argv[2]
    except:
        sys.exit(sys.argv[0] + ' [input star fusion path] [output filted path]')

    infile = open(inpath, 'r')
    savefile = open(outpath, 'w')
    header = infile.readline().rstrip().split('\t')
    savefile.write('\t'.join(header) + '\n')
    while 1:
        line = infile.readline()
        if not line:
            break
        c = line.rstrip().split('\t')

        # 1. Remove both chrM fusion
        if c[4].split(':')[0] == 'chrM' and c[7].split(':')[0] == 'chrM':
            continue

        # 2. keep >= 2 junction reads and >= 5 spanning frags
        if int(c[1]) >= 2 and int(c[2]) >= 5:
            savefile.write(line)
            continue

        # 3. keep >= 1 junction reads and >= 10 spanning frags
        if int(c[1]) >= 1 and int(c[2]) >= 10:
            savefile.write(line)
            continue
        
        # 4. keep >= 0 junction reads and >= 20 spanning frags
        if int(c[1]) >= 0 and int(c[2]) >= 20:
            savefile.write(line)
            continue

    savefile.close()
    infile.close()

if __name__ == '__main__':
    main()
