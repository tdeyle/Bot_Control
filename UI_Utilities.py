#!/usr/bin/env python
__author__ = 'Theo'
__copyright__ = "Copyright 2013, theo.is-a-geek.com"
__credits__ = ["Theo Deyle"]
__license__ = "MIT"
__version__ = "0.01"
__maintainer__ = "Theo Deyle"
__email__ = "theo.deyle@gmail.com"
__status__ = "Hashing Out"

from math import sin, cos

class Utils2D:

    # --------
    # rotate:
    #   returns point rotated around base_point for given angle

    # TODO: Make this more readable

    @staticmethod
    def rotate(point, base_point, angle):
        x = point[0]
        y = point[1]
        # translate base point to 0, 0
        p = (x - base_point[0], y - base_point[1])
        # rotate around origin:
        x = p[0] * cos(angle) - p[1] * sin(angle)
        y = p[0] * sin(angle) + p[1] * cos(angle)
        # translate back to base point
        p = (x + base_point[0], y + base_point[1])
        return p

    # --------
    # get_angle:
    #   returns orientation of the vector defined by from_point and to_point

    @staticmethod
    def get_angle(from_point, to_point):
        from_x = from_point[0]
        from_y = from_point[1]
        to_x = to_point[0]
        to_y = to_point[1]
        return atan2(to_y - from_y, to_x - from_x)

