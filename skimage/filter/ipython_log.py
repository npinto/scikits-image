import numpy as np
import scipy as sp

#import pyximport; pyximport.install()
import resample_cython
import pylab as pl

l = sp.misc.lena()/1.
l.shape = l.shape + (1,)
l = l.astype('float32')
a = np.random.randn(5, 3, 4).astype('float32')

#r = resample_cython.upsample_cython(a, (6, 4, 4))
#print r
out = np.empty((1024, 1024, 1), dtype='float32')
r = resample_cython.upsample_cython(l, out)

pl.matshow(r[:,:,0])
pl.show()

