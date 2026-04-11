from datatypes import *
from dataclasses import dataclass


def screen_space_to_world_space(screen_x, screen_y, screen_dim) -> Vec3:
    world_x = (screen_x + 0.5) / screen_dim
    world_y = (screen_y + 0.5) / screen_dim
    world_z = 0.0

    return world_x, world_y, world_z


def distance(vec1: Vec3, vec2: Vec3) -> float:
    # Difference along x axis
    x_diff = vec1[0] - vec2[0]

    # Difference along y axis
    y_diff = vec1[1] - vec2[1]

    # Difference along z axis
    z_diff = vec1[2] - vec2[2]

    # Take square root of sum of differences squared
    distance = (x_diff * x_diff + y_diff * y_diff + z_diff * z_diff) ** 0.5

    return distance


@dataclass
class CollisionResult:
    triangle: Triangle
    hit: bool
    distance: float


def cross_product(a: Vec3, b: Vec3) -> Vec3:
    # a X b = < a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0] >
    return (

        (a[1] * b[2]) - (a[2] * b[1]),
        (a[2] * b[0]) - (a[0] * b[2]),
        (a[0] * b[1]) - (a[1] * b[0])

    )

def dot_product(a: Vec3, b: Vec3) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

def collision_between_ray_and_triangle_moller(ray: Ray, triangle: Triangle) -> CollisionResult:

    # Unpack triangle vertices
    v0, v1, v2 = triangle.vertices

    # SUB(edge1, vert1, vert0)
    edge1 = (v1[0] - v0[0], v1[1] - v0[1], v1[2] - v0[2])

    # SUB(edge2, vert2, vert0)
    edge2 = (v2[0] - v0[0], v2[1] - v0[1], v2[2] - v0[2])

    # CROSS(pvec, dir, edge2)
    p_vector = cross_product(ray.direction, edge2)

    # det = DOT(edge1, pvec)
    determinant = dot_product(edge1, p_vector)

    if determinant == 0: # we are parallel
        return CollisionResult (
            triangle = triangle,
            hit = False,
            distance= 0.0,
        )

    # inv_det = 1.0 / det
    inverse_determinant = 1 / determinant

    # calculate distance from v0 to ray origin
    t_vector = (ray.origin[0] - v0[0], ray.origin[1] - v0[1], ray.origin[2] - v0[2])

    # Calculate U and make sure it is within triangle bounds
    u = dot_product(t_vector, p_vector) * inverse_determinant

    if (u < 0.0) or (u > 1.0):
        return CollisionResult (
            triangle = triangle,
            hit = False,
            distance= 0.0,
        )

    # Calculate Q vector
    q_vector = cross_product(t_vector, edge1)

    # Calculate V and make sure it is within triangle bounds
    v = dot_product(ray.direction, q_vector) * inverse_determinant

    if (v < 0.0) or (v > 1.0):
        return CollisionResult (
            triangle = triangle,
            hit = False,
            distance= 0.0,
        )

    # Calculate t and make sure object is not behind screen
    t = dot_product(edge2, q_vector) * inverse_determinant

    if t < 0 :
        return CollisionResult (
            triangle = triangle,
            hit = False,
            distance= 0.0,
        )

    # We hit!
    return CollisionResult(
        triangle=triangle,
        hit=True,
        distance=t,
    )

def perform_raycast(ray: Ray, triangles: tuple[Triangle]) -> CollisionResult | None:
    min_hit: CollisionResult | None = None

    for triangle in triangles:
        result = collision_between_ray_and_triangle_moller(ray, triangle)
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
