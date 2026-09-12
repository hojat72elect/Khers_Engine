from ursina import EditorCamera, Sky, Ursina, camera, held_keys

if __name__ == "__main__":
    app = Ursina()
    Sky(texture="sky_sunset")
    camera.fov = 90
    EditorCamera()

    def input(key):
        if key == "-":
            camera.clip_plane_far -= 100 + (held_keys["control"] * 10)
            print(camera.clip_plane_far)
        elif key == "+":
            camera.clip_plane_far += 100 + (held_keys["control"] * 10)
            print(camera.clip_plane_far)

    app.run()
