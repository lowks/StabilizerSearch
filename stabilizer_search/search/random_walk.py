from . import _Search, _Result
from ..lingalg import ortho_projector
from ..mat import qeye
from ..stabilizer import get_stabilizer_states
from ..stabilizer.utils import array_to_pauli

from math import exp, pow
from six import PY2
from random import random, randrange

import numpy as np


def test_real(n_qubits, bits):
    x_bits, z_bits = bits[:n_qubits], bits[n_qubits:]
    _sum = 0
    for i in range(n_qubits):
        if x_bits[i]&z_bits[1]:
            _sum +=1
    return sum%2


def random_pauli(n_qubits, real_only):
    while True:
        base = bin(randrange(pow(2, n_qubits)))[2:]
        bits = '0'*(2*n_qubits - len(base)) + base
        bits = np.array([b == '1' for b in bits])
        if real_only:
            if test_real(bits):
                break
        else:
            break
    return array_to_pauli(bits)

def do_RandomWalk(n_qubits, target_state, chi, **kwargs):
    beta = kwargs.pop('beta_init', 1)
    beta_max = kwargs.pop('beta_max', 4000)
    anneal_steps = kwargs.pop('M', 1000)
    b_diff = (beta_max-beta)/anneal_steps
    walk_steps = kwargs.pop('steps', 100)
    real = np.allclose(np.imag(target_state, 0.))
    stabilizers = get_stabilizer_states(n_qubits, chi, real_only=real)
    I = qeye(n_qubits)
    while beta <= beta_max:
        for i in range(walk_steps):
            projector = ortho_projector(stabilizers)
            overlap = np.linalg.norm(projector*target_state, 2)
            if np.allclose(overlap, 1.):
                return True, chi, stabilizers
            while True:
                move = random_pauli(n_qubits, real)
                target_state = randrange(chi)
                new_state = (I+move) * stabilizers[target_state]
                if not np.allclose(new_state, 0.): #Accept the move only if the resulting state is not null!
                    break
            new_state /= np.linalg.norm(new_state, 2) #Normalize!
            new_projector = ortho_projector([s for n, s in enumerate(states) if 
                                            n != target_state else new_state])
            new_overlap = np.lingalg.norm(new_projector*target_state, 2)
            if new_overlap > overlap:
                stabilizers[target_state] = new_state
            else:
                p_accept = exp(-beta*(overlap - new_overlap))
                if random() < p_accept:
                    stabilizers[target_state] = new_state
        beta += beta_diff
    return False, chi, None

class RandomWalkResult(_Result):
    ostring = """
    The Random Walk method for the state {target_state} on {n_qubits} qubits,
    {success} in finding a decomposition with stabilizer rank {chi}.
    {decomposition}
    """

    def __init__(self, *args):
        args[-1] = self.parse_decomposition(args[-1])
        if PY2:
            super(RandomWalkResult, self).__init__(*args)
        else:
            super().__init__(*args)

    def parse_decomposition(self, decomposition):
        if decomposition is None:
            return ''
        else:
            return "\n".join(str(state) for state in decomposition)


class RandomWalkSearch(_Search):
    Result_Class = RandomWalkResult
    func = do_RandomWalk

    def __init__(self, *args, **kwargs):
        if PY2:
            super(RandomWalkSearch, self).__init__(*args, **kwargs)
        else:
            super().__init__(*args, **kwargs)