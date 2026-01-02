"""
Mesh clipping utilities for hydrostatics.
"""
# Waterplane closure via fan triangulation.
# This introduces small centroid bias that converges with mesh refinement.
# Acceptable for Phase 2 (research-grade hydrostatics).

import numpy as np

def is_submerged(vertex, draft):
    """
    Check if a vertex is below the waterplane.
    """
    return vertex[2] >= draft

def intersect_edge_with_plane(v1, v2, draft):
    """
    Compute intersection point of an edge with horizontal plane z = draft.

    Assumes v1 and v2 lie on opposite sides of the plane.
    """

    z1 = v1[2]
    z2 = v2[2]

    # Linear interpolation factor
    t = (draft - z1) / (z2 - z1)

    return v1 + t * (v2 - v1)

def clip_mesh_at_draft(vertices, faces, draft):
    """
    Clip a closed mesh at a given draft and return submerged mesh.

    Parameters
    ----------
    vertices : ndarray (N, 3)
    faces : ndarray (M, 3)
    draft : float

    Returns
    -------
    vertices_sub : ndarray
    faces_sub : ndarray
    """

    new_vertices = []
    new_faces = []

    vertex_map = {}  # old_index -> new_index

    def get_vertex(idx):
        if idx not in vertex_map:
            vertex_map[idx] = len(new_vertices)
            new_vertices.append(vertices[idx])
        return vertex_map[idx]

    # We will also store waterplane intersection edges
    waterline_edges = []

    # --- iterate through triangles ---
    for f in faces:
        v_ids = list(f)
        verts = [vertices[i] for i in v_ids]
        submerged = [is_submerged(v, draft) for v in verts]

        n_sub = sum(submerged)

        # Case handling will go here (next step)
        if n_sub == 3:
            # fully submerged
            new_faces.append([
                get_vertex(v_ids[0]),
                get_vertex(v_ids[1]),
                get_vertex(v_ids[2])
            ])

        elif n_sub == 0:
            # fully above water → discard
            continue

        else:
            # partially submerged triangle
            sub_ids = []
            dry_ids = []

            for i in range(3):
                if submerged[i]:
                    sub_ids.append(v_ids[i])
                else:
                    dry_ids.append(v_ids[i])

            if n_sub == 1:
                # One submerged, two dry → one new triangle
                v_sub = vertices[sub_ids[0]]
                v_dry1 = vertices[dry_ids[0]]
                v_dry2 = vertices[dry_ids[1]]

                p1 = intersect_edge_with_plane(v_sub, v_dry1, draft)
                p2 = intersect_edge_with_plane(v_sub, v_dry2, draft)

                i_sub = get_vertex(sub_ids[0])

                i_p1 = len(new_vertices)
                new_vertices.append(p1)
                i_p2 = len(new_vertices)
                new_vertices.append(p2)

                new_faces.append([i_sub, i_p1, i_p2])

                waterline_edges.append((i_p1, i_p2))

            elif n_sub == 2:
                # Two submerged, one dry → two new triangles
                v_sub1 = vertices[sub_ids[0]]
                v_sub2 = vertices[sub_ids[1]]
                v_dry = vertices[dry_ids[0]]

                p1 = intersect_edge_with_plane(v_sub1, v_dry, draft)
                p2 = intersect_edge_with_plane(v_sub2, v_dry, draft)

                i_sub1 = get_vertex(sub_ids[0])
                i_sub2 = get_vertex(sub_ids[1])

                i_p1 = len(new_vertices)
                new_vertices.append(p1)
                i_p2 = len(new_vertices)
                new_vertices.append(p2)

                new_faces.append([i_sub1, i_sub2, i_p2])
                new_faces.append([i_sub1, i_p2, i_p1])

                waterline_edges.append((i_p1, i_p2))

    # ===============================
    # Close the waterplane (z = draft)
    # ===============================
    if len(waterline_edges) > 0:
        # Collect unique waterline vertex indices
        wl_indices = set()
        for e in waterline_edges:
            wl_indices.update(e)

        wl_indices = list(wl_indices)

        # Extract waterline vertices
        wl_vertices = np.array([new_vertices[i] for i in wl_indices])

        # Sort vertices around perimeter using angle in x–y plane
        xy = wl_vertices[:, :2]
        center_xy = xy.mean(axis=0)

        angles = np.arctan2(
            xy[:, 1] - center_xy[1],
            xy[:, 0] - center_xy[0]
        )

        order = np.argsort(angles)
        wl_indices = [wl_indices[i] for i in order]

        # Create center vertex on waterplane
        center = wl_vertices.mean(axis=0)
        center[2] = draft

        center_index = len(new_vertices)
        new_vertices.append(center)

        # Fan triangulation of waterplane
        for i in range(len(wl_indices)):
            i0 = wl_indices[i]
            i1 = wl_indices[(i + 1) % len(wl_indices)]

            new_faces.append([i0, i1, center_index])

    return np.array(new_vertices), np.array(new_faces)
