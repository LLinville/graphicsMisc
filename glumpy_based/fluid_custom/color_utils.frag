#version 130

// First color map
float cAbs(vec2 z)
{
    return sqrt(z.x * z.x + z.y * z.y);
}

float cArg(vec2 z)
{
    return atan(z.y, z.x);
}

vec2 cMul(vec2 z1, vec2 z2)
{
    return vec2(z1.x * z2.x - z1.y * z2.y, z1.x * z2.y + z1.y * z2.x);
}

vec2 cDiv(vec2 z1, vec2 z2)
{
    if (z2.y == 0)
    {
        return vec2(z1.x / z2.x, z1.y / z2.x);
    }
    if (z2.x == 0)
    {
        return vec2(z1.y / z2.y, -(z1.x / z2.y));
    }

    float r = z2.x * z2.x + z2.y * z2.y;
    return vec2((z1.x * z2.x + z1.y * z2.y) / r,
    (z1.y * z2.x - z1.x * z2.y) / r);
}

vec2 cPow(vec2 z, int k)
{
    vec2 res = vec2(1.0, 0);
    if (k >= 0)
    {
        for (; k > 0; k--)
        res = cMul(res, z);
    }
    else
    {
        for (; k < 0; k++)
        res = cDiv(res, z);
    }
    return res;
}

vec2 cSin(vec2 z)
{
    return vec2(sin(z.x) * cosh(z.y), cos(z.x) * sinh(z.y));
}

vec2 cCos(vec2 z)
{
    return vec2(cos(z.x) * cosh(z.y), sin(z.x) * sinh(z.y));
}

vec2 cTan(vec2 z)
{
    float cx = cos(z.x);
    float shy = sinh(z.y);
    float temp = cx * cx + shy * shy;
    return vec2((sin(z.x) * cx) / temp, (shy * cosh(z.y)) / temp);
}

vec2 cExp(vec2 z)
{
    return exp(z.x) * vec2(cos(z.y), sin(z.y));
}

vec2 cLog(vec2 z)
{
    return vec2(log(cAbs(z)), cArg(z));
}
float PI = atan(1.0)*4.0;
vec4 complexToColor(vec2 w)
{
    //Compute color hue
    float phi = cArg(w);
    if (phi < 0.0)
    phi += 2.0 * PI; // Restrict to interval [0,2PI]
    phi = degrees(phi);
    vec4 hue = vec4(0.0);
    vec4 c1 = vec4(0.0, 0.0, 0.0, 1.0); //Black
    vec4 c2 = vec4(1.0, 0.0, 0.0, 1.0); //Red
    vec4 c3 = vec4(1.0, 1.0, 0.0, 1.0); //Yellow
    //In the upper half of the plane, interploate between black and red
    if (phi >= 0.0 && phi < 180.0)
    {
        float s = (phi) / 180.0;
        hue = c2 * s + (1.0 - s) * c1;
    }
    //In the lower half of the plane, interploate between red and yellow
    else if (phi >= 180.0 && phi < 360.0)
    {
        float s = (phi - 180.0) / 180.0;
        hue = c3 * s + (1.0 - s) * c2;
    }

    //Compute brightness
    float r = cAbs(w);
    float brightness = fract(log2(r));

    return brightness * hue;
}