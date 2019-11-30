import numpy as np
import cmath
from math import sqrt

import moderngl
from window import Example

def invert(x, y):
    mag = x*x+y*y
    return min(x / mag, 1), min(y / mag, 1)


def add_point(field, location, size=10, polarity=1, rotation = 0, turns=1):
    patch_input_x, patch_input_y = np.meshgrid(np.linspace(-1, 1, size), np.linspace(-1, 1, size))
    patch = np.zeros((size, size), dtype=complex)
    for u in range(size):
        for v in range(size):
            input_point = patch_input_x[u,v] + 1j * patch_input_y[u,v]
            r, theta = np.abs(input_point), np.angle(input_point)
            theta *= turns
            r = 1 / np.abs(r * 10)
            input_point = cmath.rect(r, theta)
            dist2 = (u) ** 2 + (v) ** 2 + 1
            patch[u,v] += input_point

    rotated = patch * (np.cos(rotation) + np.sin(rotation) * 1j)

    field[location[0] - size // 2 : location[0] + size // 2, location[1] - size // 2 : location[1] + size // 2, 0] += rotated.real
    field[location[0] - size // 2: location[0] + size // 2, location[1] - size // 2: location[1] + size // 2, 1] += rotated.imag


class Conway(Example):
    title = "Polar field"
    aspect_ratio = 1.0
    window_size = (500, 500)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        width, height = self.window_size
        canvas = np.array([0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0]).astype('f4')
        pixels = np.random.rand(width, height,2).astype('f4')
        pixels = np.array([
            [[invert(x, y)] for y in np.linspace(-10, 10, width)] for x in np.linspace(-10, 10, height)
        ]).astype('f4')
        pixels = np.zeros((width, height, 2)).astype('f4')
        # add_point(pixels, (200, 200), 50)
        add_point(pixels, (300, 300), 300, turns=31)
        grid = np.dstack(np.mgrid[0:height, 0:width][::-1]).astype('i4')

        self.prog = self.ctx.program(
            vertex_shader='''
                #version 330

                in vec2 in_vert;
                out vec2 v_text;
                
                void main() {
                    v_text = in_vert;
                    gl_Position = vec4(in_vert * 2.0 - 1.0, 0.0, 1.0);
                }
            ''',
            fragment_shader='''
                #version 330
                
                const float PI = 3.1415926535897932384626433832795;

                uniform sampler2D Texture;

                in vec2 v_text;
                out vec4 f_color;
                
                vec3 hsv2rgb(vec3 c) {
                  vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
                  vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
                  return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
                }

                void main() {
                    vec4 input = texture(Texture, v_text);
                    float mag = input.r*input.r+input.g*input.g;
                    mag = sqrt(mag);
                    vec3 hsv = vec3(atan(input.r, input.g)/(2*PI), 1, mag * 0.7 + 0.3);
                    vec3 rgb = hsv2rgb(hsv);
                    f_color = vec4(rgb.rgb, 1);
                }
            ''',
        )

        self.transform = self.ctx.program(
            vertex_shader='''
                #version 330

                uniform sampler2D Texture;
                uniform int Width;
                uniform int Height;

                in ivec2 in_text;
                out vec2 out_vert;

                vec2 lookup(int x, int y) {
                    return texelFetch(Texture, ivec2((x + Width) % Width, (y + Height) % Height), 0).rg;
                }

                void main() {
                    vec2 total = lookup(in_text.x, in_text.y);

                    total += lookup(in_text.x - 1, in_text.y);
                    total += lookup(in_text.x + 1, in_text.y);
                    total += lookup(in_text.x, in_text.y - 1);
                    total += lookup(in_text.x, in_text.y + 1);

                    out_vert = total / 5.0;
                    //out_vert = lookup(in_text.x, in_text.y);
                }
            ''',
            varyings=['out_vert']
        )

        self.transform['Width'].value = width
        self.transform['Height'].value = height

        self.texture = self.ctx.texture((width, height), 2, pixels.tobytes(), dtype='f4')
        self.texture.filter = (moderngl.NEAREST, moderngl.NEAREST)
        self.texture.swizzle = 'RGG1'
        self.texture.use()

        self.vbo = self.ctx.buffer(canvas.tobytes())
        self.vao = self.ctx.simple_vertex_array(self.prog, self.vbo, 'in_vert')

        self.text = self.ctx.buffer(grid.tobytes())
        self.tao = self.ctx.simple_vertex_array(self.transform, self.text, 'in_text')
        self.pbo = self.ctx.buffer(reserve=pixels.nbytes)

    def render(self, time, frame_time):
        self.ctx.clear(1.0, 1.0, 1.0)

        self.tao.transform(self.pbo)
        self.texture.write(self.pbo)

        self.vao.render(moderngl.TRIANGLE_STRIP)


if __name__ == '__main__':
    Conway.run()
