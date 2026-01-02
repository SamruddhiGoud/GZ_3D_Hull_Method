import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401


def set_equal_aspect_3d(ax, X, Y, Z):
    """
    Set equal aspect ratio for a 3D plot.
    """
    max_range = np.array([
        X.max() - X.min(),
        Y.max() - Y.min(),
        Z.max() - Z.min()
    ]).max() / 2.0

    mid_x = (X.max() + X.min()) * 0.5
    mid_y = (Y.max() + Y.min()) * 0.5
    mid_z = (Z.max() + Z.min()) * 0.5

    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(mid_z - max_range, mid_z + max_range)


def plot_submerged_hull_and_B(vertices, Bc, title=None):
    """
    Plot submerged hull vertices and buoyancy centroid
    with correct scaling and view.
    """

    fig = plt.figure(figsize=(8, 7))
    ax = fig.add_subplot(111, projection='3d')

    # Hull points
    ax.scatter(
        vertices[:, 0],
        vertices[:, 1],
        vertices[:, 2],
        s=3,
        alpha=0.35
    )

    # Buoyancy center
    ax.scatter(
        Bc[0], Bc[1], Bc[2],
        color='red',
        s=120,
        label='Buoyancy Center B'
    )

    ax.set_xlabel('x (longitudinal)')
    ax.set_ylabel('y (transverse)')
    ax.set_zlabel('z (vertical)')

    # Force equal scaling
    set_equal_aspect_3d(
        ax,
        vertices[:, 0],
        vertices[:, 1],
        vertices[:, 2]
    )

    # Camera angle that clearly shows heel
    ax.view_init(elev=20, azim=120)

    if title:
        ax.set_title(title)

    ax.legend()
    plt.tight_layout()
    plt.show()
