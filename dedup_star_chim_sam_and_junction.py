#!/usr/bin/env python
from __future__ import division
import os, sys, gzip

def calcQ(qseq):
    qlist = [ord(n) for n in qseq]
    return sum(qlist) / len(qlist) * 100

def loadSam(samPath):
    readKeyDic = {}
    if samPath[-3:] == '.gz':
        infile = gzip.open(samPath, 'rb')
    else:
        infile = open(samPath, 'r')
    while 1:
        line = infile.readline()
        if not line:
            break
        if line[0] == '@':
            continue
        c = line.rstrip().split('\t')
        if c[0] not in readKeyDic:
            readKeyDic[c[0]] = {'bcd':[], 'qlt':[]}
        readKeyDic[c[0]]['bcd'].append('%s:%s' %(c[2], c[3]))
        readKeyDic[c[0]]['qlt'].append(calcQ(c[10]))
    
    infile = ''

    for readid in readKeyDic:
        tmpqlt = sum(set(readKeyDic[readid]['qlt'])) / 2
        tmpbcd = '-'.join(sorted(readKeyDic[readid]['bcd']))
        readKeyDic[readid]['qlt'] = tmpqlt
        readKeyDic[readid]['bcd'] = tmpbcd

    return readKeyDic

def dedup(readKeyDic):
    bcdDic = {}
    for readid in readKeyDic:
        bcd = readKeyDic[readid]['bcd']
        if bcd not in bcdDic:
            bcdDic[bcd] = {}
        bcdDic[bcd][readid] = readKeyDic[readid]['qlt']

    dupDic = {}
    for bcd in bcdDic:
        if len(bcdDic[bcd]) == 1:
            pass
        elif len(bcdDic[bcd]) >1:
            maxqlt = 0
            maxid  = ''
            for readid in bcdDic[bcd]:
                if bcdDic[bcd][readid] > maxqlt:
                    maxqlt = bcdDic[bcd][readid]
                    maxid  = readid
            for readid in bcdDic[bcd]:
                if readid == maxid:
                    pass
                else:
                    dupDic[readid] = 1
    return dupDic

def writeSam(samPath, dupDic, prefix):
    if samPath[-3:] == '.gz':
        infile = gzip.open(samPath, 'rb')
    else:
        infile = open(samPath, 'r')

    savefile = gzip.open('%s.sam.gz'%prefix, 'wb')
    while 1:
        line = infile.readline()
        if not line:
            break
        if line[0] == '@':
            savefile.write(line)
            continue
        if line.split('\t')[0] not in dupDic:
            savefile.write(line)
            continue
    savefile.close()
    infile.close()

def writeJunc(juncPath, dupDic, prefix):
    if juncPath[-3:] == '.gz':
        infile = gzip.open(juncPath, 'rb')
    else:
        infile = open(juncPath, 'r')

    savefile = gzip.open('%s.junction.gz'%prefix, 'wb')
    while 1:
        line = infile.readline()
        if not line:
            break
        if line.split('\t')[9] not in dupDic:
            savefile.write(line)
            continue
    savefile.close()
    infile.close()


def main():
    try:
        samPath = sys.argv[1]
        juncPath = sys.argv[2]
        prefix  = sys.argv[3]
    except:
        sys.exit(sys.argv[0] + ' [input sam path] [input junction path] [output prefix]')
    
    readKeyDic = loadSam(samPath) 
    print 'Sam file loaded.'

    dupDic = dedup(readKeyDic)
    print 'Dedup finished. %d duplicate reads found.' %(len(dupDic))

    writeSam(samPath, dupDic, prefix)
    print 'Write sam done!'

    writeJunc(juncPath, dupDic, prefix)
    print 'Write junction done!'

if __name__ == '__main__':
    main()
