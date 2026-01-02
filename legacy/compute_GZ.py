import numpy as np
import matplotlib.pyplot as plt

from geometry.surface import sample_wigley_surface
from geometry.mesh import triangulate_surface, mirror_mesh, close_deck, close_end
from geometry.transform import rotate_about_x
from hydrostatics.clip import clip_mesh_at_draft
from hydrostatics.volume_centroid import volume_and_centroid

# ----------------------------
# Hull & loading parameters
# ----------------------------
L, B, T = 100.0, 20.0, 10.0
draft = 6.0
KG = 2
.0  # try changing this

# ----------------------------
# Build full hull (once)
# ----------------------------
# Higher surface resolution for smoother hydrostatics
NX = 61
NZ = 61

X, Y, Z = sample_wigley_surface(L, B, T, NX, NZ)

v, f = triangulate_surface(X, Y, Z)
v, f = mirror_mesh(v, f)
v, f = close_deck(v, f)
v, f = close_end(v, f, -L/2)
v, f = close_end(v, f, +L/2)

# ----------------------------
# KN computation
# ----------------------------

# NOTE:
# KN and GZ smoothness depend on mesh resolution and angle step.
# Any residual jitter is numerical, not physical.

# Finer heel angle sampling (1 degree steps)
angles = np.linspace(0, 30, 31)

KN_vals = []

for a in angles:
    theta = np.deg2rad(a)
    v_rot = rotate_about_x(v, theta)
    v_sub, f_sub = clip_mesh_at_draft(v_rot, f, draft)
    _, Bc = volume_and_centroid(v_sub, f_sub)
    KN_vals.append(abs(Bc[1]))

# ----------------------------
# GZ computation
# ----------------------------
GZ_vals = []

for a, kn in zip(angles, KN_vals):
    theta = np.deg2rad(a)
    gz = kn - KG * np.sin(theta)
    GZ_vals.append(gz)

# ----------------------------
# Print results
# ----------------------------
print("Angle (deg)   KN (m)     GZ (m)")
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
plt.title("GZ Curve (Phase 2 – 3D Hull Method)")
plt.grid(True)
plt.show()
