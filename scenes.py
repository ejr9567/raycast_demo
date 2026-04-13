from datatypes import Scene
from generate_triangle_data import make_triangular_prism, NewStructureProperties, load_obj_file
import math


# noinspection PyArgumentList
scene_1 = Scene(
    name = "Scene 1",
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
            color_1=(1.0, 0.0, 0.0),  # mint green
            color_2=(0.0, 1.0, 1.0),  # hot pink
            props=NewStructureProperties(
                rotations_rads=(0, math.pi / 8, math.pi / 8),
                scale=(0.1, 0.1, 0.1),
                origin=(0.8, 0.8, 3.)
            )
        ),
        *make_triangular_prism(
            color_1=(232/255, 115/255, 5/255),  # mint green
            color_2=(39/255, 108/255, 228/255),  # hot pink
            props=NewStructureProperties(
                rotations_rads = (0, -math.pi / 8, -math.pi / 8),
                scale = (0.085, 0.085, 0.085),
                origin = (0.15, 0.7, 3.)
            )
        ),
        *NewStructureProperties(
            rotations_rads = (math.pi / 4, math.pi / 4, math.pi / 4),
            scale = (0.09, 0.09, 0.09),
            origin = (0.2, 0.2, 3.),
        ).apply(
            load_obj_file(
                file_path = "models/cube.obj",
                color = (1., 0., 0.)
            )
        ),
        *NewStructureProperties(
            rotations_rads = (-math.pi / 4, -math.pi / 4, -math.pi / 4),
            scale = (0.07, 0.07, 0.07),
            origin = (0.8, 0.2, 3.),
        ).apply(
            load_obj_file(
                file_path = "models/cube.obj",
                color = (1., 1., 0.)
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
            rotations_rads=(math.pi / 16, -math.pi / 16, 0),
            scale=(0.05, 0.05, 0.05),
            origin=(0.6, 0.3, 1.5),
        ).apply(
            load_obj_file(
                file_path="models/hollow_long_cube.obj",
                color=(0., 1., 0.)
            )
        ),
        *NewStructureProperties(
            rotations_rads=(- math.pi / 16, -math.pi / 16, math.pi / 8),
            scale=(0.03, 0.03, 0.003),
            origin=(0.9, 0.175, 1.5),
        ).apply(
            load_obj_file(
                file_path="models/hollow_long_cube.obj",
                color=(1., 0., 0.)
            )
        )
    ],
    light = (0.5, 0.5, 0.5),
    background_color =  (1., 1., 1.)  # white
)

scene_2 = Scene(
    name = "Scene 2",
    triangles = [
        *NewStructureProperties(
            rotations_rads=(-math.pi / 16, 9 * math.pi / 8, 0),
            scale=(0.04, 0.04, 0.04),
            origin=(0.8, 0.43, 1.5),
        ).apply(
            load_obj_file(
                file_path="models/miku.obj",
                color=(0.122, 1., 0.941)
            )
        ),
        *NewStructureProperties(
            rotations_rads=(0, 7 * math.pi /8, 0),
            scale=(0.25, 0.25, 0.25),
            origin=(0.2, 0.5, 1.5),
        ).apply(
            load_obj_file(
                file_path="models/spiderman.obj",
                color=(0x44/255, 0x7B/255, 0xBE/255)
            )
        ),
        *NewStructureProperties(
            rotations_rads=(-math.pi/8,-math.pi/8, 0),
            scale=(0.06, 0.06, 0.06),
            origin=(0.6, 0.8, 5),
        ).apply(
            load_obj_file(
                file_path="models/delorean.obj",
                color=(193/255, 177/255, 214/255)
            )
        ),
        *NewStructureProperties(
            rotations_rads=(- math.pi / 8, -math.pi, -math.pi / 8),
            scale=(0.065, 0.065, 0.065),
            origin=(0.49, 0.45, 1.5),
        ).apply(
            load_obj_file(
                file_path="models/mario.obj",
                color=(0xEE / 255, 0x4E/255, 0x4B/255)
            )
        ),
         *NewStructureProperties(
            rotations_rads=( 0 , - math.pi /16 , -math.pi / 16),
            scale=(0.3, 0.3, 0.3),
            origin=(0.2, 0.25, 1.5),
        ).apply(
            load_obj_file(
                file_path="models/mw_er.obj",
                color=(120 / 255, 81/255, 169/255)
            )
        )
    ],
    light = (0.5, 0.9, 1),
    background_color =  (0.8, 0.8, 0.8)  # light gray
)


scenes = [scene_1, scene_2]
