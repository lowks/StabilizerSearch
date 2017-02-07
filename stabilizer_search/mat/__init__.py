"""Module to hold useful matrices"""

from math import exp as cexp
from math import pi, sqrt

import numpy as np


__all__=['qeye', 'X', 'Y', 'Z', 'S', 'H', 'T']


def qeye(n):
    return np.eye(n, dtype=np.complex_)


X = np.array([[0,1], [1,0]], dtype=np.complex_)


Y = np.array([[0,-1j], [1j,0]], dtype=np.complex_)


Z = np.array([[1,0], [0,-1]], dtype=np.complex_)


H = (1/sqrt(2.))*np.array([[1, 1],[1, -1]], dtype=np.complex_)


S = np.array([[1, 0], [0, 1j]], dtype=np.complex_)


T = np.array([[1, 0], [0, cexp(1j*pi/4)]], dtype=np.complex_)