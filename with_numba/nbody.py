import numba
from numba import njit
import math
from numba.cuda import jit
import numpy as np
from numpy import float32

from numba import cuda
print(cuda.gpus)

eps_2 = np.float32(1e-6)
zero = np.float32(0.0)
one = np.float32(1.0)




def run_cpu_nbody(positions, weights):
    accelerations = np.zeros_like(positions)
    n = weights.size
    for j in range(n):
        # Compute influence of j'th body on all bodies
        r = positions[j] - positions
        rx = r[:,0]
        ry = r[:,1]
        sqr_dist = rx * rx + ry * ry + eps_2
        sixth_dist = sqr_dist * sqr_dist * sqr_dist
        inv_dist_cube = one / np.sqrt(sixth_dist)
        s = weights[j] * inv_dist_cube
        accelerations += (r.transpose() * s).transpose()
    return accelerations


def make_nbody_samples(n_bodies):
    positions = np.random.RandomState(0).uniform(-1.0, 1.0, (n_bodies, 2))
    weights = np.random.RandomState(0).uniform(1.0, 2.0, n_bodies)
    return positions.astype(np.float32), weights.astype(np.float32)


@cuda.jit(device=True, inline=True)
def body_body_interaction(xi, yi, xj, yj, wj, axi, ayi):
    """
    Compute the influence of body j on the acceleration of body i.
    """
    rx = xj - xi
    ry = yj - yi
    sqr_dist = rx * rx + ry * ry + eps_2
    sixth_dist = sqr_dist * sqr_dist * sqr_dist
    inv_dist_cube = one / math.sqrt(sixth_dist)
    s = wj * inv_dist_cube
    axi += rx * s
    ayi += ry * s
    return axi, ayi


@cuda.jit(device=True, inline=True)
def tile_calculation(xi, yi, axi, ayi, positions, weights):
    """
    Compute the contribution of this block's tile to the acceleration
    of body i.
    """
    for j in range(cuda.blockDim.x):
        xj = positions[j,0]
        yj = positions[j,1]
        wj = weights[j]
        axi, ayi = body_body_interaction(xi, yi, xj, yj, wj, axi, ayi)
    return axi, ayi

tile_size = 128
@cuda.jit
def calculate_forces(positions, weights, accelerations):
    """
    Calculate accelerations produced on all bodies by mutual gravitational
    forces.
    """
    sh_positions = cuda.shared.array((tile_size, 2), float32)
    sh_weights = cuda.shared.array(tile_size, float32)
    i = cuda.grid(1)
    axi = 0.0
    ayi = 0.0
    xi = positions[i,0]
    yi = positions[i,1]
    for j in range(0, len(weights), tile_size):
        index = (j // tile_size) * cuda.blockDim.x + cuda.threadIdx.x
        sh_index = cuda.threadIdx.x
        sh_positions[sh_index,0] = positions[index,0]
        sh_positions[sh_index,1] = positions[index,1]
        sh_weights[sh_index] = weights[index]
        cuda.syncthreads()
        axi, ayi = tile_calculation(xi, yi, axi, ayi,
                                    sh_positions, sh_weights)
        cuda.syncthreads()
    accelerations[i,0] = axi
    accelerations[i,1] = ayi



