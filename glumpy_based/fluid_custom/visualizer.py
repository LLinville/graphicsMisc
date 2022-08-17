import numpy as np
from glumpy import app, gloo, gl, data
from glumpy.log import log
from glumpy.gloo.gpudata import GPUData
from glumpy.gloo.globject import GLObject

from fluid_custom import Simulation

class Visualizer:

    def __init__(self):
        self.simulation = Simulation()
        self.vertex_shader_filename = "fluid.vert"
        self.simulation.vertex_shader_filename = self.vertex_shader_filename
        self.visualization_program = gloo.Program(self.vertex_shader_filename, "visualize.frag", count=4)
        self.visualization_program['Position'] = [(-1,-1), (-1,+1), (+1,-1), (+1,+1)]

        window = app.Window(1000, 1000)

        @window.event
        def on_init():
            gl.glDisable(gl.GL_DEPTH_TEST)
            gl.glDisable(gl.GL_BLEND)
            self.simulation = Simulation()

        @window.event
        def on_draw(dt):
            gl.glViewport(0, 0, self.simulation.width, self.simulation.height)
            gl.glDisable(gl.GL_BLEND)

            # self.simulation.step()

            gl.glViewport(0, 0, window.width, window.height)
            gl.glClearColor(0, 0, 0, 1)
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)
            gl.glEnable(gl.GL_BLEND)
            gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

            self.visualization_program['u_data'] = self.simulation.pressure.buffer_in.texture
            self.visualization_program['u_shape'] = self.simulation.width, self.simulation.height
            self.visualization_program['u_kernel'] = data.get("spatial-filters.npy")

            self.visualization_program["FillColor"] = 0.95, 0.925, 1.00
            self.visualization_program["Scale"] = 1.0/window.width, 1.0/window.height
            self.visualization_program.draw(gl.GL_TRIANGLE_STRIP)

        app.run()


if __name__ == "__main__":
    visualizer = Visualizer()
    pass






