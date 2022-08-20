import numpy as np
from glumpy import app, gloo, gl, data
from glumpy.log import log
from glumpy.gloo.gpudata import GPUData
from glumpy.gloo.globject import GLObject
from glumpy.transforms import Position, OrthographicProjection, PanZoom

from simulation import Simulation


class Visualizer:

    def __init__(self):
        self.sim_width = 256
        self.sim_height = self.sim_width
        self.window_width = 1000
        self.window_height = 1000
        self.simulation = Simulation(width=self.sim_width, height=self.sim_height)
        self.vertex_shader_filename = "shaders/plotting/fluid.vert"
        self.simulation.vertex_shader_filename = self.vertex_shader_filename
        self.visualization_program = gloo.Program(self.vertex_shader_filename, "shaders/plotting/visualize.frag", count=4)
        self.visualization_program['Position'] = [(-1,-1), (-1,+1), (+1,-1), (+1,+1)]
        self.visualization_program.fragment._version = 130

        self.n_arrows_width = 32
        self.n_arrows = self.n_arrows_width ** 2
        self.arrows = np.zeros(self.n_arrows,
                           dtype=[('pos',         np.float32, 2),
                                  ('fg_color',    np.float32, 4),
                                  ('bg_color',    np.float32, 4),
                                  ('size',        np.float32, 1),
                                  ('head',        np.float32, 1),
                                  ('linewidth',   np.float32, 1)])
        self.arrows_program = gloo.Program("shaders/plotting/arrow.vert", "shaders/plotting/arrow.frag", count=self.n_arrows)
        self.arrows_program['fg_color'] = (1.0, 0.0, 0.0, 1.0)
        self.arrows_program['bg_color'] = (0.0, 1.0, 0.0, 1.0)
        self.arrows_program['size'] = 150.0
        self.arrows_program['head'] = 1.25
        self.arrows_program['linewidth'] = 36.0
        transform = OrthographicProjection(Position("pos"))
        self.arrows_program['transform'] = transform
        # self.arrows_program['Position'] = [(-1,-1), (-1,+1), (+1,-1), (+1,+1)]

        for x in range(self.n_arrows_width):
            for y in range(self.n_arrows_width):
                self.arrows['pos'][x + y * self.n_arrows_width] = x / self.n_arrows_width, y / self.n_arrows_width

        self.arrows['pos'] = np.random.random((self.n_arrows_width ** 2, 2))

        self.arrow_buffer = self.arrows.view(gloo.VertexBuffer)
        self.arrows_program.bind(self.arrow_buffer)

        window = app.Window(1000, 1000)

        @window.event
        def on_init():
            self._on_init()

        @window.event
        def on_draw(a=None):
            self._on_draw(0)

        app.run()

    def _on_init(self):
        gl.glDisable(gl.GL_DEPTH_TEST)
        gl.glDisable(gl.GL_BLEND)
        self.simulation = Simulation(self.sim_width, self.sim_height)

    def _on_draw(self, dt):
        gl.glViewport(0, 0, self.window_width, self.window_height)
        gl.glDisable(gl.GL_BLEND)

        for _ in range(10):
            self.simulation.step()

        gl.glViewport(0, 0, self.window_width, self.window_height)
        gl.glClearColor(0.2, 0.2, 0.2, 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

        data_to_display = self.simulation.pressure_gradient
        try:
            data_to_display = data_to_display.texture
        except Exception as ex:
            data_to_display = data_to_display.buffer_in.texture

        self.visualization_program['u_data'] = data_to_display
        self.visualization_program['u_shape'] = data_to_display.shape[1], data_to_display.shape[0]
        self.visualization_program['u_kernel'] = data.get("spatial-filters.npy")

        # self.visualization_program["FillColor"] = 0.95, 0.925, 1.00
        self.visualization_program["Scale"] = 1.0 / self.window_width, 1.0 / self.window_height
        # self.visualization_program.draw(gl.GL_TRIANGLE_STRIP)

        self.draw_arrows()

    def draw_arrows(self):
        self.arrows_program['velocity'] = self.simulation.velocity.buffer_in.texture
        self.arrows_program.draw(gl.GL_POINTS)


if __name__ == "__main__":
    visualizer = Visualizer()
    pass






