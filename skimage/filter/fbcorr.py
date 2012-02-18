import numpy as np
#from skimage.util.shape import view_as_windows
from ..util.shape import view_as_windows

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
    arr_inrm = arr_inr.reshape(arr_inr.shape[:2] + (-1,))

    # -- reshape arr_fb
    arr_fb = arr_fb.transpose((0, 3, 1, 2))
    arr_fbm = arr_fb.reshape(fbn, -1)

    # -- correlate !
    arr_out = np.dot(arr_inrm, arr_fbm.T)
    arr_out = arr_out.reshape(arr_inr.shape[:2] + (-1,))

    return arr_out


#def main():
    #arr_in = np.random.randn(5, 5, 2)
    #fb = np.random.randn(4, 3, 3, 2)

    #print fbcorr_dot(arr_in, fb).shape

#if __name__ == '__main__':
    #main()
