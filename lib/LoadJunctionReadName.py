#!/usr/bin/env python

def loadJunctionReadName(junctionReadNamePath, candidateDic):
    '''    In:\
    loadJunctionReadName(junctionReadNamePath, candidateDic)\
    Out:\
    {9:{'HWI-ST1347:50:C1D0UACXX:8:1206:5976:79011': 1, 'HWI-ST1347:50:C1D0UACXX:8:1315:6627:4092': 1, 'HWI-ST1347:50:C1D0UACXX:8:1207:11734:63567': 1, 'HWI-ST1347:50:C1D0UACXX:8:1316:7944:26265': 1, 'HWI-ST1347:50:C1D0UACXX:8:2112:8264:50480': 1, 'HWI-ST1347:50:C1D0UACXX:8:1315:8322:7553': 1, 'HWI-ST1347:50:C1D0UACXX:8:1215:9746:58249': 1, 'HWI-ST1347:50:C1D0UACXX:8:1107:19085:27860': 1, 'HWI-ST1347:50:C1D0UACXX:8:1215:6263:47832': 1, 'HWI-ST1347:50:C1D0UACXX:8:2106:3798:33225': 1, 'HWI-ST1347:50:C1D0UACXX:8:1209:15836:88457': 1, 'HWI-ST1347:50:C1D0UACXX:8:2212:9389:45464': 1}, ...}\
    '''
    tmphash = {}
    for cand in candidateDic:
        c = candidateDic[cand]
        juncId = '%s;%s;%s;%s;%s;%s;%s--%s;%s' %(
                c['LeftGene'],
                c['LeftBreakpoint'],
                c['LeftDistFromRefExonSplice'],
                c['RightGene'],
                c['RightBreakpoint'],
                c['RightDistFromRefExonSplice'],
                c['LeftGene'],
                c['RightGene'],
                c['fusion_name'])
        tmphash[juncId] = cand
    for n in tmphash:
        if 'ENSG00000115310.13' in n and 'ENSG00000143947.8' in n:
            print n

    infile = open(junctionReadNamePath, 'r')
    junctionReadDic = {}
    while 1:
        line = infile.readline()
        if not line:
            break
        c = line.rstrip().split('\t')
        if c[1] not in tmphash:
            # filted out candidates
            continue
        if tmphash[c[1]] not in junctionReadDic:
            junctionReadDic[tmphash[c[1]]] = {}
        junctionReadDic[tmphash[c[1]]][c[2]] = 1
    infile.close()
    
    return junctionReadDic

def test_loadFusionCandidates():
    from LoadCandidates import test_loadFusionCandidates
    candidateDic = test_loadFusionCandidates()

    junctionReadNamePath = '../testdata/star-fusion.junction_read_names'

    return loadJunctionReadName(junctionReadNamePath, candidateDic)
    
if __name__ == '__main__':
    tmpdic = test_loadFusionCandidates()
    for n in tmpdic:
        print n
        print tmpdic[n]


