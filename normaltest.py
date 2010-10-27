#!/usr/bin/env python

import lrudict
import sys
import time

d = {}

start = time.time()

for i in xrange( int( sys.argv[1] ) ):
  d[i] = i

end = time.time()

print "took", end-start
