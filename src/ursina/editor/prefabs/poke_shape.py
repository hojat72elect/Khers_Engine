from ursina.editor.level_editor import *
from ursina.shaders import colored_lights_shader
from ursina.scripts.property_generator import generate_properties_for_class

@generate_properties_for_class()
class PokeShape(Entity):
    default_values = Entity.default_values | dict(
        name='poke_shape',
        wall_height=1.0,
        subdivisions=0,
        smoothing_distance=.1,
        points=[Vec3(-.5,0,-.5), Vec3(.5,0,-.5), Vec3(.5,0,.5), Vec3(-.5,0,.5)],
        collider_type='None',
        texture='grass',
        texture_scale=Vec2(.125, .125),
    )  # combine dicts

    gizmo_color = color.violet

    def __init__(self, edit_mode=False, **kwargs):
        kwargs = __class__.default_values | kwargs
        points = kwargs.pop('points', None)
        self.ready = False
        super().__init__(**kwargs)

        self.original_parent = LEVEL_EDITOR
        self.selectable = True
        self.highlight_color = color.blue
        self.model = Mesh()
        self.add_new_point_renderer = Entity(model=Mesh(mode='point', vertices=[], thickness=.075), color=color.white, alpha=.5, texture='circle', unlit=True, is_gizmo=True, selectable=False, enabled=False, always_on_top=True)
        self.add_collider = False
        self._wall_parent = None
        self.wall_height = kwargs['wall_height']
        self.subdivisions =  kwargs['subdivisions']
        self.smoothing_distance = kwargs['smoothing_distance']

        self._point_gizmos = []
        if not points:
            self.points = __class__.default_values['points']
        else:
            self.points = points

        self.texture = kwargs['texture']
        self.position = kwargs['position']
        for key in Entity.default_values.keys():
            if key == 'model':
                continue
            setattr(self, key, kwargs[key])

        self.edit_mode = edit_mode
        self.generate()
        self.ready = True

    def draw_inspector(self):
        return {'edit_mode': bool, 'wall_height': float, 'subdivisions':int, 'smoothing_distance':float}

    def generate(self):
        import tripy
        self._point_gizmos = LoopingList([e for e in self._point_gizmos if e])   # ensure deleted points are removed
        polygon = LoopingList(Vec2(*e.get_position(relative_to=self).xz) for e in self._point_gizmos)

        if self.subdivisions:
            for j in range(self.subdivisions):
                smooth_polygon = LoopingList()
                for i, p in enumerate(polygon):
                    smooth_polygon.append(lerp(p, polygon[i-1], self.smoothing_distance))
                    smooth_polygon.append(lerp(p, polygon[i+1], self.smoothing_distance))
                polygon = smooth_polygon

        triangles = tripy.earclip(polygon)
        self.model.vertices = []
        for tri in triangles:
            for v in tri:
                self.model.vertices.append(Vec3(v[0], 0, v[1]))

        self.model.uvs = [Vec2(v[0],v[2])*1 for v in self.model.vertices]
        self.model.normals = [Vec3(0,1,0) for i in range(len(self.model.vertices))]
        self.model.generate()
        if self._wall_parent:
            destroy(self._wall_parent)
            self._wall_parent = None

        if self.wall_height:
            if not self._wall_parent:
                self._wall_parent = Entity(parent=self, model=Mesh(), color=color.dark_gray, add_to_scene_entities=False, shader=colored_lights_shader)

            wall_verts = []
            for i, vert in enumerate(polygon):
                vert = Vec3(vert[0], 0, vert[1])
                next_vert = Vec3(polygon[i+1][0], 0, polygon[i+1][1])

                wall_verts.extend((
                    vert,
                    vert + Vec3(0,-self.wall_height,0),
                    next_vert,

                    next_vert,
                    vert + Vec3(0,-self.wall_height,0),
                    next_vert + Vec3(0,-self.wall_height,0),
                ))
            self._wall_parent.model.vertices = wall_verts
            self._wall_parent.model.generate_normals(False)
            self._wall_parent.model.generate()

        if self.edit_mode:
            self.add_new_point_renderer.model.vertices = []
            for i, e in enumerate(self._point_gizmos):
                self.add_new_point_renderer.model.vertices.append(lerp(self._point_gizmos[i].world_position, self._point_gizmos[i+1].world_position, .5))
            self.add_new_point_renderer.model.generate()

    def __deepcopy__(self, memo):
        changes = self.get_changes(__class__)
        _copy = __class__(texture_scale = self.texture_scale, **changes)
        _copy.texture_scale = self.texture_scale
        return _copy

    def points_getter(self):
        return [e.position for e in self._point_gizmos]

    def points_setter(self, value):
        [destroy(e) for e in self._point_gizmos]
        self._point_gizmos = LoopingList([Entity(parent=self, original_parent=self, position=e, selectable=False, name='PokeShape_point', is_gizmo=True, enabled=False) for e in value])
        LEVEL_EDITOR.entities.extend(self._point_gizmos)

    def edit_mode_getter(self):
        return getattr(self, '_edit_mode', False)

    def edit_mode_setter(self, value):
        self._edit_mode = value

        print('set edit mode', value)
        if value:
            [setattr(e, 'selectable', False) for e in LEVEL_EDITOR.entities if not e == self]
            for e in self._point_gizmos:
                if not e in LEVEL_EDITOR.entities:
                    LEVEL_EDITOR.entities.append(e)

            [setattr(e, 'selectable', True) for e in self._point_gizmos]
            LEVEL_EDITOR.gizmo.subgizmos['y'].enabled = False
            LEVEL_EDITOR.gizmo.fake_gizmo.subgizmos['y'].enabled = False
            self.add_new_point_renderer.enabled = True
            self.collider = None
        else:
            [LEVEL_EDITOR.entities.remove(e) for e in self._point_gizmos if e in LEVEL_EDITOR.entities]
            [setattr(e, 'selectable', True) for e in LEVEL_EDITOR.entities]
            if True in [e in LEVEL_EDITOR.selection for e in self._point_gizmos]: # if point is selected when exiting edit mode, select the poke shape
                LEVEL_EDITOR.selection = [self, ]

            LEVEL_EDITOR.gizmo.subgizmos['y'].enabled = True
            LEVEL_EDITOR.gizmo.fake_gizmo.subgizmos['y'].enabled = True
            self.add_new_point_renderer.enabled = False
            self.collider = 'mesh'
        LEVEL_EDITOR.render_selection()

    def update(self):
        if self.edit_mode:
            if mouse.left or held_keys['d']:
                LEVEL_EDITOR.render_selection()
                self.generate()

    def input(self, key):
        combined_key = input_handler.get_combined_key(key)
        if combined_key == 'tab':
            if not LEVEL_EDITOR.selection:
                self.edit_mode = False

            if self in LEVEL_EDITOR.selection or True in [e in LEVEL_EDITOR.selection for e in self._point_gizmos]:
                self.edit_mode = not self.edit_mode

        if self.edit_mode and (key == 'left mouse down' or key == 'd'):
            if LEVEL_EDITOR.selector.get_hovered_entity():
                return
            points_in_range = [(distance_2d(world_position_to_screen_position(v), mouse.position), v) for v in self.add_new_point_renderer.model.vertices]
            points_in_range = [e for e in points_in_range if e[0] < .075/2]
            points_in_range.sort()

            closest_point = None
            if not points_in_range:
                return

            closest_point = points_in_range[0][1]
            i = self.add_new_point_renderer.model.vertices.index(closest_point)

            new_point = Entity(parent=self, original_parent=self, position=lerp(self._point_gizmos[i].position, self._point_gizmos[i+1].position, .5), selectable=True, is_gizmo=True)
            LEVEL_EDITOR.entities.append(new_point)
            self._point_gizmos.insert(i+1, new_point)
            LEVEL_EDITOR.render_selection()
            if key == 'd':
                LEVEL_EDITOR.quick_grabber.input('d')

        elif key == 'space':
            self.generate()

        elif self.edit_mode and key.endswith(' up'):
            invoke(self.generate, delay=3/60)
