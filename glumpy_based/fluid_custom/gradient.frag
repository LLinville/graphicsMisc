uniform sampler2D field;
uniform float cell_size;
uniform float timestep;

vec4 texelFetch(sampler2D sampler, vec2 pos)
{
    return texture2D(sampler, vec2(pos) * cell_size);
}

void main()
{
    vec2 T = vec2(gl_FragCoord.xy);

    // neighbors:
    float n = texelFetch(field, T + vec2(0, 1)).r;
    float s = texelFetch(field, T + vec2(0, -1)).r;
    float e = texelFetch(field, T + vec2(1, 0)).r;
    float w = texelFetch(field, T + vec2(-1, 0)).r;
    float c = texelFetch(field, T).r;

    vec2 grad = vec2(e - w, n - s);
//    gl_FragColor = vec4(0.5);
    gl_FragColor.rg = grad;
}
