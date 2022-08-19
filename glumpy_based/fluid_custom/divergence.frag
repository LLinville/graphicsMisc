// -----------------------------------------------------------------------------
// Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
// Distributed under the (new) BSD License.
// -----------------------------------------------------------------------------
// From Fluid demo by Philip Rideout
// Originals sources and explanation on http://prideout.net/blog/?p=58
// -----------------------------------------------------------------------------
uniform sampler2D field;
uniform float cell_size;

vec4 texelFetch(sampler2D sampler, vec2 pos)
{
    return texture2D(sampler, vec2(pos) * cell_size);
}

void main()
{
    vec2 T = vec2(gl_FragCoord.xy);

    // Find neighboring velocities:
    vec2 n = texelFetch(field, T + vec2(0, 1)).rg;
    vec2 s = texelFetch(field, T + vec2(0, -1)).rg;
    vec2 e = texelFetch(field, T + vec2(1, 0)).rg;
    vec2 w = texelFetch(field, T + vec2(-1, 0)).rg;
    vec2 c = texelFetch(field, T).rg;

    gl_FragColor.r = 0.5 * (e.x - w.x + n.y - s.y);
}
