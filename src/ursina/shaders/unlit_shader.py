import ursina
from ursina.ursinastuff import Func
from ursina.shader import Shader
from ursina.vec2 import Vec2
from ursina.vec3 import Vec3
from ursina import color
# from ursina.camera import instance as camera
# from ursina.scene import instance as scene

unlit_shader = Shader(name='unlit_shader', language=Shader.GLSL, vertex = '''#version 140

uniform mat4 p3d_ModelViewProjectionMatrix;
uniform mat4 p3d_ModelViewMatrix;
uniform mat4 p3d_ModelMatrix;
in vec4 p3d_Vertex;
in vec2 p3d_MultiTexCoord0;
out vec2 uvs;
uniform vec2 texture_scale;
uniform vec2 texture_offset;

in vec4 p3d_Color;
out vec4 vertex_color;

void main() {
    gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
    uvs = (p3d_MultiTexCoord0 * texture_scale) + texture_offset;
    vertex_color = p3d_Color;
}
''',

fragment='''
#version 140

uniform sampler2D p3d_Texture0;
uniform vec4 p3d_ColorScale;
in vec2 uvs;
out vec4 fragColor;

in vec4 vertex_color;

void main() {
    vec4 color = texture(p3d_Texture0, uvs) * p3d_ColorScale * vertex_color;
    fragColor = color;
}

''',
default_input={
    'texture_scale': Vec2(1,1),
    'texture_offset': Vec2(0.0, 0.0),
},
)
