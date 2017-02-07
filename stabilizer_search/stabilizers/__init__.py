"""Module for obtaining Stabilizer States as Numpy arrays. The main method 
provided by this module is `get_stabilizer_states`, which is also available in 
the package namespace.

Potential future plans would allow a more general representation than QObj 
states. Alternatively, we could look to implement a wrapper function capable of 
transforming between a QObj and the raw vector."""

from.eigenstates import py_find_eigenstates
from .py_generators import get_positive_stabilizer_groups as py_positive_groups
from .utils import n_stabilizer_states

import os.path as path
import pickle


__all__ = ['get_stabilizer_states']


APP_DIR = path.abspath(__file__)
STATE_STRING = '{}_stabs.pkl'
GROUP_STRING = '{}_groups.pkl'


def try_load(format_string, n_qubits, n_states=None):
    f_string = format_string.format(n_qubits)
    package_path = path.join(APP_DIR, 'data', f_string)
    rel_path = path.join('./', f_string)
    if path.exists(package_path):
        with open(package_path, 'rb') as _f:
            items = pickle.load(_f)
    elif path.exists(rel_path):
        with open(package_path, 'rb') as _f:
            items = pickle.load(_f)
    else:
        items = None
    if n_states != n_stabilizer_states(n_qubits):
        return items.sample(n_states)
    return items


def save_to_pickle(items, format_string, n_qubits):
    with open(path.join('./', format_string.format(n_qubits)), 'wb') as f:
        pickle.dump(items, f)
    return


def get_stabilizer_states(n_qubits, n_states=None, **kwargs):
    """Method for returning a set of stabilizer states. It takes the following 
    arguments:
    Positional:
      n_qubits: The number of qubits our stabilizer states will be built out of.
      n_states (Optional): Number of stabilizer states we require. If not 
      specified, defaults to all Stabilier states.
    Keyword:
      use_cached: Boolean, defaults to True and looks in the package or working 
      dir for serialised states or generators.
      generator_backend: Function which searches for the stabilizer generators
      eigenstate_backend: Function which takes sets of stabilizer generators and
      builds the corresponding eigenstates.
    """
    use_cached = kwargs.get('use_cached', True)
    generator_func = kwargs.get('generator_backend', py_positive_groups)
    eigenstate_func = kwargs.get('eigenstate_backend', py_find_eigenstates)
    stabilizer_states = None
    if n_states is None:
        n_states = n_stabilizer_states(n_qubits)
    if use_cached:
        stabilizer_states = try_load(STATE_STRING, n_qubits, n_states)
        if stabilizer_states is None:
            groups = try_load(GROUP_STRING, n_qubits, n_states)
            if groups is not None:
                if n_states == n_stabilizer_states(n_qubits):
                    save_to_pickle(groups, GROUP_STRING, n_qubits)
                stabilizer_states = eigenstate_func(groups, n_states)
    if stabilizer_states is None:
        stabilizer_states = eigenstate_func(generator_func(n_qubits, n_states))
        if use_cached:
            save_to_pickle(stabilizer_states, STATE_STRING, n_qubits)
    return stabilizer_states
