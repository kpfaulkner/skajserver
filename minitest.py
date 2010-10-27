#!/usr/bin/env python

import MiniDict
import sys
import time



d = MiniDict.MiniDict( int( sys.argv[1] )  )

start = time.time()

for i in xrange( int( sys.argv[2] ) ):
  #d.set( i, i )
  d[i] = i

end = time.time()

print "took", end-start

print d.get('a', 'ddd')
d['a'] = 123

print d.get('a', 'ddd')
print d['a']


