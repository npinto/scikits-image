from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

import numpy

ext_modules=[
    Extension("fbcorr_cython", ["fbcorr_cython.pyx"],
              include_dirs = [numpy.get_include(),'.'],
              libraries=['cblas'],
              extra_compile_args = \
              ["-O3", "-Wall",
               "-pthread",
               "-fopenmp",
               #"-ffast-math",
               #"-funroll-all-loops",
               "-msse2",
               "-msse3",
               "-msse4",
               #"-fomit-frame-pointer",
               "-march=native",
               "-mtune=native",
               "-ftree-vectorize",
               "-ftree-vectorizer-verbose=2",
               #"-fwrapv",
              ],
              ),
]

setup(
  cmdclass = {'build_ext': build_ext},
  ext_modules = ext_modules,
)
