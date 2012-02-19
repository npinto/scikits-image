import numpy as np
from skimage.util.shape import view_as_windows


def fbcorr_dot(arr_in, arr_fb, mode='valid',
               mem_limit=1024):
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

    # -- item size in bytes
    itemsize = arr_in.itemsize

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

    # -- reshape `arr_fb` so as to unroll the last three
    #    dimensions in a way that matches the unrolling above
    arr_fb = arr_fb.transpose((0, 3, 1, 2))
    arr_fbm = arr_fb.reshape(fbn, -1)

    # -- actually computing the correlation with a matrix
    #    multiplication
    arr_out = np.empty(arr_inr.shape[:2] + (fbn,))
    blk_bounds = _get_block_bounds(arr_inr.shape[0],
                                   arr_inr.shape[1],
                                   fbh, fbw, fbd,
                                   itemsize,
                                   mem_limit)
    for h_min, h_max, w_min, w_max in blk_bounds:
        blk_h_size = h_max - h_min
        blk_w_size = w_max - w_min
        blk = arr_inr[h_min:h_max, w_min:w_max].reshape((blk_h_size,
                                                         blk_w_size,
                                                         -1))
        arr_out[h_min:h_max, w_min:w_max] = np.dot(blk, arr_fbm.T)

    return arr_out


def _get_block_bounds(h, w, fbh, fbw, fbd, itemsize, mem_limit):
    """mem_limit is in MB, so we multiply by 1024**2 to get the
    number of bytes
    """

    scalor = 1. * 1024**2 * mem_limit / \
            (1. * itemsize * h * w * fbh * fbw * fbd)
    scalor = np.sqrt(scalor)

    if 1. <= scalor:
        return [(0, h, 0, w)]

    blk_h = int(scalor * h)
    blk_w = int(scalor * w)

    nblk_h = h / blk_h
    nblk_w = w / blk_w

    h_start = [i * blk_h for i in xrange(nblk_h + 1)]
    h_stop = [i * blk_h for i in xrange(1, nblk_h + 1)] + [h]

    w_start = [i * blk_w for i in xrange(nblk_w + 1)]
    w_stop = [i * blk_w for i in xrange(1, nblk_w + 1)] + [w]

    blk_coords = []
    for h0, h1 in zip(h_start, h_stop):
        for w0, w1 in zip(w_start, w_stop):
            blk_coords += [(h0, h1, w0, w1)]

    return blk_coords
