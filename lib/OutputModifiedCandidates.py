#!/usr/bin/env python
import gzip

def countUniq(readDic):
    count = 0
    for readid in readDic:
        if readDic[readid] == 1:
            count += 1
    return count


def output(candidateDic, junctionDedupReadDic, spanningDedupReadDic, samPath, prefix):

    # Output canditate file
    savefile = open('%s.fusion_candidates.final' %prefix, 'w')
    header = ['fusion_name','JunctionReads','SpanningFrags','LeftGene','LeftBreakpoint','LeftDistFromRefExonSplice','RightGene','RightBreakpoint','RightDistFromRefExonSplice']
    savefile.write('#%s\n' %('\t'.join(header)))
    for candid in sorted(candidateDic.keys()):
        candtmp = candidateDic[candid]
        candtmp['JunctionReads'] = countUniq(junctionDedupReadDic[candid])
        candtmp['SpanningFrags'] = countUniq(spanningDedupReadDic[candid])
        savefile.write('\t'.join([str(candtmp[n]) for n in header]) + '\n')
    savefile.close()

    allReadIdDic = {}
    # Output junction file
    savefile = open('%s.junction_read_names'%prefix, 'w')
    for candid in sorted(candidateDic.keys()):
        c = candidateDic[candid]
        id1 = '%s--%s' %(c['LeftGene'], c['RightGene'])
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
        for readid in junctionDedupReadDic[candid]:
            if junctionDedupReadDic[candid][readid] == 1:
                savefile.write('%s\t%s\t%s\n' %(id1, juncId, readid))
                allReadIdDic[readid] = 1
    savefile.close()

    # Output spanning file
    savefile = open('%s.spanning_read_names' %prefix, 'w')
    for candid in sorted(candidateDic.keys()):
        c = candidateDic[candid]
        id1 = '%s--%s' %(c['LeftGene'], c['RightGene'])
        for readid in spanningDedupReadDic[candid]:
            if spanningDedupReadDic[candid][readid] == 1:
                savefile.write('%s\t%s\t%s\n' %(id1, juncId, readid))
                allReadIdDic[readid] = 1
    savefile.close()

    # Output sam file
    if samPath[-3:] == '.gz':
        samfile = gzip.open(samPath, 'rb')
    else:
        samfile = open(samPath, 'r')
    
    savefile = gzip.open('%s.chimeric.out.sam.gz', 'wb')
    while 1:
        line = samfile.readline()
        if not line:
            break
        if line[0] == '@':
            continue
        if line.split('\t')[0] not in allReadIdDic:
            continue
        savefile.write(line)
    savefile.close()
    samfile.close()

def test_output():
    from LoadCandidates import test_loadFusionCandidates
    candidateDic = test_loadFusionCandidates()

    from DedupReads import test_dedup1, test_dedup2
    junctionDedupReadDic = test_dedup1()
    spanningDedupReadDic = test_dedup2()

    samPath = '../testdata/Chimeric.out.sam.gz'

    prefix  = '../testdata/testresult'

    output(candidateDic, junctionDedupReadDic, spanningDedupReadDic, samPath, prefix)

if __name__ == '__main__':
    test_output()
