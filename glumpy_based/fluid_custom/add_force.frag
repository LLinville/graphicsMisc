uniform sampler2D buffer_in;
uniform sampler2D force;
uniform float cell_size;
uniform float scale_factor;
uniform float timestep;

void main()
{
    vec2 fragCoord = cell_size * gl_FragCoord.xy;

    gl_FragColor = timestep * scale_factor * texture2D(force, fragCoord) + texture2D(buffer_in, fragCoord);
}
