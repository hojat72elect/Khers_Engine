from ursina.shader import Shader

camera_contrast_shader = Shader(fragment='''
#version 430

uniform sampler2D tex;
uniform float contrast = 1.;

in vec2 uv;
out vec4 out_color;



void main() {
    vec4 color = texture(tex, uv).rgba;
    color.rgb = clamp(mix(vec3(0.5, 0.5, 0.5), color.rgb, contrast), 0., 1.);   // adjust contrast
    out_color = color;
}


''',
default_input={
    'contrast': 1,
}
)
