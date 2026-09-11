from ursina import Shader, Vec2, Vec3

vertex_animation_shader = Shader(
vertex='''
#version 330 core

uniform mat4 p3d_ModelViewProjectionMatrix;
in vec4 p3d_Vertex;
in vec2 p3d_MultiTexCoord0;
out vec2 uvs;
uniform vec2 texture_scale;
uniform vec2 texture_offset;

in vec4 p3d_Color;

uniform sampler2D frame_texture; // texture containing all animation frames
uniform float frame_index;
uniform float total_frames;
uniform vec3 pos_min;
uniform vec3 pos_max;
uniform float num_verts;

out vec4 vertex_color;

void main() {
    float frame_height = 1.0 / total_frames; // Each frame's height in the texture
    vec3 pos_offset = texture(frame_texture, vec2((gl_VertexID/num_verts) + ((1./num_verts)*.5), (frame_index/total_frames) + (frame_height*.5))).rgb;
    vec3 denormalized_pos_offset = mix(pos_min, pos_max, pos_offset.xyz);
    gl_Position = p3d_ModelViewProjectionMatrix * vec4(denormalized_pos_offset, 1.0);
    uvs = (p3d_MultiTexCoord0 * texture_scale) + texture_offset;
    vertex_color = p3d_Color;
    vertex_color = texture(frame_texture, vec2((gl_VertexID/num_verts) + ((1./num_verts)*.5) +.5, (frame_index/total_frames) + (frame_height*.5)));
}

''',

fragment='''
#version 330 core

uniform sampler2D p3d_Texture0;
uniform vec4 p3d_ColorScale;
in vec2 uvs;
out vec4 fragColor;

in vec4 vertex_color;

void main() {
    vec4 color = texture(p3d_Texture0, uvs) * p3d_ColorScale * vertex_color;
    fragColor = color.rgba;
}

''',
default_input = {
    'texture_scale' : Vec2(1,1),
    'texture_offset' : Vec2(0.0, 0.0),

    'frame_index': 0,
}
)
