from datatypes import Color, Screen, Scene, Vec3


def screen_space_to_world_space(screen_x, screen_y, screen_dim) -> Vec3:
    world_x = (screen_x + 0.5) / screen_dim
    world_y = (screen_y + 0.5) / screen_dim
    world_z = 0.0

    return world_x, world_y, world_z


def render_onto_screen(
    screen: Screen,
    dim: int,

    scene: Scene
):
    for y in range(dim):
        for x in range(dim):
            world_coords = screen_space_to_world_space(x, y, dim)

            print(f"({x}, {y}) = {world_coords}")

            # TODO remove this part:
            r = x / dim
            g = y / dim
            b = 0.5
            screen[y][x] = (r, g, b)
