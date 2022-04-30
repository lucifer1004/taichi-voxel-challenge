from scene import Scene, MAT_LIGHT, MAT_LAMBERTIAN
import taichi as ti
from taichi.math import *

scene = Scene(exposure=10)
scene.set_floor(-0.05, (1.0, 1.0, 1.0))
scene.set_background_color((1.0, 0, 0))


@ti.kernel
def initialize_voxels():
    for i in range(31):
        for j in range(31):
            for k in range(31):
                mat = MAT_LIGHT if (i + j + k) % 10 == 0 else MAT_LAMBERTIAN
                scene.set_voxel(vec3(i, j, k), mat, vec3(
                    0.9 - i * 0.03, 0.9 - j * 0.03, 0.9 - k * 0.03))


initialize_voxels()

scene.finish()
