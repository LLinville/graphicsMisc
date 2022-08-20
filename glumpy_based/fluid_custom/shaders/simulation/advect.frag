uniform sampler2D velocity;
uniform sampler2D to_advect;
uniform vec2 cell_size;
uniform float timestep;

vec4 texelFetch(sampler2D sampler, vec2 pos)
{
    return texture2D(sampler, vec2(pos) * cell_size);
}

void main()
{
    vec2 fragCoord = gl_FragCoord.xy;

    vec2 vel = texture2D(velocity, gl_FragCoord.xy).xy;
    vec2 coord = cell_size * (fragCoord - timestep * vel);
    gl_FragColor = 1.0 * texture2D(to_advect, coord);
}
