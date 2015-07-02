#!/usr/bin/env python

def dedup(chemReadDic, readKeyDic):
    '''    In:
    dedup(chemReadDic, readKeyDic)
    Out:
    {9:{'HWI-ST1347:50:C1D0UACXX:8:1206:5976:79011': 1, 'HWI-ST1347:50:C1D0UACXX:8:1315:6627:4092': 1, 'HWI-ST1347:50:C1D0UACXX:8:2215:11770:26353': 1, 'HWI-ST1347:50:C1D0UACXX:8:1316:7944:26265': 0, 'HWI-ST1347:50:C1D0UACXX:8:2112:8264:50480': 1, 'HWI-ST1347:50:C1D0UACXX:8:1315:8322:7553': 1, 'HWI-ST1347:50:C1D0UACXX:8:1215:9746:58249': 0, 'HWI-ST1347:50:C1D0UACXX:8:1209:13068:19281': 1, 'HWI-ST1347:50:C1D0UACXX:8:1215:9137:88681': 1, 'HWI-ST1347:50:C1D0UACXX:8:1215:6263:47832': 1, 'HWI-ST1347:50:C1D0UACXX:8:1316:9077:6415': 1, 'HWI-ST1347:50:C1D0UACXX:8:1107:19085:27860': 1, 'HWI-ST1347:50:C1D0UACXX:8:1207:11734:63567': 1, 'HWI-ST1347:50:C1D0UACXX:8:2106:3798:33225': 1, 'HWI-ST1347:50:C1D0UACXX:8:1209:15836:88457': 1, 'HWI-ST1347:50:C1D0UACXX:8:2205:8292:67281': 1, 'HWI-ST1347:50:C1D0UACXX:8:2212:9389:45464': 1, 'HWI-ST1347:50:C1D0UACXX:8:1309:14076:41658': 1, 'HWI-ST1347:50:C1D0UACXX:8:1209:2880:54510': 1, 'HWI-ST1347:50:C1D0UACXX:8:1305:4772:30591': 1},...}
    '''
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

