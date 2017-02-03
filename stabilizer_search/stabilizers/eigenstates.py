"""Module which defines methods for converting the QObj Pauli Operators that 
generate each stabilizer group, building a projector and finding the associated 
+1 eigenstate."""

from numpy import allclose
from qutip import qeye


def find_projector(generating_set):
    n_qubits = len(generating_set)
    _id = qeye(pow(2, n_qubits))
    dims = [[2]*n_qubits, [2]*n_qubits]
    _id.dims = dims
    res = qeye(pow(2, n_qubits))
    res.dims = dims
    for _g in generating_set:
        res *= (_id+_g)/2
    return res

def find_eigenstate(projector):
    eigs, vecs = projector.eigenstates(sort='high')
    for _n, _eig in enumerate(eigs):
        if allclose(_eig, complex(1)) or allclose(_eig, 1.):
            return vecs[_n]
        else:
            print(eigs)
            return None

def py_find_eigenstates(generating_sets):
    """ """
    return map(find_eigenstate, 
               map(find_projector, generating_sets))
    #Dat functional pattern (╭☞￢ ل͜￢ )╭☞
