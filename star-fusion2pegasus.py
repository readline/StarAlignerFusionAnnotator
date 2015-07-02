#!/usr/bin/env python
import os, sys

def loadGeneSite(gtfPath):
    siteDic = {}
    infile = open(gtfPath, 'r')
    while 1:
        line = infile.readline()
        if not line:
            break
        if line[0] == '#':
            continue
        c = line.rstrip().split('\t')
        if c[2] != 'gene':
            continue

        gene_id = c[8].split('"')[1]
        siteDic[gene_id] = [c[3], c[4], c[6]]
    infile.close()
    return siteDic

def transform(starPath, siteDic, prefix):
    infile = open(starPath, 'r')
    savefile=open(prefix,   'w')

    while 1:
        line = infile.readline()
        if not line:
            break
        if line[0] == '#':
            continue
        c = line.rstrip().split('\t')
        gene1_name = c[3].split('^')[0]
        gene2_name = c[6].split('^')[0]
        gene1_id   = c[3].split('^')[1].split('.')[0]
        gene2_id   = c[6].split('^')[1].split('.')[0]
        gene1_fus  = c[4].split(':')[1]
        gene2_fus  = c[7].split(':')[1]
        gene1_info = siteDic[gene1_id]
        gene2_info = siteDic[gene2_id]
        
        savefile.write('%s:%s:%s:%s:%s\t%s:%s:%s:%s:%s\n' %(
            gene1_name,
            gene1_info[2],
            gene1_info[0],
            gene1_info[1],
            gene1_fus,
            gene2_name,
            gene2_info[2],
            gene2_info[0],
            gene2_info[1],
            gene2_fus))
    savefile.close()
    infile.close()

def main():
    try:
        starPath = sys.argv[1]
        gtfPath  = sys.argv[2]
        prefix   = sys.argv[3]
    except:
        sys.exit(sys.argv[0] + ' [star fusion result path] [ensembl gtf path] [output prefix]')

    siteDic = loadGeneSite(gtfPath)
    
    transform(starPath, siteDic, prefix)

if __name__ == '__main__':
    main()


        
