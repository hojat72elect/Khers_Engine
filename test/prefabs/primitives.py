from ursina import Ursina
from ursina.prefabs.primitives import RedCube, VioletSphere, YellowCube

if __name__ == "__main__":
    """procedurally generate classes like RedCube, GreenCube, BlueSphere and so on."""
    app = Ursina()
    RedCube()
    VioletSphere(x=1)
    YellowCube(x=2, scale=(10, 1, 10), texture="white_cube", texture_scale=(10, 10))
    app.run()
