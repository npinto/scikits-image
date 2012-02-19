import numpy as np
from skimage.util.shape import view_as_windows

def fbcorr(arr_in, arr_fb, mode='valid'):

    # XXX

    # -- we use `view_as_windows` to be able to extract patches
    #    from the input array of the same shape as the filters
    arr_inr = view_as_windows(arr_in, (fbh, fbw, 1))
    arr_inrm = arr_inr.reshape(arr_inr.shape[:2] + (-1,))

    # -- reshape arr_fb
    arr_fb = arr_fb.transpose((0, 3, 1, 2))
    arr_fbm = arr_fb.reshape(fbn, -1)

    # -- actually computing the correlation with a matrix
    #    multiplication
    arr_out = np.dot(arr_inrm, arr_fbm.T)
    arr_out = arr_out.reshape(arr_inr.shape[:2] + (-1,))

    return arr_out
