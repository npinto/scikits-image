import numpy as np

from lnorm import lnorm
from fbcorr import fbcorr
from lpool import lpool

def slm(arr_in):

    assert arr_in.ndim == 3
    inh, inw, ind = arr_in.shape

    #nfs = [32, 64, 128]
    nfs = [64, 128, 256]
    nb = (9, 9)

    for nf in nfs:
        fbshape = (nf,) + nb + (arr_in.shape[-1],)
        fb1 = np.random.randn(*fbshape).astype('f')
        n1 = lnorm(arr_in, inker_shape=nb, threshold=1.0)
        f1 = fbcorr(n1, fb1)
        p1 = lpool(f1, ker_shape=nb, order=2, stride=2)
        arr_in = p1

    return p1

def main():

    a = np.random.randn(200, 200, 1).astype('f')

    import time
    N = 10
    start = time.time()
    for i in xrange(N):
        out = slm(a)
        print out.shape
    end = time.time()
    print N / (end - start)

if __name__ == '__main__':
    main()
