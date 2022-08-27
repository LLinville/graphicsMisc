uniform sampler2D field;
uniform vec2 cell_size;
uniform vec2 position;
uniform float amount;
uniform float radius;

#define rpos relative_position

void main()
{
    vec2 fragCoord = gl_FragCoord.xy * cell_size;

    float current = texture2D(field, fragCoord).x;
    vec2 relative_position = fragCoord - position;
    float to_add = amount / exp((rpos.x*rpos.x + rpos.y*rpos.y) / radius);
    to_add = rpos.x * rpos.x + rpos.y * rpos.y;
    gl_FragColor = vec4(1*current + 0*to_add/10000, 0, 0, 0);
}
