import numpy as np
from glumpy import app, gloo, gl, data
from buffer import Buffer, BufferPair


class Simulation:
    def __init__(self):
        self.width = 256
        self.height = self.width

        self.timestep = 0.01

        self.velocity = BufferPair(self.width, self.height, 2)
        self.pressure = BufferPair(self.width, self.height, 1)
        self.pressure_gradient = Buffer(self.width, self.height, 2)
        self.velocity_divergence = Buffer(self.width, self.height, 1)

        self.program_filenames = [
            "advect.frag",
            "gradient.frag",
            "divergence.frag",
            "add_force.frag"
        ]
        
        self.vertex_shader_filename = "fluid.vert"
        self.programs = {}
        # for program_filename in self.program_filenames:
        #     program_name = program_filename.split('.')[0]
        #     program = gloo.Program(self.vertex_shader_filename, program_filename, count=4)
        #     program['Position'] = [(-1,-1), (-1,+1), (+1,-1), (+1,+1)]
        #     program['CellSize'] = 1.0 / self.width
        #     program['Timestep'] = self.timestep
        #     self.programs[program_name] = program

    def step(self):
        self.gradient(self.pressure.buffer_in, self.pressure_gradient)
        self.divergence(self.velocity.buffer_in, self.velocity_divergence)
        self.add_force(self.velocity, self.pressure_gradient, -1.0)
        self.add_force(self.pressure, self.velocity_divergence, -1.0)
        self.advect(self.pressure)
        self.advect(self.velocity)

    def advect(self, to_advect):
        program = self.programs['advect']
        program['velocity'] = self.velocity.buffer_in
        program['to_advect_in'] = to_advect.buffer_in
        program['to_advect_out'] = to_advect.buffer_out
        to_advect.buffer_out.activate()
        program.draw(gl.GL_TRIANGLE_STRIP)
        to_advect.buffer_out.deactivate()
        to_advect.swap()

    def gradient(self, field, buffer_out):
        program = self.programs['gradient']
        program['field'] = field
        program['to_advect_out'] = buffer_out
        buffer_out.activate()
        program.draw(gl.GL_TRIANGLE_STRIP)
        buffer_out.deactivate()

    def divergence(self, field, buffer_out):
        program = self.programs['divergence']
        program['field'] = field
        program['to_advect_out'] = buffer_out
        buffer_out.activate()
        program.draw(gl.GL_TRIANGLE_STRIP)
        buffer_out.deactivate()

    def add_force(self, to_update, force, scale_factor):
        program = self.programs['add_force']
        program['buffer_in'] = to_update.buffer_in
        program['buffer_out'] = to_update.buffer_out
        program['force'] = force
        program['scale_factor'] = scale_factor
        to_update.buffer_out.activate()
        program.draw(gl.GL_TRIANGLE_STRIP)
        to_update.buffer_out.deactivate()
        to_update.swap()

