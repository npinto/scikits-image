import numpy as np

from scipy.ndimage import correlate1d as ndicorr1d
from scipy import signal

def lsum_corr1d(arr_in, ker_shape, axis):
    ker = np.ones((ker_shape), dtype=arr_in.dtype)
    out = ndicorr1d(arr_in, ker, axis=axis)
    return out

def lsum(arr_in, lsum_shape, mode='valid'):
    """XXX: better docstring
    output basically equivalent to:
    from scipy import signal
    signal.correlate(arr_in, np.ones(lsum_shape, mode)
    """

    if mode != 'valid':
        raise NotImplementedError("mode has to be 'valid'")

    lsum_shape_len = len(lsum_shape)
    assert arr_in.ndim == lsum_shape_len

    ## harcoded heuristic: if all elements of lsum_shape are small, use
    ## signal.correlate instead
    if max(lsum_shape) <= 7:
        return signal.correlate(arr_in,
                                np.ones(lsum_shape, dtype=arr_in.dtype),
                                mode='valid')

    out = arr_in
    for axis in np.argsort(-np.array(lsum_shape)):
        # determine lsum_shape element 'lse'
        lse = lsum_shape[axis]

        # -- computer 'valid' boundaries
        left = int(round((lse-1) / 2.0))
        if lse % 2 == 1:
            right = -left
        else:
            right = -left + 1

        left = left if left != 0 else None
        right = right if right != 0 else None

        # -- compute 'same' 1d correlation with vector full of ones
        out = lsum_corr1d(out, lse, axis=axis)

        # -- compute appropriate slice for 'valid' domain
        idx = [slice(None, None, None) for _ in xrange(lsum_shape_len)]
        idx[axis] = slice(left, right, None)

        out = out[idx]

    return out
