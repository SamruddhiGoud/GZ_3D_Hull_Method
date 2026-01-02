"""
Geometry validation utilities.
"""

import numpy as np


def signed_volume(vertices, faces):
    """
    Compute signed volume of a closed triangular mesh.

    Parameters
    ----------
    vertices : ndarray (N, 3)
    faces : ndarray (M, 3)

    Returns
    -------
    volume : float
        Signed volume
    """

    vol = 0.0

    for f in faces:
        v0 = vertices[f[0]]
        v1 = vertices[f[1]]
        v2 = vertices[f[2]]

        vol += np.dot(v0, np.cross(v1, v2))

    return abs(vol / 6.0)

