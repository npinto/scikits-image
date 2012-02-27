import numpy as np

from lnorm import lnorm
from fbcorr import fbcorr
from lpool import lpool

from pythor3.operation import fbcorr as pt3fbcorr
from pythor3.operation import lpool as pt3lpool
from pythor3.operation import lnorm as pt3lnorm

nfs = [64, 128, 256]
nb = (9, 9)
fbs = []
fbd = 1

for nf in nfs:
    fbshape = (nf,) + nb + (fbd,)
    print 'generating', fbshape, 'filterbank'
    fb = np.random.randn(*fbshape).astype('f')
    fbs += [fb]
    fbd = nf

def pt3slm(arr_in):

    assert arr_in.ndim == 3
    inh, inw, ind = arr_in.shape

    for fb in fbs:
    #for nf in nfs:
        #fbshape = (nf,) + nb + (arr_in.shape[-1],)
        #fb1 = np.random.randn(*fbshape).astype('f')
        n1 = pt3lnorm(arr_in, inker_shape=nb, outker_shape=nb, threshold=1.0,
                      plugin='cthor', plugin_kwargs=dict(variant='sse:tbb'))
        f1 = pt3fbcorr(n1, fb,
                       plugin='cthor', plugin_kwargs=dict(variant='sse:tbb'))
        p1 = pt3lpool(f1, ker_shape=nb, order=2, stride=2,
                      plugin='cthor', plugin_kwargs=dict(variant='sse:tbb'))
        arr_in = p1

    return p1

def slm(arr_in):

    assert arr_in.ndim == 3
    inh, inw, ind = arr_in.shape

    for fb in fbs:
        n1 = lnorm(arr_in, inker_shape=nb, threshold=1.0)
        f1 = fbcorr(n1, fb)
        p1 = lpool(f1, ker_shape=nb, order=2, stride=2)
        arr_in = p1

    return p1

def main():

    import sys
    which = sys.argv[1]

    a = np.random.randn(200, 200, 1).astype('f')

    import time
    N = 10
    start = time.time()
    for i in xrange(N):
        if which == 'cthor':
            out = pt3slm(a)
        elif which == 'new':
            out = slm(a)
        else:
            raise NotImplementedError()
        print out.shape
    end = time.time()
    print N / (end - start)

if __name__ == '__main__':
    main()
