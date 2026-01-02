"""
Geometric transformations for hull meshes.
"""

import numpy as np


def rotate_about_x(vertices, angle_rad):
    """
    Rotate vertices about the x-axis by angle_rad.

    Parameters
    ----------
    vertices : ndarray (N, 3)
    angle_rad : float
        Heel angle in radians (positive = starboard heel)

    Returns
    -------
    vertices_rot : ndarray (N, 3)
    """

    c = np.cos(angle_rad)
    s = np.sin(angle_rad)

    R = np.array([
        [1.0,  0.0,  0.0],
        [0.0,   c,  -s ],
        [0.0,   s,   c ]
    ])

    return vertices @ R.T
