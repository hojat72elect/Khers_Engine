from ursina import color
from ursina.shader import Shader
from ursina.vec3 import Vec3

fog_of_war_shader = Shader(language=Shader.GLSL,
vertex = '''
#version 140
uniform mat4 p3d_ModelViewProjectionMatrix;
uniform mat4 p3d_ModelMatrix;

in vec4 p3d_Vertex;
in vec2 p3d_MultiTexCoord0;
out vec2 texcoord;

in vec3 p3d_Normal;
out vec3 world_normal;
uniform vec3 light_position;
out float dist;

void main() {
    gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
    texcoord = p3d_MultiTexCoord0;

    // dist = length(light_position - p3d_Vertex.rgb) * .1;
    dist = length(light_position - gl_Position.xyz) * .01;
    // dist = 1.0;
}
''',

fragment='''
#version 140

uniform sampler2D p3d_Texture0;
uniform vec4 p3d_ColorScale;
in vec2 texcoord;
in vec3 world_normal;
out vec4 fragColor;
in float dist;

// uniform mat4 p3d_ViewProjectionMatrix;
// uniform sampler2D tex;
// uniform sampler2D dtex;
// in vec2 uv;
// out vec4 o_color;

// uniform vec3 light_position;

// vec3 reconstructPosition(in vec2 uv, in float z)
// {
//     float x = uv.x * 2.0f - 1.0f;
//     float y = (1.0 - uv.y) * 2.0f - 1.0f;
//     vec4 position_s = vec4(x, y, z, 1.0f);
//     mat4x4 view_projection_matrix_inverse = inverse(p3d_ViewProjectionMatrix);
//     vec4 position_v = view_projection_matrix_inverse * position_s;
//     return position_v.xyz / position_v.w;
// }

void main() {
    vec4 color = texture(p3d_Texture0, texcoord) * p3d_ColorScale * (1-dist);
    color.a = 1.;
    fragColor = color.rgba;


    // float depth = texture(dtex, uv).r;
    // vec3 position = reconstructPosition(uv, depth);
    //
    // float dist = (position - light_position).x;
    //
    // o_color.rgb = texture(tex, uv).rgb * dist;
    // // o_color.rgb = vec3(dist);
    // o_color.a = 1.0;
}


''', geometry='',
default_input = {
    'light_position' : Vec3(0,1,0),

}
)
