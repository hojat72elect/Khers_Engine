from panda3d.core import AmbientLight as PandaAmbientLight
from panda3d.core import DirectionalLight as PandaDirectionalLight
from panda3d.core import PointLight as PandaPointLight
from panda3d.core import Spotlight as PandaSpotLight

from ursina import Entity, Vec2, Vec3, color, scene
from ursina.prefabs.sky import Sky
from ursina.scripts.property_generator import generate_properties_for_class

class Light(Entity):
    default_values = {'rotation_x':90, }
    def __init__(self, color=color.white, **kwargs):
        super().__init__(**(__class__.default_values | kwargs))

    @property
    def color(self):
        return getattr(self, '_color', color.white)

    @color.setter
    def color(self, value):
        self._color = value
        self._light.setColor(value)

@generate_properties_for_class()
class DirectionalLight(Light):
    def __init__(self, shadow_map_resolution=Vec2(1024,1024), shadows=True, **kwargs):
        super().__init__(**kwargs)
        self._light = PandaDirectionalLight('directional_light')
        node_path = self.attachNewNode(self._light)
        node_path.node().setCameraMask(0b0001)
        render.setLight(node_path)

        self.shadow_map_resolution = shadow_map_resolution
        self._bounds_entity = scene
        self.shadows = shadows

    def shadows_setter(self, value):
        self._shadows = value
        if value:
            self._light.set_shadow_caster(True, int(self.shadow_map_resolution[0]), int(self.shadow_map_resolution[1]))
            self.update_bounds()
        else:
            self._light.set_shadow_caster(False)



    def update_bounds(self, entity=scene):  # update the shadow area to fit the bounds of target entity, defaulted to scene.
        # don't include skydome when calculating shadow bounds
        [e.disable() for e in Sky.instances]

        bounds = entity.get_tight_bounds(self)
        if bounds is not None:
            bmin, bmax = bounds
            lens = self._light.get_lens()
            lens.set_near_far(bmin.z*2, bmax.z*2)
            lens.set_film_offset((bmin.xy + bmax.xy) * .5)
            lens.set_film_size(bmax.xy - bmin.xy)
        else:
            lens = self._light.get_lens()
            lens.set_near_far(1, 100)
            lens.set_film_offset((0, 0))
            lens.set_film_size((1, 1))

        [e.enable() for e in Sky.instances]

        self._bounds_entity = entity

    def look_at(self, target, axis=Vec3.forward):
        super().look_at(target, axis=axis)
        self.update_bounds(self._bounds_entity)

class PointLight(Light):
    def __init__(self, **kwargs):
        super().__init__()
        self._light = PandaPointLight('point_light')
        render.setLight(self.attachNewNode(self._light))

        for key, value in kwargs.items():
            setattr(self, key ,value)

class AmbientLight(Light):
    def __init__(self, **kwargs):
        super().__init__()
        self._light = PandaAmbientLight('ambient_light')
        render.setLight(self.attachNewNode(self._light))

        for key, value in kwargs.items():
            setattr(self, key ,value)

class SpotLight(Light):
    def __init__(self, **kwargs):
        super().__init__()
        self._light = PandaSpotLight('spot_light')
        render.setLight(self.attachNewNode(self._light))

        for key, value in kwargs.items():
            setattr(self, key ,value)
