from scene import Scene, MAT_LIGHT, MAT_LAMBERTIAN
import taichi as ti
from taichi.math import *

scene = Scene(exposure=1)
scene.set_floor(-50, (1.0, 1.0, 1.0))
scene.set_background_color((1.0, 1.0, 1.0))
scene.set_directional_light((0.5, 0.5, 0.5),
                            0.02, (1.0, 1.0, 1.0))


@ti.kernel
def initialize_voxels():
    for i in range(-31, 32):
        for j in range(-31, 32):
            for k in range(-31, 32):
                mat = MAT_LIGHT if i == j == k else MAT_LAMBERTIAN
                distance = ti.sqrt(i**2 + j**2 + k**2)
                if distance < 30:
                    scene.set_voxel(vec3(i, j, k), mat, vec3(1.0, 1.0, 1.0))
                elif distance < 31:
                    light = distance - 30
                    scene.set_voxel(vec3(i, j, k), MAT_LAMBERTIAN,
                                    vec3(light, light, light))


initialize_voxels()

scene.finish()
