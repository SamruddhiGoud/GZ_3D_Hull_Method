"""
Analytical definition of a Wigley hull.

Coordinate system:
x : longitudinal, from -L/2 to +L/2
y : transverse (half-breadth), >= 0
z : vertical, from 0 (deck plane) to T (keel)
"""

def wigley_half_breadth(x, z, L, B, T):
    """
    Returns half-breadth y at longitudinal position x
    and vertical position z for a Wigley hull.

    Parameters
    ----------
    x : float
        Longitudinal position [-L/2, L/2]
    z : float
        Vertical position [0, T]
    L : float
        Length between perpendiculars
    B : float
        Breadth
    T : float
        Draft

    Returns
    -------
    y : float
        Half-breadth (>= 0)
    """

    # Outside hull domain
    if abs(x) > L / 2 or z < 0 or z > T:
        return 0.0

    x_term = 1.0 - (2.0 * x / L) ** 2
    z_term = 1.0 - (z / T) ** 2

    y = (B / 2.0) * x_term * z_term

    # Numerical safety
    return max(y, 0.0)
