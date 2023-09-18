from distutils.core import setup
from Cython.Build import cythonize

setup(
    name="my_array_5",
    ext_modules=cythonize("my_array.pyx")
)
