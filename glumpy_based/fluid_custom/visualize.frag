// -----------------------------------------------------------------------------
// Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
// Distributed under the (new) BSD License.
// -----------------------------------------------------------------------------
// From Fluid demo by Philip Rideout
// Originals sources and explanation on http://prideout.net/blog/?p=58
// -----------------------------------------------------------------------------
#include "misc/spatial-filters.frag"

uniform sampler2D u_data;
uniform vec2 u_shape;
uniform vec3 FillColor;
uniform vec2 Scale;

void main()
{
    vec2 texcoord = gl_FragCoord.xy * Scale;
    float v = Bicubic(u_data, u_shape, texcoord).r;
    gl_FragColor = vec4(v, v, v, v);
}
