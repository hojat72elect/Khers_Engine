from ursina import Quat, Shader, Vec2, Vec3, Vec4

instancing_shader = Shader(name='instancing_shader', language=Shader.GLSL, vertex='''#version 140

uniform mat4 p3d_ModelViewProjectionMatrix;
in vec4 p3d_Vertex;
in vec2 p3d_MultiTexCoord0;
in vec4 p3d_Color;
out vec2 texcoords;
out vec4 vertex_color;
uniform vec2 texture_scale;
uniform vec2 texture_offset;

uniform vec3 position_offsets[256];
uniform vec4 rotation_offsets[256];
uniform vec3 scale_multipliers[256];

void main() {
    vec3 v = p3d_Vertex.xyz * scale_multipliers[gl_InstanceID];
    vec4 q = rotation_offsets[gl_InstanceID];
    v = v + 2.0 * cross(q.xyz, cross(q.xyz, v) + q.w * v);

    gl_Position = p3d_ModelViewProjectionMatrix * (vec4(v + position_offsets[gl_InstanceID], 1.));
    texcoords = (p3d_MultiTexCoord0 * texture_scale) + texture_offset;
    vertex_color = p3d_Color;
}
''',

fragment='''#version 140

uniform sampler2D p3d_Texture0;
uniform vec4 p3d_ColorScale;
in vec2 texcoords;
in vec4 vertex_color;
out vec4 fragColor;

void main() {
    vec4 color = texture(p3d_Texture0, texcoords) * p3d_ColorScale * vertex_color;
    fragColor = color.rgba;
}
''',

default_input={
    'texture_scale': Vec2(1, 1),
    'texture_offset': Vec2(0.0, 0.0),
    'position_offsets': [Vec3(i, 0, 0) for i in range(256)],
    'rotation_offsets': [Vec4(0) for i in range(256)],
    'scale_multipliers': [Vec3(1) for i in range(256)],
}
)
