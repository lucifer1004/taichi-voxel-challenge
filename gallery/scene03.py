from scene import Scene, MAT_LAMBERTIAN
import taichi as ti
from taichi.math import *

scene = Scene(exposure=1, voxel_edges=0.0)
scene.set_floor(-50, (1.0, 1.0, 1.0))
scene.set_background_color((1.0, 1.0, 1.0))
scene.set_directional_light((0.5, 0.5, 0.5),
                            0.02, (1.0, 1.0, 1.0))

GREEN = vec3(0.0, 1.0, 0.0)
WHITE = vec3(1.0, 1.0, 1.0)
OUTER = (56, 26)
INNER = (38, 16)


@ti.func
def should_be_white(i, j):
    return (abs(i) <= OUTER[0] and abs(j) <= OUTER[1]) and (abs(i) == OUTER[0] or i == 0 or (9 < ti.sqrt(i ** 2 + j ** 2) <= 10) or abs(j) == OUTER[1] or (abs(i) == INNER[0] and abs(j) <= INNER[1]) or (abs(i) >= INNER[0] and abs(j) == INNER[1]) or (4 < ti.sqrt((i - OUTER[0]) ** 2 + (j - OUTER[1]) ** 2) <= 5) or (4 < ti.sqrt((i + OUTER[0]) ** 2 + (j - OUTER[1]) ** 2) <= 5) or (4 < ti.sqrt((i - OUTER[0]) ** 2 + (j + OUTER[1]) ** 2) <= 5) or (4 < ti.sqrt((i + OUTER[0]) ** 2 + (j + OUTER[1]) ** 2) <= 5))


@ti.kernel
def initialize_voxels():
    for i in range(-63, 64):
        for j in range(-31, 32):
            color = WHITE if should_be_white(i, j) else GREEN
            scene.set_voxel(vec3(i, 0, j), MAT_LAMBERTIAN, color)

    for i in range(OUTER[0], 64):
        for j in range(9):
            for k in range(10):
                if (abs(j) == 8 or k == 9 or abs(i) == 63) and (i + j + k) % 2 == 0:
                    scene.set_voxel(vec3(i, k, j), MAT_LAMBERTIAN, WHITE)
                    scene.set_voxel(vec3(-i, k, j), MAT_LAMBERTIAN, WHITE)
                    scene.set_voxel(vec3(i, k, -j), MAT_LAMBERTIAN, WHITE)
                    scene.set_voxel(vec3(-i, k, -j), MAT_LAMBERTIAN, WHITE)


initialize_voxels()

scene.finish()
