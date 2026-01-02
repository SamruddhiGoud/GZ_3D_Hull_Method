"""
Triangulation utilities for hull surface meshes.
"""

import numpy as np


def triangulate_surface(X, Y, Z):
    """
    Triangulate a structured surface grid into vertices and faces.

    Parameters
    ----------
    X, Y, Z : ndarray
        Arrays of shape (Nz, Nx) representing surface points

    Returns
    -------
    vertices : ndarray
        Array of shape (N, 3)
    faces : ndarray
        Array of shape (M, 3), indices into vertices
    """

    Nz, Nx = X.shape

    # --- Flatten vertices ---
    vertices = np.column_stack([
        X.ravel(),
        Y.ravel(),
        Z.ravel()
    ])

    faces = []

    def vid(i, j):
        """Vertex index helper"""
        return i * Nx + j

    # --- Create triangles ---
    for i in range(Nz - 1):
        for j in range(Nx - 1):
            v0 = vid(i, j)
            v1 = vid(i, j + 1)
            v2 = vid(i + 1, j + 1)
            v3 = vid(i + 1, j)

            # Triangle 1
            faces.append([v0, v1, v2])

            # Triangle 2
            faces.append([v0, v2, v3])

    return np.array(vertices), np.array(faces)
def mirror_mesh(vertices, faces):
    """
    Mirror a half-hull mesh about the centerplane (y = 0)
    and fix face orientation.

    Parameters
    ----------
    vertices : ndarray (N, 3)
    faces : ndarray (M, 3)

    Returns
    -------
    vertices_full : ndarray
    faces_full : ndarray
    """

    # --- Mirror vertices ---
    vertices_mirror = vertices.copy()
    vertices_mirror[:, 1] *= -1  # y -> -y

    # --- Offset for new vertex indices ---
    offset = len(vertices)

    # --- Reverse face orientation for mirrored side ---
    faces_mirror = []
    for f in faces:
        faces_mirror.append([
            f[0] + offset,
            f[2] + offset,
            f[1] + offset
        ])

    # --- Combine ---
    vertices_full = np.vstack([vertices, vertices_mirror])
    faces_full = np.vstack([faces, np.array(faces_mirror)])

    return vertices_full, faces_full

def close_deck(vertices, faces):
    """
    Close the hull at the deck plane (z = 0).
    Assumes hull is symmetric and already mirrored.
    """

    z_tol = 1e-6

    # Find deck boundary vertices
    deck_indices = np.where(abs(vertices[:, 2]) < z_tol)[0]

    # Sort deck vertices along x, then y
    deck_vertices = vertices[deck_indices]
    order = np.lexsort((deck_vertices[:, 1], deck_vertices[:, 0]))
    deck_indices = deck_indices[order]

    # Create center point
    center = deck_vertices.mean(axis=0)
    center[2] = 0.0

    center_index = len(vertices)
    vertices = np.vstack([vertices, center])

    new_faces = []

    for i in range(len(deck_indices) - 1):
        new_faces.append([
            deck_indices[i],
            deck_indices[i + 1],
            center_index
        ])

    faces = np.vstack([faces, np.array(new_faces)])
    return vertices, faces

def close_end(vertices, faces, x_value):
    """
    Close bow or stern using a triangle fan.
    x_value = +L/2 (stern) or -L/2 (bow)
    """

    x_tol = 1e-6

    end_indices = np.where(abs(vertices[:, 0] - x_value) < x_tol)[0]
    end_vertices = vertices[end_indices]

    # Sort by z, then y
    order = np.lexsort((end_vertices[:, 1], end_vertices[:, 2]))
    end_indices = end_indices[order]

    center = end_vertices.mean(axis=0)
    center[0] = x_value

    center_index = len(vertices)
    vertices = np.vstack([vertices, center])

    new_faces = []

    for i in range(len(end_indices) - 1):
        new_faces.append([
            end_indices[i],
            center_index,
            end_indices[i + 1]
        ])

    faces = np.vstack([faces, np.array(new_faces)])
    return vertices, faces
