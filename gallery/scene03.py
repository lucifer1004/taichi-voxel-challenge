from scene import Scene, MAT_LAMBERTIAN, MAT_LIGHT
import taichi as ti
from taichi.math import *

scene = Scene(exposure=1, voxel_edges=0.0)
scene.set_floor(-50, (1.0, 1.0, 1.0))
scene.set_background_color((1.0, 1.0, 1.0))
scene.set_directional_light((0.5, 0.5, 0.5),
                            0.02, (1.0, 1.0, 1.0))

GREEN = vec3(0.0, 1.0, 0.0)
WHITE = vec3(1.0, 1.0, 1.0)
BLUE = vec3(0.0, 0.0, 1.0)
BLACK = vec3(0.0, 0.0, 0.0)
OUTER = (56, 26)
INNER = (38, 16)


@ti.func
def should_be_white(i, j):
    return (abs(i) <= OUTER[0] and abs(j) <= OUTER[1]) and (
        abs(i) == OUTER[0] or i == 0 or (9 < ti.sqrt(i ** 2 + j ** 2) <= 10) or
        abs(j) == OUTER[1] or (abs(i) == INNER[0] and abs(j) <= INNER[1]) or
        (abs(i) >= INNER[0] and abs(j) == INNER[1]) or
        (4 < ti.sqrt((i - OUTER[0]) ** 2 + (j - OUTER[1]) ** 2) <= 5) or
        (4 < ti.sqrt((i + OUTER[0]) ** 2 + (j - OUTER[1]) ** 2) <= 5) or
        (4 < ti.sqrt((i - OUTER[0]) ** 2 + (j + OUTER[1]) ** 2) <= 5) or
        (4 < ti.sqrt((i + OUTER[0]) ** 2 + (j + OUTER[1]) ** 2) <= 5))


@ti.func
def plot_grid(xs, xe, ys, ye, zs, ze, color, probability=1.0):
    for x in range(xs, xe + 1):
        for y in range(ys, ye + 1):
            for z in range(zs, ze + 1):
                if ti.random() < probability:
                    scene.set_voxel(vec3(x, z, y), MAT_LAMBERTIAN, color)


@ti.func
def plot_sphere(x, y, z, r, color):
    for i in range(x - r, x + r + 1):
        for j in range(y - r, y + r + 1):
            for k in range(z - r, z + r + 1):
                if ti.sqrt((i - x) ** 2 + (j - y) ** 2 + (k - z) ** 2) <= r:
                    scene.set_voxel(vec3(i, k, j), MAT_LIGHT, color)


@ti.func
def plot_player(x, y, shoes=WHITE, clothes=BLUE, skin=WHITE, hair=BLACK):
    plot_grid(x - 6, x - 2, y - 6, y + 1, 1, 2, shoes)
    plot_grid(x + 2, x + 6, y - 6, y + 1, 1, 2, shoes)
    plot_grid(x - 6, x - 2, y - 6, y - 3, 3, 7, clothes)
    plot_grid(x + 2, x + 6, y - 6, y - 3, 3, 7, clothes)
    plot_grid(x - 6, x - 2, y - 6, y - 3, 8, 8, skin)
    plot_grid(x + 2, x + 6, y - 6, y - 3, 8, 8, skin)
    plot_grid(x - 7, x - 1, y - 7, y - 2, 9, 16, clothes)
    plot_grid(x + 1, x + 7, y - 7, y - 2, 9, 16, clothes)
    plot_grid(x - 7, x + 7, y - 7, y - 2, 17, 17, WHITE)
    plot_grid(x - 7, x + 7, y - 7, y - 2, 18, 25, clothes)
    plot_grid(x - 9, x + 9, y - 7, y - 2, 26, 29, clothes)
    plot_grid(x - 17, x - 10, y - 6, y - 3, 27, 27, skin)
    plot_grid(x + 10, x + 17, y - 6, y - 3, 27, 27, skin)
    plot_grid(x - 18, x - 10, y - 6, y - 3, 28, 28, skin)
    plot_grid(x + 10, x + 18, y - 6, y - 3, 28, 28, skin)
    plot_grid(x - 3, x + 3, y - 8, y - 2, 29, 30, skin)
    plot_grid(x - 5, x + 5, y - 10, y, 31, 40, skin)
    plot_grid(x - 5, x + 5, y - 10, y, 41, 41, hair)
    plot_grid(x - 5, x + 5, y - 10, y, 42, 42, hair, 0.8)


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

    plot_player(30, -10)
    plot_player(-20, 24, vec3(0.4, 0.5, 0.2), vec3(1.0, 0.0, 0.1),
                vec3(0.8, 0.6, 0.4), vec3(0.8, 0.2, 0.3))

    plot_sphere(15, 10, 5, 5, WHITE)


initialize_voxels()

scene.finish()
