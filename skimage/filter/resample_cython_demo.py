import numpy as np
import scipy as sp

#import pyximport; pyximport.install()
import resample_cython
import pylab as pl

l = sp.misc.lena()[::2, ::2]/1.
l.shape = l.shape + (1,)
l = l.astype('float32')
#a = np.random.randn(5, 3, 4).astype('float32')
l = np.tile(l, 96)

#r = resample_cython.upsample_cython(a, (6, 4, 4))
#print r
import time
N = 10
start = time.time()
for i in xrange(N):
    out = np.empty((1024, 1024, l.shape[-1]), dtype='float32')
    resample_cython.upsample_cython(l, out)
    print out.shape
end = time.time()
print N / (end - start)

pl.matshow(out[:,:,-1])
pl.show()

