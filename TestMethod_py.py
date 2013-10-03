#!/usr/bin/env python
__author__ = 'Theo'
__copyright__ = "Copyright 2013, theo.is-a-geek.com"
__credits__ = ["Theo Deyle"]
__license__ = "MIT"
__version__ = "0.01"
__maintainer__ = "Theo Deyle"
__email__ = "theo.deyle@gmail.com"
__status__ = "Hashing Out"

"""
Need to create a method to calculate end point of scan line based on robot position, and map.
"""

from math import sin, cos, radians

def findXPrime(loc, length, angle):

    return loc + (cos(radians(angle)) * length)

def findYPrime(loc, length, angle):

    return loc + (sin(radians(angle)) * length)