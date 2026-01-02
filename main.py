"""
Phase 2 – 3D Hull Method
Main executable for GZ curve computation using a parametric Wigley hull.

Author: Samruddhi Goud
Purpose: Research-grade 3D hydrostatics (NOT certification level)
"""

import numpy as np
import matplotlib.pyplot as plt

from geometry.surface import sample_wigley_surface
from geometry.mesh import triangulate_surface, mirror_mesh, close_deck, close_end
from geometry.transform import rotate_about_x
from hydrostatics.clip import clip_mesh_at_draft
from hydrostatics.volume_centroid import volume_and_centroid


def compute_GZ_curve(KG, draft):
    # ----------------------------
    # Hull parameters (Wigley)
    # ----------------------------
    L, B, T = 100.0, 20.0, 10.0
    NX, NZ = 61, 61

    # ----------------------------
    # Build full hull once
    # ----------------------------
    X, Y, Z = sample_wigley_surface(L, B, T, NX, NZ)
    v, f = triangulate_surface(X, Y, Z)
    v, f = mirror_mesh(v, f)
    v, f = close_deck(v, f)
    v, f = close_end(v, f, -L / 2)
    v, f = close_end(v, f, +L / 2)

    # ----------------------------
    # Heel angles
    # ----------------------------
    angles = np.linspace(0, 30, 31)  # degrees
    KN_vals = []
    GZ_vals = []

    # ----------------------------
    # Hydrostatics loop
    # ----------------------------
    for a in angles:
        theta = np.deg2rad(a)

        v_rot = rotate_about_x(v, theta)
        v_sub, f_sub = clip_mesh_at_draft(v_rot, f, draft)

        _, Bc = volume_and_centroid(v_sub, f_sub)
        KN = abs(Bc[1])

        GZ = KN - KG * np.sin(theta)

        KN_vals.append(KN)
        GZ_vals.append(GZ)

    return angles, KN_vals, GZ_vals


def main():
    print("\n=== Phase 2: 3D Hull GZ Computation ===")

    KG = float(input("Enter KG (m): "))
    draft = float(input("Enter draft (m): "))

    angles, KN_vals, GZ_vals = compute_GZ_curve(KG, draft)

    print("\nAngle (deg)   KN (m)     GZ (m)")
    for a, kn, gz in zip(angles, KN_vals, GZ_vals):
        print(f"{a:6.1f}     {kn:7.4f}   {gz:7.4f}")

    # ----------------------------
    # Plot GZ curve
    # ----------------------------
    plt.figure()
    plt.plot(angles, GZ_vals, marker='o')
    plt.axhline(0, color='k', linestyle='--')
    plt.xlabel("Heel angle (deg)")
    plt.ylabel("GZ (m)")
    plt.title("GZ Curve – Phase 2 (3D Hull Method)")
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()
