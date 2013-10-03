from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [Extension("Robot_Control_cy", ["Robot_Control.pyx"]),
               Extension("Occ_Map_Utilities_cy", ["Occ_Map_Utilities.pyx"]),
               Extension("TestMethod", ["TestMethod.pyx"])]

setup(
  name = 'Suite',
  cmdclass = {'build_ext': build_ext},
  ext_modules = ext_modules
)