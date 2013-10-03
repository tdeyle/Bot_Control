from libc.math cimport M_PI, sin, cos

#cdef extern from "math.h":
#    double sin(double x)
#    double cos(double x)

def findXPrime(loc, length, angle):
    return cFindXPrime(loc, length, angle)

def findYPrime(loc, length, angle):
    return cFindYPrime(loc, length, angle)

cdef double cFindXPrime(double loc, double length, double angle):
    cdef double degrees = angle * M_PI / 180.0

    return loc + (cos(degrees) * length)

cdef double cFindYPrime(double loc, double length, double angle):
    cdef double degrees = angle * M_PI / 180.0

    return loc + (sin(degrees) * length)

