#!/usr/bin/env python

def loadSpanningReadName(spanningReadNamePath, candidateDic):
    '''    In:
    loadSpanningReadName(spanningReadNamePath, candidateDic)
    Out:
    {9:{'HWI-ST1347:50:C1D0UACXX:8:1206:5976:79011': 1, 'HWI-ST1347:50:C1D0UACXX:8:1315:6627:4092': 1, 'HWI-ST1347:50:C1D0UACXX:8:2215:11770:26353': 1, 'HWI-ST1347:50:C1D0UACXX:8:1316:7944:26265': 1, 'HWI-ST1347:50:C1D0UACXX:8:2112:8264:50480': 1, 'HWI-ST1347:50:C1D0UACXX:8:1315:8322:7553': 1, 'HWI-ST1347:50:C1D0UACXX:8:1215:9746:58249': 1, 'HWI-ST1347:50:C1D0UACXX:8:1209:13068:19281': 1, 'HWI-ST1347:50:C1D0UACXX:8:1215:9137:88681': 1, 'HWI-ST1347:50:C1D0UACXX:8:1215:6263:47832': 1, 'HWI-ST1347:50:C1D0UACXX:8:1316:9077:6415': 1, 'HWI-ST1347:50:C1D0UACXX:8:1107:19085:27860': 1, 'HWI-ST1347:50:C1D0UACXX:8:1207:11734:63567': 1, 'HWI-ST1347:50:C1D0UACXX:8:2106:3798:33225': 1, 'HWI-ST1347:50:C1D0UACXX:8:1209:15836:88457': 1, 'HWI-ST1347:50:C1D0UACXX:8:2205:8292:67281': 1, 'HWI-ST1347:50:C1D0UACXX:8:2212:9389:45464': 1, 'HWI-ST1347:50:C1D0UACXX:8:1309:14076:41658': 1, 'HWI-ST1347:50:C1D0UACXX:8:1209:2880:54510': 1, 'HWI-ST1347:50:C1D0UACXX:8:1305:4772:30591': 1}, ...}
    '''
    tmphash = {}
    for cand in candidateDic:
        c = candidateDic[cand]
        juncId = '%s--%s' %(
                c['LeftGene'],
                c['RightGene'])
        if juncId not in tmphash:
            tmphash[juncId] = {}
        tmphash[juncId][cand] = 1

    infile = open(spanningReadNamePath, 'r')

    spanningReadDic = {}
    while 1:
        line = infile.readline()
        if not line:
            break
        c = line.rstrip().split('\t')
        if c[0] not in tmphash:
            # filted out candidates
            continue
        for candid in tmphash[c[0]]:
            if candid not in spanningReadDic:
                spanningReadDic[candid] = {}
            if c[1] not in spanningReadDic[candid]:
                spanningReadDic[candid][c[1]] = 1

    infile.close()
    
    return spanningReadDic

def test_loadSpanningReadName():
    from LoadCandidates import test_loadFusionCandidates
    candidateDic = test_loadFusionCandidates()

    spanningReadNamePath = '../testdata/star-fusion.spanning_read_names'

    return loadSpanningReadName(spanningReadNamePath, candidateDic)
    
if __name__ == '__main__':
    tmpdic = test_loadSpanningReadName()
    for n in tmpdic:
        print n
        print str(tmpdic[n])[:60]
        print len(tmpdic[n])
        print len(set((tmpdic[n].keys())))
        raw_input()
        


