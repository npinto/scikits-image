import numpy as np
from skimage.util.shape import view_as_windows
#from ..util.shape import view_as_windows
#from pythor3.wildwest.rolling_view import rolling_view

def fbcorr(arr_in, arr_fb, mode='valid'):

    assert arr_in.ndim == 3
    assert arr_fb.ndim == 4
    if mode != 'valid':
        raise NotImplementedError()

    inh, inw, ind = arr_in.shape
    fbn, fbh, fbw, fbd = arr_fb.shape

    assert fbn > 1
    assert fbh <= inh
    assert fbw <= inw
    assert fbd == ind

    # -- reshape arr_in
    arr_inr = view_as_windows(arr_in, (fbh, fbw, 1))
    #arr_inr = rolling_view(arr_in, (fbh, fbw))
    outh, outw = arr_inr.shape[:2]
    arr_inrm = arr_inr.reshape(outh * outw, -1)

    # -- reshape arr_fb
    arr_fb = arr_fb.transpose((0, 3, 1, 2))
    arr_fbm = arr_fb.reshape(fbn, -1)

    # -- correlate !
    #import IPython; ipshell = IPython.embed; ipshell(banner1='ipshell')
    print 'shape', arr_inrm.shape, arr_fbm.T.shape
    arr_out = np.dot(arr_inrm, arr_fbm.T)
    arr_out = arr_out.reshape(outh, outw, -1)

    return arr_out


try:
    fbcorr = profile(fbcorr)
except NameError:
    pass


def main():
    arr_in = np.random.randn(128, 128, 128).astype('f')
    fb = np.random.randn(256, 5, 5, 128).astype('f')

    import time
    N = 10
    start = time.time()
    for i in xrange(N):
        print i
        print fbcorr(arr_in, fb).shape
    end = time.time()
    fps = N / (end - start)
    print fps
    tim = 1. / fps
    print tim

    flops = np.cumprod(arr_in.shape[:2] + fb.shape)[-1] * 2
    gflops = (flops / 1e9)
    print 'gflops / sec', 1. * gflops / tim

if __name__ == '__main__':
    main()
