import treams.io
import h5py
import re
import ast
import diffaaable
import numpy as np
import textwrap

def save_hdf5(filename, z_j, f_j, w_j, T0, description="", lunit="m", **kwargs):
    """Save Barycentric Rational Representation of the T-matrix to file

    Args:
        filename (path): file to write to
        z_j (complex): pole frequencies
        f_j (complex): matrix valued residues
        w_j (complex): weights
        T0 (treams.TMatrix): reference T-matrix 
            with correct basis, poltype and embedding
    """

    tms = [treams.TMatrix(tdata, k0=k0, basis=T0.basis, poltype=T0.poltype, material=T0.material) for k0, tdata in zip(z_j, f_j)]
    with h5py.File(filename, "w") as file:
        treams.io.save_hdf5(file, tms,
            keywords = "pole-expansion, barycentric-rational",
            lunit = lunit,
            description = description + textwrap.dedent(
                f"""
                Attention: This T-matrix is in barycentric rational format. To evaluate it at arbitrary frequencies install `diffaaable` and use the following weights:
                w_j=np.{np.array_repr(w_j, precision=16, max_line_width=np.inf)}

                A small library to handle T-matrices in barycentric rational representation can be found [here](TODO)
                """
            ),
            **kwargs
        )
    

def baryT(z_j, f_j, w_j, T0):
    """Barycentric Rational Representation of the T-matrix

    Args:
        z_j (complex): pole frequencies
        f_j (complex): matrix valued residues
        w_j (complex): weights
        T0 (treams.TMatrix): reference T-matrix 
            with correct basis, poltype and embedding

    Returns:
        Callable: T as a function of z
    """
    R = diffaaable.tensor.tensor_baryrat(z_j, f_j, w_j)
    def T(k0):
        k0 = np.array(k0)
        if k0.ndim > 0:
            tmat_data = R(k0)
            return np.vectorize(treams.TMatrix, otypes=[object])(tmat_data, k0=k0, material=T0.material, basis=T0.basis, poltype=T0.poltype)
        else:
            tmat_data = R([k0])[0]
            return treams.TMatrix(tmat_data, k0=k0, material=T0.material, basis=T0.basis, poltype=T0.poltype)
    
    return T

def load_hdf5(filename, lunit="m", **kwargs):
    """Load a T-matrix in Barycentric Rational form from the given file

    Args:
        filename (path): file to load

    Returns:
        Callable: T as a function of z
    """

    with h5py.File(filename, "r") as file: 
        tmats = treams.io.load_hdf5(file, lunit=lunit, **kwargs)
        descr = file.attrs["description"]

    matches = re.findall(r"^w_j=.*$", descr, re.MULTILINE)
    assert len(matches) == 1

    k0s = [T.k0 for T in tmats]
    z_j = np.array(k0s)

    T0 = tmats[0] 

    f_j = np.array(list(tmats))
    w_j = np.array(ast.literal_eval(matches[0].split("np.array(")[-1][:-1]))
    
    return baryT(z_j, f_j, w_j, T0)