import numpy as np
from numpy.testing import assert_equal
from nose.tools import raises
from skimage.filter.fbcorr import fbcorr_dot as fbcorr


@raises(ValueError)
def test_wrong_input_array_dimension():

    arr_in = np.arange(5*5).reshape(5, 5)
    fb = np.arange(2*3*3*4).reshape(2, 3, 3, 4)
    fbcorr(arr_in, fb)


@raises(ValueError)
def test_wrong_fb_dimension():

    arr_in = np.arange(5*5*4).reshape(5, 5, 4)
    fb = np.arange(3*3*4).reshape(3, 3, 4)
    fbcorr(arr_in, fb)


@raises(ValueError)
def test_filter_height_too_large():

    arr_in = np.arange(5*5*4).reshape(5, 5, 4)
    fb = np.arange(2*6*3*4).reshape(2, 6, 3, 4)
    fbcorr(arr_in, fb)


@raises(ValueError)
def test_filter_width_too_large():

    arr_in = np.arange(5*5*4).reshape(5, 5, 4)
    fb = np.arange(2*3*6*4).reshape(2, 3, 6, 4)
    fbcorr(arr_in, fb)


@raises(ValueError)
def test_depth_mismatch():

    arr_in = np.arange(5*5*4).reshape(5, 5, 4)
    fb = np.arange(2*3*6*3).reshape(2, 3, 6, 3)
    fbcorr(arr_in, fb)


def test_all_ones():

    h, w, d = 10, 12, 4
    fn, fh, fw, fd = 2, 3, 3, 4
    arr_in = np.ones((h, w, d))
    fb = np.ones((fn, fh, fw, fd))
    res = fbcorr(arr_in, fb)
    ref = fh * fw * fd * np.ones((h - fh + 1, w - fw + 1, fn))
    assert_equal(res, ref)


def test_all_zeros():

    h, w, d = 10, 12, 4
    fn, fh, fw, fd = 2, 3, 3, 4
    arr_in = np.zeros((h, w, d))
    fb = np.ones((fn, fh, fw, fd))
    res = fbcorr(arr_in, fb)
    ref = fh * fw * fd * np.zeros((h - fh + 1, w - fw + 1, fn))
    assert_equal(res, ref)


def test_arange_along_depth():

    h, w, d = 5, 5, 4
    fn, fh, fw, fd = 2, 3, 3, 4
    _, _, arr_in = np.mgrid[0:h, 0:w, 0:d]
    fb = np.ones((fn, fh, fw, fd))
    res = fbcorr(arr_in, fb)
    ref = fh * fw * d /2 * (d - 1) * np.ones((h - fh + 1,
                                              w - fw + 1,
                                              fn))
    assert_equal(res, ref)
