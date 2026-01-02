import numpy as np

from geometry.surface import sample_wigley_surface
from geometry.mesh import triangulate_surface, mirror_mesh, close_deck, close_end
from geometry.transform import rotate_about_x
from hydrostatics.clip import clip_mesh_at_draft
from hydrostatics.volume_centroid import volume_and_centroid
from plotting.visualize import plot_submerged_hull_and_B

# Parameters
L, B, T = 100, 20, 10
draft = 5.0
theta_deg = 10.0
theta = np.deg2rad(theta_deg)

# Build hull
X, Y, Z = sample_wigley_surface(L, B, T, 31, 31)
v, f = triangulate_surface(X, Y, Z)
v, f = mirror_mesh(v, f)
v, f = close_deck(v, f)
v, f = close_end(v, f, -L/2)
v, f = close_end(v, f, +L/2)

# Rotate + clip
v_rot = rotate_about_x(v, theta)
v_sub, f_sub = clip_mesh_at_draft(v_rot, f, draft)

# Hydrostatics
V, Bc = volume_and_centroid(v_sub, f_sub)

print("Volume:", V)
print("Buoyancy center:", Bc)

# Plot
plot_submerged_hull_and_B(
    v_sub,
    Bc,
    title=f"Submerged hull at {theta_deg}° heel"
)
