from datatypes import *
from dataclasses import dataclass


def screen_space_to_world_space(screen_x, screen_y, screen_dim) -> Vec3:
    world_x = (screen_x + 0.5) / screen_dim
    world_y = (screen_y + 0.5) / screen_dim
    world_z = 0.0

    return world_x, world_y, world_z


def distance(vec1: Vec3, vec2: Vec3) -> float:
    # TODO
    return 0.


@dataclass
class CollisionResult:
    triangle: Triangle
    hit: bool
    distance: float


def collision_between_ray_and_triangle(ray: Ray, triangle: Triangle) -> CollisionResult:
    # TODO
    return CollisionResult(
        triangle = triangle,
        hit = True,
        distance = 0.
    )


def perform_raycast(ray: Ray, triangles: tuple[Triangle]) -> CollisionResult | None:
    min_hit: CollisionResult | None = None

    for triangle in triangles:
        result = collision_between_ray_and_triangle(ray, triangle)
        if not result.hit:
            continue

        if min_hit is None:
            min_hit = result
            continue

        if result.distance < min_hit.distance:
            min_hit = result

    return min_hit

def render_onto_screen(
    screen: Screen,
    dim: int,

    scene: Scene
):
    background_color = (0., 0., 0.)

    for y in range(dim):
        for x in range(dim):
            world_coords = screen_space_to_world_space(x, y, dim)

            print(f"({x}, {y}) = {world_coords}")

            ray = Ray(
                origin = world_coords,
                direction = (0., 0., 1.)  # into the world
            )

            raycast_result = perform_raycast(ray, scene.triangles)
            if raycast_result is None:
                color = background_color
            else:
                color = raycast_result.triangle.color

            screen[y][x] = color
