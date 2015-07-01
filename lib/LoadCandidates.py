#!/usr/bin/env python

def loadFusionCandidates(candidatesPath, cut1=[2,5], cut2=[1,10], cut3=[0,20]):
    '''    In:\
    loadFusionCandidates(candidatesPath, cut1=[2,5], cut2=[1,10], cut3=[0,20])
    Out:
    1: {'LeftBreakpoint': 'chr19:54515463:+', \
    'RightDistFromRefExonSplice': '19', \
    'SpanningFrags': '53', \
    'RightGene': 'RPLP2^ENSG00000177600.4', \
    'LeftDistFromRefExonSplice': '455', \
    'RightBreakpoint': 'chr11:810022:+', \
    'JunctionReads': '55', \
    'LeftGene': 'CACNG6^ENSG00000130433.3', \
    'fusion_name': 'CACNG6--RPLP2'}, 
    '''

    candidateDic = {}
    count = 0
    infile = open(candidatesPath, 'r')
    header = infile.readline().lstrip('#').rstrip('\n').split('\t')
    while 1:
        line = infile.readline()
        if not line:
            break
        c = line.rstrip().split('\t')

        # 1. Remove both chrM fusion
        if c[4].split(':')[0] == 'chrM' and c[7].split(':')[0] == 'chrM':
            continue

        if int(c[1]) >= 2 and int(c[2]) >= 5:
            # 2. keep >= 2 junction reads and >= 5 spanning frags
            pass
        elif int(c[1]) >= 1 and int(c[2]) >= 10:
            # 3. keep >= 1 junction reads and >= 10 spanning frags
            pass
        elif int(c[1]) >= 0 and int(c[2]) >= 20:
            # 4. keep >= 0 junction reads and >= 20 spanning frags
            pass
        else:
            continue

        candidateDic[count] = {}
        for n in range(len(header)):
            candidateDic[count][header[n]] = c[n]
        count += 1
    infile.close()
    return candidateDic

def test_loadFusionCandidates():
    candidatesPath = '../testdata/star-fusion.fusion_candidates.final'
    
    candidateDic = loadFusionCandidates(candidatesPath)

    print candidateDic

if __name__ == '__main__':
    test_loadFusionCandidates()
