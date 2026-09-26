# Animation

## SpriteSheetAnimation (2D)

Use a sprite sheet to make an animation. A sprite sheet is an image
containing all of the animation frames in on image, laid out in a grid.

[SpriteSheetAnimation Documentation](https://www.ursinaengine.org/api_reference.html#SpriteSheetAnimation)

## Animation (2D)

Loads an image sequence or a .gif as an animation. for more info, look at [Animation Documentation](https://www.ursinaengine.org/api_reference.html#Animation)

## Actor (3D)

For skeletal animations you can use panda3d's Actor.
Export the model as .glft/.glb since those formats support
mesh data, texture data, animations and more, all in one file.

``` py
from ursina import *
from direct.actor.Actor import Actor

app = Ursina()

entity = Entity()
#animations are stored within the file
actor = Actor("filename.gltf")
actor.reparent_to(entity)

actor.loop("animation_name")  # use .play() instead of loop() to play it once.
app.run()
```

See the [panda3d documentation](https://docs.panda3d.org/1.10/python/programming/models-and-actors/actor-animations) for more info.

## FrameAnimation3D (3D)

[FrameAnimation3D Documentation](https://www.ursinaengine.org/api_reference.html#FrameAnimation3D)

`FrameAnimation3d` loads a sequence of models and cycles through them so it looks like it animates.
This is a memory intensive option, so it's recommended to not have a very high poly count.
With this method, you can't interpolate animations or move a single bone like you can with Actor.
However, `FrameAnimation3D` is a very solid solution that is very unlikely to break or produce
bugs like skeletal animations often can. Also, since every frame is unique, it's possible to
adjust each frame individually.

First, export your animation as a sequence of 3d models.
Assuming you have a bunch of models named `run_cycle_000.obj`, `run_cycle_001.obj`, `run_cycle_002.obj` and so on,
you can load the animation like this:

``` py
FrameAnimation3d('run_cycle_')
```