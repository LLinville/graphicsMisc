from numba import cuda, float32
import numpy as np
import math

import numpy as np
import matplotlib.pyplot as plt

plt.axis([0, 1, 0, 1])



G = np.float32(0.010)
eps_2 = np.float32(1e-6)
zero = np.float32(0.0)
one = np.float32(1.0)

timestep = np.float32(1e-7)

n_particles = 1000

@cuda.jit(device=True, inline=True)
def force(xi, yi, xj, yj, wj, acc):
    # print(xi, yi, xj, yj)
    """
    Compute the influence of body j on the acceleration of body i.
    """
    rx = xj - xi
    ry = yj - yi
    sqr_dist = rx * rx + ry * ry + eps_2
    # sixth_dist = sqr_dist * sqr_dist * sqr_dist
    # inv_dist_cube = one / math.sqrt(sixth_dist)
    s = wj * one / sqr_dist
    # print(s)
    acc[0] += rx * s
    acc[1] += ry * s

@cuda.jit()
def calc_pulls(pos, pos_out, vel, acc):
    p1_index = cuda.grid(1)
    for p2_index in range(n_particles):
        if p1_index == p2_index:
            continue
        force(pos[p1_index,0], pos[p1_index,1], pos[p2_index,0], pos[p2_index,1], G, acc[p1_index])
    vel[p1_index,0] += acc[p1_index,0]
    vel[p1_index,1] += acc[p1_index,1]
    pos_out[p1_index,0] = pos[p1_index,0] + vel[p1_index,0] * timestep
    pos_out[p1_index,1] = pos[p1_index,1] + vel[p1_index,1] * timestep




particles = np.array(np.random.random((n_particles, 2)), dtype=np.float32)
p_out = np.zeros_like(particles, dtype=np.float32)
# particles = cuda.to_device(particles)
velocities = np.array(np.stack([particles[...,1] * -1, particles[...,0]]), dtype=np.float32) * 1000
# velocities = np.zeros_like(particles, dtype=np.float32)
accelerations = np.zeros_like(particles, dtype=np.float32)
# particles = cuda.shared.array(shape=1, dtype=float32)
# particles_out = cuda.shared.array(shape=(n_particles), dtype=float32)

# Host code

threadsperblock = 32
blockspergrid = math.ceil(n_particles / threadsperblock)
print(velocities)

# particles = np.array([[0.2, 0.1],[1, 0.2]], dtype=np.float32)
# velocities = np.array([[0, 0],[0.0001,0.0002]], dtype=np.float32)


particles = cuda.to_device(particles)
p_out = cuda.to_device(p_out)
velocities = cuda.to_device(velocities)
accelerations = cuda.to_device(accelerations)


for i in range(1000000):
    print(i)
    plt.cla()
    plt.axis([-1, 1, -1, 1])


    for n in range(100):
        accelerations = np.zeros_like(particles, dtype=np.float32)
        calc_pulls[blockspergrid, threadsperblock](particles, p_out, velocities, accelerations)
    # print(np.sum(velocities * velocities))
    # print(np.max(particles))
    tmp = particles
    particles = p_out
    p_out = tmp
    plt.scatter(np.array(particles.copy_to_host())[...,0], np.array(particles.copy_to_host())[...,1], s=1)
    plt.pause(0.01)