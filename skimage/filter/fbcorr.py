import numpy as np
from skimage.util.shape import view_as_windows


def fbcorr_dot(arr_in, arr_fb, mode='valid'):
    """correlate a 3D input array `arr_in` with a "filter bank",
    i.e. a list of filters.
    """

    # -- basic requirements on inputs
    if arr_in.ndim != 3:
        raise ValueError('input array must be 3 dimensional')
    if arr_fb.ndim != 4:
        raise ValueError('filter bank must be 4 dimensional')
    if mode != 'valid':
        raise NotImplementedError()

    # -- input array and filterbank shapes
    inh, inw, ind = arr_in.shape
    fbn, fbh, fbw, fbd = arr_fb.shape

    # -- we make sure that we can perform the correlation
    if fbh > inh:
        raise ValueError('wrong height for the filters')
    if fbw > inw:
        raise ValueError('wrong width for the filters')
    if fbd != ind:
        raise ValueError('depth of filters must match '
                         'depth of input array')

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
