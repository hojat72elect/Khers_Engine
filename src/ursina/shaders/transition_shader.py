from ursina import color
from ursina.shader import Shader

transition_shader = Shader(name='transition_shader', language=Shader.GLSL, fragment='''
#version 140

uniform sampler2D p3d_Texture0;
uniform vec4 p3d_ColorScale;

in vec2 uv;
out vec4 COLOR;

uniform sampler2D mask_texture;
uniform float min_cutoff;
uniform float max_cutoff;
uniform float smooth_size;

void main() {
    vec3 color = texture2D(p3d_Texture0, uv).rgb * p3d_ColorScale.rgb;
    float value = texture(mask_texture, uv).r;

    float alpha = 1.;
    if (value <= min_cutoff || value > max_cutoff) {
        alpha = 0.;
    }

    COLOR = vec4(color.rgb, alpha * p3d_ColorScale.a);
}

''',

default_input = {
    'min_cutoff' : 0,
    'max_cutoff' : 1,
    'smooth_size' : .25,
}
)
