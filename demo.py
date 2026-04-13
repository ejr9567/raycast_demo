from datatypes import *
from generate_triangle_data import make_triangular_prism, NewStructureProperties
from viewer import show_result
from renderer import render_onto_screen
from write_image_file import write_image_file
import math
import time
from scenes import scene_1, scene_2


def make_empty_screen(dim: int) -> Screen:
    screen: Screen = []

    for _ in range(dim):
        screen.append([(0., 0., 0.) for __ in range(dim)])

    return screen


sizes = (16, 32, 64, 128, 256, 512)


def main():
    max_screen_dim = 512

    screen = make_empty_screen(max_screen_dim)

    scene = scene_2
    for screen_dim in sizes:
        print(f"Rendering at {screen_dim} x {screen_dim}...")
        start_time = time.perf_counter()
        render_onto_screen(screen, screen_dim, scene)
        end_time = time.perf_counter()

        delta = end_time - start_time

        print(f"Dimension {screen_dim} took {delta:e} seconds")

    out_filename = "result.png"

    write_image_file(screen, max_screen_dim, out_filename)

    print(f"Saved as {out_filename}! Showing in window...")

    show_result(
        screen,
        scale = 30,  # 30 monitor pixels per scene pixel
        pad = 0,  # 2 pixels' worth of padding on each side,
        debug = False
    )

if __name__ == '__main__':
    main()
