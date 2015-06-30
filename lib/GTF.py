#!/usr/bin/env python
import os, sys

def getLongestTid(gtfpath, gid):
    if gtfpath[-3:] == '.gz':
        infile = gzip.open(gtfpath, 'rb')
    else:
        infile = open(gtfpath, 'r')
    
    gstart, gend = 0, 0
    transdic = {}
    while 1:
        line = infile.readline()
        if not line:
            break
        if line[0] == '#':
            continue
        
        c = line.rstrip().split('\t')
        if gid not in c[8]:
            continue
        if c[2] == 'gene':
            gstart = int(c[3])
            gend   = int(c[4])
        if c[2] == 'transcript' and c[1] == 'protein_coding':
            tid = c[8].split(';')[1].split('"')[1]
            transdic[tid] = [int(c[3]), int(c[4])]

    infile.close()
    longest, longest_tid = 0, ''
    for tid in transdic:
        start = transdic[tid][0]
        end   = transdic[tid][1]
        if start >= gstart and end <= gend:
            pass
        else:
            continue
        if end - start > longest:
            longest = end - start
            longest_tid = tid
    return longest

def getTidGtf(gtfpath, tid):
    if gtfpath[-3:] == '.gz':
        infile = gzip.open(gtfpath, 'rb')
    else:
        infile = open(gtfpath, 'r')

    chain = ''

    while 1:
        line = infile.readline()
        if not line:
            break
        if line[0] == '#':
            continue

        c = line.rstrip().split('\t')
        if tid not in c[8]:
            continue

        if c[2] == 'transcript':
            chain = c[6]
            cdslist = []
        
        if c[2] == 'CDS':
            cdslist.append('%s-%s'%(c[3], c[4]))
    return {'chain':chain, 'cds':cdslist}


        
