#!/usr/bin/env python
from __future__ import division
import os

def calcQ(qseq):
    qlist = [ord(n) for n in qseq]
    return sum(qlist) / len(qlist) * 100

def LoadSam(samPath):
    '''    In:
    LoadSam(samPath)
    Out:
    {HWI-ST1347:50:C1D0UACXX:8:2301:7918:7079:{'bcd': 'chr15:38545396-chr15:38591660-chr15:38591701', 'qlt': 6186.138613861386}, ...}
    '''
    readKeyDic = {}
    if samPath[-3:] == '.gz':
        infile = os.popen('zcat %s | samtools view -S -X -' %samPath)
    else:
        infile = os.popen('cat %s | samtools view -S -X -' %samPath)
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

def test_LoadSam():
    samPath = '../testdata/Chimeric.out.sam.gz'
    return LoadSam(samPath)

if __name__ == '__main__':
    readKeyDic = test_LoadSam()
    for readid in readKeyDic:
        print readid
        print readKeyDic[readid]
        raw_input()
