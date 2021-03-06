from scene import Scene, MAT_LAMBERTIAN, MAT_LIGHT
import taichi as ti
from taichi.math import *

scene = Scene(exposure=1, voxel_edges=0.01)
scene.set_floor(0.0, (1.0, 1.0, 1.0))
scene.set_background_color((1.0, 1.0, 1.0))
scene.set_directional_light((0.5, 0.5, 0.5),
                            0.05, (0.2, 0.2, 0.2))


@ti.func
def random_walk(xl, xu, yl, yu, zl, zu, rl, ru, gl, gu, bl, bu, num=1000):
    x = (xl + xu) // 2
    y = (yl + yu) // 2
    z = (zu + zu) // 2
    r = (rl + ru) // 2
    g = (gl + gu) // 2
    b = (bl + bu) // 2

    ti.loop_config(serialize=True)
    for _ in range(num):
        v = ti.random(int) % 6
        if v == 0:
            x = x - 1 if x - 1 >= xl else xu
        elif v == 1:
            x = x + 1 if x + 1 <= xu else xl
        elif v == 2:
            y = y - 1 if y - 1 >= yl else yu
        elif v == 3:
            y = y + 1 if y + 1 <= yu else yl
        elif v == 4:
            z = z - 1 if z - 1 >= zl else zu
        else:
            z = z + 1 if z + 1 <= zu else zl

        v = ti.random(int) % 6
        if v == 0:
            r = r - 1 if r - 1 >= rl else ru
        elif v == 1:
            r = r + 1 if r + 1 <= ru else rl
        elif v == 2:
            g = g - 1 if g - 1 >= gl else gu
        elif v == 3:
            g = g + 1 if g + 1 <= gu else gl
        elif v == 4:
            b = b - 1 if b - 1 >= bl else bu
        else:
            b = b + 1 if b + 1 <= bu else bl

        mat = MAT_LIGHT if (11 * x + 3 * y + 5 *
                            z) % 7 == 0 else MAT_LAMBERTIAN
        scene.set_voxel(vec3(x, y, z), mat, vec3(r, g, b) * 0.01)


@ ti.kernel
def initialize_voxels():
    random_walk(-63, 63, 0, 0, -63, 63, 20, 40, 60,
                100, 20, 40, 100000)
    random_walk(-25, 25, 1, 51, -25, 25, 0, 100, 0,
                100, 0, 100, 50000)
    for x in range(-64, 64):
        for y in range(-64, 64):
            _, color = scene.get_voxel(vec3(x, 0, y))
            if color[1] < 0.6:
                scene.set_voxel(vec3(x, 0, y), MAT_LAMBERTIAN, vec3(
                    ti.random() * 0.2 + 0.1, ti.random() * 0.2 + 0.1, ti.random() * 0.2 + 0.8))


initialize_voxels()

scene.finish()
