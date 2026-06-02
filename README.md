# barytmat

A small Python library for saving and loading T-matrices in **barycentric rational form** (equivalent to the pole-expansion form), stored in a format compatible with the [daphona T-matrix database](https://arxiv.org/abs/2602.02101).

## Background

Electromagnetic scattering properties of particles are fully encoded in their T-matrix. The T-matrix varies smoothly with frequency, and its poles correspond to resonances of the scatterer. `barytmat` stores a compact pole expansion, for example computed via a matrix-valued AAA algorithm ([`diffaaable`](https://github.com/jan-david-fischbach/diffaaable)), as an HDF5 file that conforms to the `treams`/daphona data format. The expansion can then be evaluated at arbitrary frequencies without re-running the full T-matrix calculation.

The method is described in:

> J. D. Fischbach et al., *Pole-Expansion of the T-Matrix Based on a Matrix-Valued AAA-Algorithm*, arXiv:2602.18414 (2026). <https://doi.org/10.48550/arXiv.2602.18414>

## Related publications

| Resource | Reference |
|---|---|
| T-matrix database (daphona) | N. Asadova et al., arXiv:2602.02101 (2026). <https://doi.org/10.48550/arXiv.2602.02101> |
| treams T-matrix package | D. Beutel et al., *Comput. Phys. Commun.* **297**, 109076 (2024). <https://doi.org/10.1016/j.cpc.2023.109076> |
| Multiple-scattering resonances via AAA | J. D. Fischbach et al., *Adv. Theory Simul.* **8**, 2400989 (2025). <https://doi.org/10.1002/adts.202400989> |

## Installation

```bash
pip install barytmat
```

or 

```bash
uv add barytmat
```

## Usage

```python
import numpy as np
import barytmat

# Save a pole expansion to HDF5 (daphona-compatible)
# z_j: pole frequencies (complex), f_j: residues (matrix-valued), w_j: AAA weights
# T0: a treams.TMatrix instance that carries the basis/poltype/material metadata
barytmat.save_hdf5("my_particle.hdf5", z_j, f_j, w_j, T0,
                   description="Gold nanosphere, r=50 nm")

# Load and evaluate at arbitrary frequencies
T = barytmat.load_hdf5("my_particle.hdf5")
Ts = T(k0=np.linspace(0.9e7, 1.1e7, 50))  # array of frequencies
```

The saved file is a valid daphona/treams HDF5 file. The barycentric weights needed to reconstruct the rational approximation are stored in the file's `description` attribute so that no sidecar files are required.

## Dependencies

- [`treams`](https://github.com/tfp-photonics/treams) — T-matrix representation and HDF5 I/O
- [`diffaaable`](https://github.com/jan-david-fischbach/diffaaable) — differentiable matrix-valued AAA algorithm
- `h5py`, `numpy`