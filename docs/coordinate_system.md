## Coordiante System

The coordinate system that our entities follow is like this: 

```
            y (up)
            |
            |
(forward) z |
          \ |
           \|
            *---------- x (right)
```

The coordinate system that the UI elements follow is like this: 

```
                      (-.5, .5)           (.5, .5)
  (window.top_right)_______|__(window.top)____|_______(window.top_right)
                   |       '                  '       |
                   |       '                  '       |
                   |       '                  '       |
                   |       '                  '       |
       (window.left)       '      (0, 0)      '       (window.right or Vec2(.5*window.aspect_ratio, 0))
                   |       '                  '       |
                   |       '                  '       |
                   |       '                  '       |
                   |_______'__________________'_______|
(window.bottom_left)       |  (window.bottom) |       (window.bottom_right)
                      (-.5, -.5)          (.5, -.5)
```

## Rotation

Positive rotation means rotating clockwise around the axis, looking from the outside in.
The exception to this is the z-axis, which is counter-clockwise.
While this is inconsistent, it makes setting rotation_z in 2D also clockwise.

Although generally not recommended, the rotation direction can be changed by
setting `Entity.rotation_directions` (default: (-1,-1,1)). **My suggestion is to never do that.**

In general when working with rotation you'll want to only set one of the axes at the same time.
For more complicated rotations you can use `entity.look_at(position)`, `entity.look_at_2d(position)`
or even set/get .quaternion if you're comfortable with that. For continuous rotation, `entity.rotate(amount)` can be good as it will add a rotation to the current rotation.

```
           _______
          /
          \->
    __
   /  \     y
   v  |     |
      |  z  |                __
          \ |               /  \
           \|               v   |
            *---------- x       |
                                |
```

## Origin

Setting the origin will move the origin point of the model.
This can be especially useful when working with the UI.

```
             (-.5,.5)
+---------+      0---------+
|  (0,0)  |      |         |
|    0    |      |         |
|         |      |         |
+---------+      +---------+

   (0,.5)
+----0----+      +---------+
|         |      |         |
|         |      |         0 (.5,0)
|         |      |         |
+---------+      +---------+
```