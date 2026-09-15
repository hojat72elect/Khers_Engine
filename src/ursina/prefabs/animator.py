from ursina import *

@generate_properties_for_class()
class Animator:
    def __init__(self, animations=None, start_state='', pause_disabled=True):

        self.animations = animations    # dict
        self.pause_disabled = pause_disabled
        if not start_state and self.animations:
            start_state = list(self.animations.keys())[0]

        self.start_state = start_state
        self._state = None
        self.state = start_state

    def state_setter(self, value):
        if value not in self.animations:
            print_warning(self, 'has no animation:', value)

        elif not self._state == value:
            # only show set state and disable the rest
            for name, entity in self.animations.items():
                if entity:
                    entity.enabled = value == name
                    if self.pause_disabled and hasattr(entity, 'pause') and not entity.enabled:
                        [anim.pause() for anim in entity.animations]

            entity = self.animations[value]
            if entity:
                if hasattr(entity, 'start') and callable(entity.start):
                    entity.start()
                if hasattr(entity, 'animations'):
                    [anim.start() for anim in entity.animations]

        self._state = value
