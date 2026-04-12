from datatypes import *
from generate_triangle_data import make_triangular_prism, NewStructureProperties
from viewer import show_result
from renderer import render_onto_screen
from write_image_file import write_image_file
import math


def make_empty_screen(dim: int) -> Screen:
    screen: Screen = []

    for _ in range(dim):
        screen.append([(0., 0., 0.) for __ in range(dim)])

    return screen

def load_obj_file(file_path: str, color: Color) -> list[Triangle]:
    vertices: list[Vec3] = []
    triangles: list[Triangle] = []

    with open(file_path, 'r') as f:
        for line in f:
            parts = line.strip().split()

            if not parts:
                continue

            # vertices
            if parts[0] == "v":
                assert len(parts) == 4
                x = float(parts[1])
                y = float(parts[2])
                z = float(parts[3])
                vertices.append((x, y, z))

            # faces
            elif parts[0] == "f":
                indices = []
                assert len(parts) == 4
                for p in parts[1:]:
                    vertex_index = int(p.split("/")[0]) - 1 # 1 -indexed
                    indices.append(vertex_index)

                triangles.append(Triangle(
                    vertices=(
                        vertices[indices[0]],
                        vertices[indices[1]],
                        vertices[indices[2]]

                    ),
                    color=color
                ))

    return triangles


def main():
    screen_dim = 200

    screen = make_empty_screen(screen_dim)

    scene = Scene(
        triangles = [
            *make_triangular_prism(
                color_1=(0.412, 1.0, 0.706),  # mint green
                color_2=(1.0, 0.412, 0.706),  # hot pink
                props=NewStructureProperties(
                    rotations_rads = (-math.pi / 8, math.pi / 8, 0.),
                    scale = (0.25, 0.25, 0.25),
                    origin = (0.5, 0.5, 3.)
                )
            ),
            *make_triangular_prism(
                color_1=(0.412, 1.0, 0.706),  # mint green
                color_2=(1.0, 0.412, 0.706),  # hot pink
                props=NewStructureProperties(
                    rotations_rads=(0, math.pi / 8, math.pi / 8),
                    scale=(0.1, 0.1, 0.1),
                    origin=(0.8, 0.8, 3.)
                )
            ),
            *NewStructureProperties(
                rotations_rads = (math.pi / 4, math.pi / 4, math.pi / 4),
                scale = (0.1, 0.1, 0.1),
                origin = (0.2, 0.2, 3.),
            ).apply(
                load_obj_file(
                    file_path = "models/cube.obj",
                    color = (1., 0., 0.)
                )
            ),

            *NewStructureProperties(
                rotations_rads=(-math.pi / 16, math.pi / 16, 0),
                scale=(0.1, 0.1, 0.1),
                origin=(0.4, 0.8, 1.5),
            ).apply(
                load_obj_file(
                    file_path="models/hollow_long_cube.obj",
                    color=(0., 0., 1.)
                )
            ),

            *NewStructureProperties(
                rotations_rads=(-math.pi / 16, 9 * math.pi / 8, 0),
                scale=(0.03, 0.03, 0.03),
                origin=(0.85, 0.4, 1.5),
            ).apply(
                load_obj_file(
                    file_path="models/miku.obj",
                    color=(0.122, 1., 0.941)
                )
            ),
            # Triangle(
            #     vertices = (
            #         # △
            #         (0.35, 0.25, 1.0), # bottom left
            #         (0.75, 0.75, 3.0), # top
            #         (0.75, 0.25, 2.0) # bottom right
            #     ),
            #     color = (1., 0., 0.)  # red
            # ),
            # Triangle(
            #     vertices=(
            #         # △
            #         (0.15, 0.55, 3.0),
            #         (0.85, 0.85, 5.0),
            #         (0.85, 0.25, 4.0)
            #     ),
            #     color=(0., 1., 0.)  # green
            # )
        ],
        light = (0.5, 0.5, 0.5),
        background_color =  (1., 1., 1.)  # white
    )

    print("Rendering...")
    render_onto_screen(screen, screen_dim, scene)
    print("Rendered, saving...")

    out_filename = "result.png"

    write_image_file(screen, screen_dim, out_filename)

    print(f"Saved as {out_filename}! Showing in window...")

    show_result(
        screen,
        scale = 1,  # 30 monitor pixels per scene pixel
        pad = 0,  # 2 pixels' worth of padding on each side,
        debug = False
    )

if __name__ == '__main__':
    main()
