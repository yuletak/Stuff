#!/usr/bin/env /usr/local/bin/python2.7

import sys
from random import randint as randint

argv = sys.argv

try:
    length = int(argv[1])
    maxVal = int(argv[2])
    target = int(argv[3])

except IndexError:
    print "Invalid number of arguments"
    raise
except ValueError:
    print "Invalid values"
    raise

mylist = []

for i in range(length):
    mylist.append(randint(0, maxVal)
    print 'mylist[{0}]:  {1}'.format(i, mylist[i])

start = 0
end = length-1

if target == mylist[end]:
    print 'index found:  {0}'.format(end)
elif target == mylist[start]:
    print 'index found:  {0}'.format(start)
elif target > mylist[end] or target < mylist[start]:
    print 'target cannot be found'
else:    
    while start < end:
        i = (end - start)/2 + start
        print 'start:  {0}  end:  {1}  index:  {2}'.format(start, end, i)
        if target == mylist[i]:
            print 'index found:  {0}'.format(i)
            break
        elif target > mylist[i]:
            start = i
        elif target < mylist[i]:
            end = i

