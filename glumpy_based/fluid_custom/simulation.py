import numpy as np
from glumpy import app, gloo, gl, data
from glumpy.graphics.collections import PointCollection
from buffer import TextureBuffer, BufferPair
from opensimplex import OpenSimplex
from math import pi

noise_x = OpenSimplex(seed=1)
noise_y = OpenSimplex(seed=0)


# x and y are in the range [0,1] where 0 wraps back to 1
def loop_noise2(x, y, scale=0.1, noisegen=None):
    return noisegen.noise4(
        scale * np.sin(2 * pi * x),
        scale * np.cos(2 * pi * x),
        scale * np.sin(2 * pi * y),
        scale * np.cos(2 * pi * y)
    )


class Simulation:
    def __init__(self, width, height, n_points = 1000):
        self.width = width
        self.height = height

        self.timestep = 0.01

        # self.n_points = n_points
        # self.points = PointBuffer(np.random.random((self.n_points, 2)) * 100)

        noise_scale = 1.0
        initial_velocity = np.array(
            [
                [
                    [loop_noise2(x, y, noise_scale, noise_x), loop_noise2(x, y, noise_scale, noise_y)] for x in np.linspace(-1, 1, width)
                ] for y in np.linspace(-1, 1, width)
            ]
        )
        self.velocity = BufferPair(self.width, self.height, 2, initial_value=initial_velocity)
        self.pressure = BufferPair(self.width, self.height, 1, initial_value='zero')
        self.pressure_gradient = TextureBuffer(self.width, self.height, 2, initial_value='zero')
        self.velocity_divergence = TextureBuffer(self.width, self.height, 1, initial_value='zero')

        self.program_filenames = [
            "advect.frag",
            "gradient.frag",
            "divergence.frag",
            "add_force.frag",
            "blur.frag"
        ]
        
        self.vertex_shader_filename = "shaders/plotting/fluid.vert"
        self.programs = {}
        for program_filename in self.program_filenames:
            program_name = program_filename.split('.')[0]
            program = gloo.Program(
                self.vertex_shader_filename,
                f"shaders/simulation/{program_filename}",
                count=4
            )
            program['Position'] = [(-1,-1), (-1,+1), (+1,-1), (+1,+1)]
            program['cell_size'] = 1.0 / self.width
            self.programs[program_name] = program

    def step(self):
        pass
        self.gradient(self.pressure.buffer_in, self.pressure_gradient)
        self.divergence(self.velocity.buffer_in, self.velocity_divergence)
        self.add_force(self.velocity, self.pressure_gradient, -1.0 * 0.1)
        self.add_force(self.pressure, self.velocity_divergence, -1.0 * 0.1)
        self.blur(self.velocity, 0.001)
        self.blur(self.pressure, 0.001)
        self.advect(self.pressure)
        self.advect(self.velocity)
        # self.advect_points(self.velocity, self.points)

    def advect(self, to_advect):
        program = self.programs['advect']
        program['velocity'] = self.velocity.buffer_in.texture
        program['to_advect'] = to_advect.buffer_in.texture
        program['timestep'] = self.timestep
        to_advect.buffer_out.activate()
        program.draw(gl.GL_TRIANGLE_STRIP)
        to_advect.buffer_out.deactivate()
        to_advect.swap()

    def gradient(self, field, buffer_out):
        program = self.programs['gradient']
        program['field'] = field.texture
        buffer_out.activate()
        program.draw(gl.GL_TRIANGLE_STRIP)
        buffer_out.deactivate()

    def divergence(self, field, buffer_out):
        program = self.programs['divergence']
        program['field'] = field.texture
        buffer_out.activate()
        program.draw(gl.GL_TRIANGLE_STRIP)
        buffer_out.deactivate()

    def add_force(self, to_update, force, scale_factor):
        program = self.programs['add_force']
        program['buffer_in'] = to_update.buffer_in.texture
        program['force'] = force.texture
        program['scale_factor'] = scale_factor
        program['timestep'] = self.timestep
        to_update.buffer_out.activate()
        program.draw(gl.GL_TRIANGLE_STRIP)
        to_update.buffer_out.deactivate()
        to_update.swap()

    def blur(self, to_update, intensity):
        program = self.programs['blur']
        program['field'] = to_update.buffer_in.texture
        program['blur_intensity'] = intensity
        to_update.buffer_out.activate()
        program.draw(gl.GL_TRIANGLE_STRIP)
        to_update.buffer_out.deactivate()
        to_update.swap()
