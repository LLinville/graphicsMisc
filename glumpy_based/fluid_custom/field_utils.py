import numpy as np


def force_gaussian_puff(shape, position, radius=0.1, velocity=(0.1,0.1)):
    magnitude = np.array([
        [

            1 / np.exp(
                ((y-position[0]) * (y-position[0]) +
                (x-position[1]) * (x-position[1])) / radius)
             for y in np.linspace(-1, 1, shape[1])
        ] for x in np.linspace(-1, 1, shape[0])
    ])

    return np.array(velocity)[np.newaxis, np.newaxis, ...] * magnitude[:, :, np.newaxis]


def spiral(shape):
    force = np.array(
        [
            [
                [
                    # loop_noise2(x, y, noise_scale, noise_x), loop_noise2(x, y, noise_scale, noise_y)
                    y*1/np.exp(x*x+y*y), -x*1/np.exp(x*x+y*y)
                ] for x in np.linspace(-5, 5, shape[0])
            ] for y in np.linspace(-5, 5, shape[1])
        ]
    )

    return force