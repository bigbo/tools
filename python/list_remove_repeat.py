#/*******************************************************************************
# * Author	 : jingbo.li | work at r.
# * Email	 : ljb90@live.cn
# * Last modified : 2013-11-05 20:09
# * Filename	 :
# * Description	 :对于list的去重四种方法效率的对比. 
# * *****************************************************************************/
# -*- coding: utf-8 -*-
#!/bin/env python
from timeit import Timer

def testset():
    list1 = ['a','b','d','a','c','d','a','c','e','a','c','e']
    list2 = list(set(list1))
    return list2

def testfromkeys():
    list1 = ['a','b','d','a','c','d','a','c','e','a','c','e']
    list2 = {}.fromkeys(list1).keys()
    return list2

def testfor():
    list1 = ['a','b','d','a','c','d','a','c','e','a','c','e']
    list2 = []
    for i in list1:
        if not i in list2:
            list2.append(i)
    return list2

def testreduce():
    list1 = ['a','b','d','a','c','d','a','c','e','a','c','e'] 
    re = reduce(lambda x,y:x if y in x else x+[y],[[],]+list1)
    return re

if __name__=='__main__':
    t1=Timer("testset()","from __main__ import testset")
    t2=Timer("testfromkeys()","from __main__ import testfromkeys")
    t3=Timer("testfor()","from __main__ import testfor")
    t4=Timer("testreduce()","from __main__ import testreduce")

    print 'the set fun run time :',t1.timeit(1000000)
    print 'set three run time :',t1.repeat(3,1000000)

    print 'the fromkeys run time :',t2.timeit(1000000)
    print 'fromkeys three run time :',t2.repeat(3,1000000)

    print 'the for run time :',t3.timeit(1000000)
    print 'for three run time:',t3.repeat(3,1000000)

    print 'the reduce run time :',t4.timeit(1000000)
    print 'reduce three run time:',t4.repeat(3,1000000)

