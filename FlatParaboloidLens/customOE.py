# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 14:06:16 2023

@author: chernir
"""

import xrt.backends.raycing.oes as roe
import numpy as np

class FlatParaboloidLens(roe.ParaboloidFlatLens):
    """Similar to ParaboloidFlatLens, where the first surface is flat
    and the second is a paraboloid."""

    def local_z2(self, x, y):
        """Determines the normal vector of OE at (x, y) position."""
        z = (x**2 + y**2) / (4 * self.focus)
        if self.zmax is not None:
            z[z > self.zmax] = self.zmax
        return z

    def local_z1(self, x, y):
        """Determines the surface of OE at (x, y) position."""
        return self.local_z(x, y)

    def local_n2(self, x, y):
        """Determines the normal vector of OE at (x, y) position. If OE is an
        asymmetric crystal, *local_n* must return 2 normals: the 1st one of the
        atomic planes and the 2nd one of the surface."""
        # just flat:
        a = -x / (2*self.focus)  # -dz/dx
        b = -y / (2*self.focus)  # -dz/dy
        if self.zmax is not None:
            z = (x**2 + y**2) / (4*self.focus)
            if isinstance(a, np.ndarray):
                a[z > self.zmax] = 0
            if isinstance(b, np.ndarray):
                b[z > self.zmax] = 0
        c = np.ones_like(x)
        norm = (a**2 + b**2 + 1)**0.5
        return [a/norm, b/norm, c/norm]

    def local_n1(self, x, y):
        return self.local_n(x, y)    