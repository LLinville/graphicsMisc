attribute vec2 pos;

void main() {
    gl_Position = vec4((pos.xy + 0*vec2(1.0, 1.0))/1.0, 0.0, 1.0);
//    gl_Position = vec4(pos.xy, 0.0, 1.0);
//    gl_Position = pos;
    gl_PointSize = 2.0;
}