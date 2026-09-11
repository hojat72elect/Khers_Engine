from ursina.shader import Shader

normals_shader = Shader(name='normals_shader',language=Shader.GLSL,
vertex = '''
#version 140
uniform mat4 p3d_ModelViewProjectionMatrix;
uniform mat4 p3d_ModelMatrix;
in vec4 p3d_Vertex;
in vec3 p3d_Normal;
out vec3 world_normal;

void main() {
    gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
    world_normal = normalize(mat3(p3d_ModelMatrix) * p3d_Normal);
}
''',

fragment='''
#version 130

uniform vec4 p3d_ColorScale;
in vec2 texcoord;
out vec4 fragColor;
in vec3 world_normal;


void main() {
    fragColor = vec4(world_normal*0.5+0.5, 1);
}

''',
geometry='',
)
