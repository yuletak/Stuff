#!/usr/bin/env /usr/local/bin/python2.7

import sys
from random import randint as randint

argv = sys.argv

mylist = []

if len(argv) == 1:
    print 'Unsorted mylist:'
    mylist = [1,0,0,0,0]
    for i in range(len(mylist)):
        print 'mylist[{0}]:  {1}'.format(i, mylist[i])
elif len(argv) == 2:
    try:
        length = int(argv[1])
        print 'Unsorted mylist:'
        for i in range(length):
            mylist.append(length-i)
            print 'mylist[{0}]:  {1}'.format(i, mylist[i])
    except ValueError:
        print "Invalid value"
        raise
elif len(argv) == 3:
    try:
        length = int(argv[1])
        maxVal = int(argv[2])
        print 'Unsorted mylist:'
        for i in range(length):
            mylist.append(randint(0, maxVal))
            print 'mylist[{0}]:  {1}'.format(i, mylist[i])
    except ValueError:
        print "Invalid values"
        raise

length = len(mylist)
end = length-1
sIndex = 0

while sIndex < end:
    sVal = mylist[sIndex]
    smaller = sIndex
    for i in range(sIndex, length):
        if mylist[i] < sVal:
            smaller = i
            sVal = mylist[i]
#    print 'smaller: {0} | sVal: {1} | mylist[sIndex]: {2} | sIndex: {3}'.format(smaller, sVal, mylist[sIndex], sIndex)
    if sIndex < smaller:
#        print 'smaller:  {0}  sIndex:  {1}'.format(smaller, sIndex)
        mylist[sIndex], mylist[smaller] = mylist[smaller], mylist[sIndex]
    sIndex += 1

print 'Sorted mylist:'
for i in range(length):
    print 'mylist[{0}]:  {1}'.format(i, mylist[i])

