"""
Surface sampling for Wigley hull.

Generates structured surface point grids for the half-hull.
"""

import numpy as np
from geometry.wigley import wigley_half_breadth


def sample_wigley_surface(L, B, T, Nx, Nz):
    """
    Sample the Wigley hull surface into a structured grid.

    Parameters
    ----------
    L : float
        Length between perpendiculars
    B : float
        Breadth
    T : float
        Draft
    Nx : int
        Number of points along length
    Nz : int
        Number of points along depth

    Returns
    -------
    X, Y, Z : ndarray
        Arrays of shape (Nz, Nx) representing surface points
        of the half-hull (y >= 0)
    """

    # Longitudinal and vertical coordinates
    x_vals = np.linspace(-L / 2.0, L / 2.0, Nx)
    z_vals = np.linspace(0.0, T, Nz)

    X = np.zeros((Nz, Nx))
    Y = np.zeros((Nz, Nx))
    Z = np.zeros((Nz, Nx))

    for i, z in enumerate(z_vals):
        for j, x in enumerate(x_vals):
            X[i, j] = x
            Z[i, j] = z
            Y[i, j] = wigley_half_breadth(x, z, L, B, T)

    return X, Y, Z
