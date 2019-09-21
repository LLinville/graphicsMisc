import numba
from numba import njit
import math
import numpy as np

from numba import cuda
print(cuda.gpus)

@njit
def gpu_cos(x, out):
    # Assuming 1D array
    start = numba.cuda.grid(1)
    stride = numba.cuda.gridsize(1)
    for i in range(start, x.shape[0], stride):
        out[i] = math.cos(x[i])


def do_cos(x):
    out = numba.cuda.device_array_like(x)
    gpu_cos[64, 64](x, out)
    return out.copy_to_host()


# check if works locally first
test_x = np.random.uniform(-10, 10, 1000).astype(np.float32)
result = do_cos(test_x)
