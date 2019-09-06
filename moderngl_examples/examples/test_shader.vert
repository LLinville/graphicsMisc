#version 330

in vec2 vert;

in vec4 vert_color;
out vec4 frag_color;

uniform vec2 scale;
uniform float rotation;

void main() {
    frag_color = vert_color;
    float r = rotation * (0.5 + gl_InstanceID * 0.05);
    mat2 rot = mat2(cos(r), sin(r), -sin(r), cos(r));
    gl_Position = vec4((rot * vert) * scale, 0.0, 1.0);
}