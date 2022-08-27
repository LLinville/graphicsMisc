uniform sampler2D velocity;
uniform sampler2D to_advect;
uniform float cell_size;
uniform float timestep;

vec4 texelFetch(sampler2D sampler, vec2 pos)
{
    return texture2D(sampler, vec2(pos) * cell_size);
}

void main()
{
    float flowrate = 1;
    vec2 T = vec2(gl_FragCoord.xy);

    vec2 vn = texelFetch(velocity, T + vec2(0, 1)).rg;
    vec2 vs = texelFetch(velocity, T + vec2(0, -1)).rg;
    vec2 ve = texelFetch(velocity, T + vec2(1, 0)).rg;
    vec2 vw = texelFetch(velocity, T + vec2(-1, 0)).rg;
    vec2 vc = texelFetch(velocity, T).rg;

    vec4 n = texelFetch(velocity, T + vec2(0, 1));
    vec4 s = texelFetch(velocity, T + vec2(0, -1));
    vec4 e = texelFetch(velocity, T + vec2(1, 0));
    vec4 w = texelFetch(velocity, T + vec2(-1, 0));
    vec4 c = texelFetch(to_advect, T);

//    float n = texelFetch(velocity, T + vec2(0, 1)).x;
//    float s = texelFetch(velocity, T + vec2(0, -1)).x;
//    float e = texelFetch(velocity, T + vec2(1, 0)).x;
//    float w = texelFetch(velocity, T + vec2(-1, 0)).x;
//    float c = texelFetch(to_advect, T).x;

    //    give_n = vec4(1, 0, 0, 0);
    //    give_s = vec4(1, 0, 0, 0);
    //    give_e = vec4(1, 0, 0, 0);
    //    give_w = vec4(1, 0, 0, 0);
    float give_n = -(vn.y + vc.y) / 2;
    float give_s = (vs.y + vc.y) / 2;
    float give_e = (ve.x + vc.x) / 2;
    float give_w = -(vw.x + vc.x) / 2;

    vec4 de = e * max(-1 * give_e, 0) - c * max(give_e, 0);
    vec4 dw = w * max(-1 * give_w, 0) - c * max(give_w, 0);
    vec4 dn = n * max(-1 * give_n, 0) - c * max(give_n, 0);
    vec4 ds = s * max(-1 * give_s, 0) - c * max(give_s, 0);

    gl_FragColor = c + (de + dw + dn + ds) * flowrate * timestep;




    // Take on value of neighbor, where they




}
