import numpy as np
from glumpy import app, gloo, gl, data


class Buffer:
    def __init__(self, width, height, depth, initial_value=None):
        if initial_value is None:
            initial_value = (np.random.random((height, width, depth)) - 0.5)
        elif initial_value == 'zero':
            initial_value = np.zeros((height, width, depth))

        self.texture = np.array(initial_value, dtype=np.float32).view(gloo.TextureFloat2D)
        self.texture.interpolation = gl.GL_LINEAR
        self.texture.wrapping = gl.GL_REPEAT
        self.buffer = gloo.FrameBuffer(color=self.texture)

    def clear(self):
        self.buffer.activate()
        gl.glClearColor(0, 0, 0, 0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        self.buffer.deactivate()

    def activate(self):
        self.buffer.activate()

    def deactivate(self):
        self.buffer.deactivate()


class BufferPair:
    def __init__(self, width, height, depth, initial_value=None):
        self.buffer_in = Buffer(width, height, depth, initial_value=initial_value)

        self.buffer_out = Buffer(width, height, depth, initial_value=initial_value)

    def swap(self):
        self.buffer_in, self.buffer_out = self.buffer_out, self.buffer_in
