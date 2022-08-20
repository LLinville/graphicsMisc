uniform sampler2D field;
uniform vec2 cell_size;
uniform float blur_intensity;

vec4 texelFetch(sampler2D sampler, vec2 pos)
{
    return texture2D(sampler, vec2(pos) * cell_size);
}


void main()
{
    vec2 fragCoord = cell_size * gl_FragCoord.xy;
    vec2 T = gl_FragCoord.xy;

    vec2 n = texelFetch(field, T + vec2(0, 1)).rg;
    vec2 s = texelFetch(field, T + vec2(0, -1)).rg;
    vec2 e = texelFetch(field, T + vec2(1, 0)).rg;
    vec2 w = texelFetch(field, T + vec2(-1, 0)).rg;
    vec2 c = texelFetch(field, T).rg;

    vec2 neighbor_average = (n + e + s + w) / 4.0;
    gl_FragColor = vec4( blur_intensity * neighbor_average + (1-blur_intensity) * c, 0, 1.0);
}
