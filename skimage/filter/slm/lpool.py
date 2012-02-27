import numpy as np
import numexpr as ne
from skimage.util.shape import view_as_windows


def lpool(arr_in, ker_shape=(3, 3), order=1, stride=1):

    assert arr_in.ndim == 3
    assert len(ker_shape) == 2

    order = np.float32(order)
    stride = np.int(stride)

    xp = arr_in ** order
    win_shape = ker_shape + (1,)
    xpr = view_as_windows(xp, win_shape)[::stride, ::stride]
    xprm = xpr.reshape(xpr.shape[:3] + (-1,))
    #xprms = whatever.reduction.sum(xprm, axis=-1)
    xprms = xprm.sum(-1)
    arr_out = xprms ** (1.0 / order)

    return arr_out


try:
    lpool = profile(lpool)
except NameError:
    pass


def main():

    a = np.random.randn(200, 200, 32).astype('f')

    N = 10

    import time

    start = time.time()
    for i in xrange(N):
        r = lpool(a, order=2)
    end = time.time()
    print N / (end - start)

if __name__ == '__main__':
    main()
