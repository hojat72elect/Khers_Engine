# this will clear the scene and try to execute the main.py code without
# restarting the program
import ast
import time
from pathlib import Path
from ursina import Entity, application, camera, mesh_importer, print_on_screen, scene, texture_importer, window
from ursina.mesh_importer import load_model

def is_valid_python(code):
   try:
       ast.parse(code)
   except Exception as e:
       return False, e
   return True

def make_code_reload_safe(code):
    newtext = ''
    dedent_next = False

    for line in code.split('\n'):
        if line.strip().endswith('app.run()') or line.strip().endswith('HotReloader()'):
            continue
        if 'eternal=True' in line:
            continue
        if line.startswith('''if __name__ == '__main__':'''):
            dedent_next = True
            continue
        if line and line[0] != ' ':
            dedent_next = False
        if line.strip().startswith('#'):
            newtext += '\n'
            continue
        if dedent_next:
            newtext += line[4:] + '\n'
        else:
            newtext += line + '\n'

    return newtext

class HotReloader(Entity):
    def __init__(self, path=__file__, **kwargs):
        super().__init__(parent=camera.ui, eternal=True, ignore_paused=True)
        self.path = path

        for key, value in kwargs.items():
            setattr(self, key, value)

        self.path = Path(self.path)
        self.hotreload = False   # toggle with f9
        self._original_source_code_content = ''
        self._i = 0
        self.hotkeys = {
            'ctrl+r' : self.reload_code,
            'f5'     : self.reload_code,
            'f6'     : self.reload_textures,
            'f7'     : self.reload_models,
            'f8'     : self.reload_shaders,
            'f9'     : self.toggle_hotreloading,
            }

        self.hotreload_window_settings = dict(size=(window.size[0]/2,window.size[1]/2), always_on_top=True, position=(window.fullscreen_size[0]-window.size[0]/22, 0))

    def input(self, key):
        if key in self.hotkeys:
            self.hotkeys[key]()

    def update(self):
        if self.hotreload:
            self._i += time.dt
            if self._i > .2:
                current_source_code = self.get_source_code()

                if current_source_code != self._original_source_code_content:
                    self.reload_code()
                    self._original_source_code_content = current_source_code

                self._i = 0

    def get_source_code(self):
        with open(self.path, encoding='utf8') as file:
            text = file.read()
        return text

    def toggle_hotreloading(self):
        self.hotreload = not self.hotreload
        print_on_screen(f'<azure>hotreloading: {self.hotreload}')
        if self.hotreload_window_settings:
            for key, value in self.hotreload_window_settings.items():
                setattr(window, key, value)

    def reload_code(self, reset_camera=True):
        if not self.path.exists:
            print('trying to reload, but path does not exist:', self.path)
            return

        with open(self.path, encoding='utf8') as file:
            text = file.read()
            text = make_code_reload_safe(text)

        if not is_valid_python(text):
            print('invalid python code')
            return

        scene.clear()
        if reset_camera:
            camera.position = (0, 0, -20)

        t = time.time()
        try:
            d = dict(locals(), **globals())
            d['__name__'] = '__main__'
            application.paused = True
            exec(text, d, d)

            import __main__
            for key, value in d.items():
                if key in dir(__main__) or key in ('update', 'input'):
                    setattr(__main__, key, value)

            application.paused = False

        except Exception as e:
            print(e)

        print('reloaded in:', time.time() - t)

    def reload_textures(self):
        textured_entities = [e for e in scene.entities if e.texture]
        reloaded_textures = list()

        for e in textured_entities:
            if e.texture.name in reloaded_textures or not hasattr(e.texture, 'path') or not e.texture.path:
                continue

            if e.texture.path.parent.name == application.textures_compressed_folder.name:
                print('texture is made from .psd file', e.texture.path.stem + '.psd')
                texture_importer.compress_textures(e.texture.path.stem)
            print('reloaded texture:', e.texture.path)
            e.texture._texture.reload()
            reloaded_textures.append(e.texture.name)

        return reloaded_textures

    def reload_models(self):
        print('reloading models...')
        entities = [e for e in scene.entities if e.model]
        unique_names = list(set(e.model.name.split('.')[0] for e in entities))
        changed_models = []

        for base_name in unique_names:
            m = load_model(f'{base_name}.blend')
            if m:
                changed_models.append(base_name)
            if not m:
                m = load_model(f'{base_name}.obj', use_deepcopy=True)
                if m:
                    m.save(f'{base_name}.bam')
                    changed_models.append(base_name)

        for e in entities:
            if e.model:
                name = e.model.name.split('.')[0]
                if name in changed_models:
                    e.model = None
                    e.model = name
                    e.origin = e.origin
                    print('reloaded model:', name)

    def reload_shaders(self):
        import ursina

        for shader in ursina.shader.imported_shaders.values():
            with open(shader.path, encoding='utf8') as f:
                try:
                    print('trying to reload:', shader.path.name)
                    text = f.read()

                    geom = ''
                    if r"geometry='''" in text:
                        geom = text.split(r"geometry='''", 1)[1].split("'''", 1)[0]
                        print('geommmmmmmmmmmmmmm', geom)

                    vert = ''
                    if r"verte ='''" in text:
                        vert = text.split(r"vertex='''", 1)[1].split("'''", 1)[0]

                    frag = text.split(r"fragment='''", 1)[1].split("'''", 1)[0]

                    if geom:
                        shader.geometry = geom
                    if vert:
                        shader.vertex = vert
                    shader.fragment = frag
                    shader.compile()

                    for e in scene.entities:
                        if hasattr(e, '_shader') and e.shader == shader:
                            e.clearShader()
                            e.shader = e.shader

                    print('reloaded shader:', shader.path.name)
                except Exception as e:
                    print('failed to reload shader:', shader.path.name, 'error:', e)
                    pass
