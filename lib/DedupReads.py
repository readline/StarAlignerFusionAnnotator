#!/usr/bin/env python

def dedup(chemReadDic, readKeyDic):

    for chem in chemReadDic:
        readDic = chemReadDic[chem]
        bcdDic = {}
        for readid in readDic:
            bcd = readKeyDic[readid]['bcd']
            if bcd not in bcdDic:
                bcdDic[bcd] = {}
            bcdDic[bcd][readid] = readKeyDic[readid]['qlt']

        for bcd in bcdDic:
            if len(bcdDic[bcd]) == 1:
                pass
            elif len(bcdDic[bcd]) >1:
                max = 0
                maxreadid = ''
                for readid in bcdDic[bcd]:
                    if bcdDic[bcd][readid] > max:
                        max = bcdDic[bcd][readid]
                        maxreadid = readid
                for readid in bcdDic[bcd]:
                    if readid == maxreadid:
                        pass
                    else:
                        readDic[readid] = 0
        chemReadDic[chem] = readDic
    return chemReadDic

def test_dedup1():
    from LoadJunctionReadName import test_loadJunctionReadName
    chemReadDic = test_loadJunctionReadName()

    from LoadReadFromSam import test_LoadSam
    readKeyDic = test_LoadSam()

    return dedup(chemReadDic, readKeyDic)

def test_dedup2():
    from LoadSpanningReadName import test_loadSpanningReadName
    chemReadDic = test_loadSpanningReadName()

    from LoadReadFromSam import test_LoadSam
    readKeyDic = test_LoadSam()

    return dedup(chemReadDic, readKeyDic)
if __name__ == '__main__':
    print 'Test junction part...'
    chemReadDic = test_dedup1()
    print 'Test spanning part...'
    chemReadDic = test_dedup2()
    for chem in chemReadDic:
        print chem
        print chemReadDic[chem]
        raw_input()

