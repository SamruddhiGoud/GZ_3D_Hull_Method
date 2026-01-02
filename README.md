## Phase 2 – 3D Hull Method

This project implements a research-grade 3D geometry-based ship stability solver.

Capabilities:
- Parametric Wigley hull
- True 3D hydrostatics
- KN and GZ computation via buoyancy centroid
- Hull visualization at arbitrary heel angle

Executables:
- main.py → Computes and plots GZ curve
- visualize_hull.py → Visualizes submerged hull and buoyancy at a given heel

Model Assumptions and Limitations:
  This Phase 2 implementation computes righting arms using a fixed-draft, fixed-waterplane assumption.
  For each heel angle, the hull geometry is rotated and clipped at a constant draft, and the buoyancy centroid is computed directly from the submerged volume.
  As a result:
  No force–moment equilibrium is solved
  Draft and trim are not updated with heel
  Free-surface effects are not modeled
  Deck-edge immersion is not handled dynamically
  For simple hulls (e.g. rectangular box), the GZ curve is valid only up to moderate heel angles.
  Beyond a critical heel (e.g. deck-edge immersion), the submerged geometry changes topology and the fixed-draft assumption breaks down, leading to non-physical behavior.
  This limitation is intentional and reflects the scope of Phase 2.
  Resolving these effects requires an iterative equilibrium solver, which is planned for later phases.
