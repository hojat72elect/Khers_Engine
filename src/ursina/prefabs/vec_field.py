from ursina import camera, color, mouse, round_to_closest
from ursina.entity import Entity
from ursina.prefabs.button import Button
from ursina.prefabs.input_field import ContentTypes, InputField
from ursina.text import Text
from ursina.vec2 import Vec2

class VecField(Button):
    def __init__(self, default_value=Vec2.zero, character_limit=8, content_type=ContentTypes.math, **kwargs):
        kwargs = dict(parent=camera.ui, scale=(.5,.05), character_limit=character_limit, text='', text_origin=(-.5,0), color=color.black90) | kwargs
        super().__init__(**kwargs)
        if isinstance(default_value, int | float):
            default_value = [default_value, ]

        self.default_value = default_value
        self.fields = []
        self.on_value_changed = None
        w = 1 / len(default_value) *.5

        self.highlight_color = self.color
        self.pressed_color = self.color
        self._dragging_on = None
        self._value_on_drag_start = []
        self._temp_value = []

        self.data_type = float
        if isinstance(default_value[0], int):
            self.data_type = int
            content_type = ContentTypes.int_math

        for i in range(len(default_value)):
            field = InputField(str(self.default_value[i])[:self.character_limit], character_limit=self.character_limit, model='quad', parent=self, limit_content_to=content_type,
                x=(i*w)+w/2, scale=(w,1), z=-1, color=color._8, font=Text.default_monospace_font, submit_on=['enter','tab'])
            field.grid = Entity(parent=field, model='wireframe_quad', color=color.dark_gray, z=-1)
            field.text_field.scale *= .75
            field.on_submit = self.convert_text_to_vector
            # field.on_value_changed = self.convert_text_to_vector
            field.text_field.shortcuts['select_all'] = ('double click', )
            field.text_field.shortcuts['select_word'] = []
            self.fields.append(field)

        self.value = default_value


    def convert_text_to_vector(self):
        vector = []
        for i, field in enumerate(self.fields):
            try:
                # value = type(self.default_value[i])(eval(field.text[:self.character_limit]))
                value = self.data_type(eval(field.text[:self.character_limit]))
                if isinstance(value, self.data_type):
                    vector.append(value)
                    field.text_field.text_entity.text = str(value)[:8]
            except: # invalid/incomplete math
                print('invalid')
                return
        # print('vector:', vector, 'fotype', type(self.default_value))
        if not isinstance(self.default_value, tuple | list):
            vector = type(self.default_value)(*vector)

        self.value = vector


    @property
    def value(self):
        if len(self._value) == 1:
            return self._value[0]
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        if len(value) == 1:
            value = str(value[0])

        if self.on_value_changed is not None:
            self.on_value_changed()

        for i, field in enumerate(self.fields):
            # print('---------', field.text, str(value[i]))
            field.text = str(value[i])[:self.character_limit]


    def input(self, key):
        super().input(key)
        if key == 'left mouse down':
            self._dragging_on = None
            self._temp_value = [e for e in self._value]

            for i, field in enumerate(self.fields):
                if field.hovered:
                    self._dragging_on = field
                    self._value_on_drag_start = self.value
                    return

        elif key == 'left mouse up' and self._dragging_on:
            self._dragging_on = None
            self.value = self._value
            self._temp_value = self._value


    def update(self):
        if mouse.left and self._dragging_on and not self._dragging_on.active:
            # print('drag on:', self._dragging_on, mouse.velocity.x)
            idx = self.fields.index(self._dragging_on)
            if self.data_type is float:
                self._temp_value[idx] += mouse.velocity.x
                self._value = [round_to_closest(e, .01) for e in self._temp_value]
            elif self.data_type is int:
                self._temp_value[idx] += mouse.velocity.x * 10
                self._value = [int(e) for e in self._temp_value]

            for i, field in enumerate(self.fields): # set text temporarily while dragging
                field.text_field.text_entity.text = str(self._value[i])[:self.character_limit]
