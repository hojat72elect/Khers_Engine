from ursina import color
from ursina.shader import Shader

camera_grayscale_shader = Shader(
fragment='''
#version 430

uniform sampler2D tex;
in vec2 uv;
out vec4 color;

void main() {
    vec3 rgb = texture(tex, uv).rgb;
    float gray = rgb.r*.3 + rgb.g*.59 + rgb.b*.11;
    color = vec4(gray, gray, gray, 1.0);
}

''',
geometry='')
