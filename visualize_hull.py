"""
Phase 2 – Hull Geometry Visualization
Visualize submerged hull and buoyancy centroid at a given heel angle.

Purpose:
- Geometry inspection
- Debugging
- Intuition building

NOT a stability solver.
"""

import numpy as np

from geometry.surface import sample_wigley_surface
from geometry.mesh import triangulate_surface, mirror_mesh, close_deck, close_end
from geometry.transform import rotate_about_x
from hydrostatics.clip import clip_mesh_at_draft
from hydrostatics.volume_centroid import volume_and_centroid
from plotting.visualize import plot_submerged_hull_and_B


def main():
    print("\n=== Hull Visualization (Phase 2) ===")

    heel_deg = float(input("Enter heel angle (deg): "))
    draft = float(input("Enter draft (m): "))

    # ----------------------------
    # Hull parameters (Wigley)
    # ----------------------------
    L, B, T = 100.0, 20.0, 10.0
    NX, NZ = 61, 61

    # ----------------------------
    # Build full hull
    # ----------------------------
    X, Y, Z = sample_wigley_surface(L, B, T, NX, NZ)
    v, f = triangulate_surface(X, Y, Z)
    v, f = mirror_mesh(v, f)
    v, f = close_deck(v, f)
    v, f = close_end(v, f, -L / 2)
    v, f = close_end(v, f, +L / 2)

    # ----------------------------
    # Rotate + clip
    # ----------------------------
    theta = np.deg2rad(heel_deg)
    v_rot = rotate_about_x(v, theta)
    v_sub, f_sub = clip_mesh_at_draft(v_rot, f, draft)

    # ----------------------------
    # Buoyancy centroid
    # ----------------------------
    _, Bc = volume_and_centroid(v_sub, f_sub)

    print(f"\nBuoyancy centroid at {heel_deg}° heel:")
    print(Bc)

    # ----------------------------
    # Visualization
    # ----------------------------
    plot_submerged_hull_and_B(
        v_sub,
        Bc,
        title=f"Submerged hull at {heel_deg}° heel"
    )


if __name__ == "__main__":
    main()
