uniform sampler2D velocity;

layout(points) in;
layout(points, max_vertices = 1100) out;

//out vec2
void main(void) {
    float dt = 0.0021;

    for (int i = 0; i < 50; i++) {
        gl_Position = gl_in[0].gl_Position + vec4(dt * i * texture2D(velocity, gl_in[0].gl_Position.xy/2 + vec2(0.5, 0.5)).xy, 0, 0);
        //    gl_Position = vec4(0.5, 0.5, 0, 1);
        EmitVertex();
    }

//    gl_Position = vec4(gl_in[0].gl_Position.xy, 0, 1);
//    gl_PointSize = 3.0;
//    EmitVertex();
//    gl_Position = gl_in[0].gl_Position + vec4(0.11, 0, 0, 0);
//    EmitVertex();

}