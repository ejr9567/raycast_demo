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
    distance_result = (x_diff * x_diff + y_diff * y_diff + z_diff * z_diff) ** 0.5

    return distance_result


@dataclass
class CollisionResult:
    triangle: Triangle
    hit: bool
    distance: float
    collision_point: Vec3


def collision_between_ray_and_triangle_moller(ray: Ray, triangle: Triangle) -> CollisionResult:

    # World position coordinates of collision
    collision_coordinates = (0.0, 0.0, 0.0)

    # Unpack triangle vertices
    v0, v1, v2 = triangle.vertices

    # SUB(edge1, vert1, vert0)
    edge1 = Vec3_sub(v1, v0)

    # SUB(edge2, vert2, vert0)
    edge2 = Vec3_sub(v2, v0)

    # CROSS(pvec, dir, edge2)
    p_vector = Vec3_cross(ray.direction, edge2)

    # det = DOT(edge1, pvec)
    determinant = Vec3_dot(edge1, p_vector)

    if determinant == 0: # we are parallel
        return CollisionResult (
            triangle = triangle,
            hit = False,
            distance= 0.0,
            collision_point=collision_coordinates
        )

    # inv_det = 1.0 / det
    inverse_determinant = 1 / determinant

    # calculate distance from v0 to ray origin
    t_vector = Vec3_sub(ray.origin, v0)

    # Calculate U and make sure it is within triangle bounds
    u = Vec3_dot(t_vector, p_vector) * inverse_determinant

    if (u < 0.0) or (u > 1.0):
        return CollisionResult (
            triangle = triangle,
            hit = False,
            distance= 0.0,
            collision_point=collision_coordinates
        )

    # Calculate Q vector
    q_vector = Vec3_cross(t_vector, edge1)

    # Calculate V and make sure it is within triangle bounds
    v = Vec3_dot(ray.direction, q_vector) * inverse_determinant

    if (v < 0.0) or ((u + v) > 1.0):
        return CollisionResult (
            triangle = triangle,
            hit = False,
            distance= 0.0,
            collision_point=collision_coordinates
        )

    # Calculate t and make sure object is not behind screen
    t = Vec3_dot(edge2, q_vector) * inverse_determinant

    if t < 0 :
        return CollisionResult (
            triangle = triangle,
            hit = False,
            distance= 0.0,
            collision_point=collision_coordinates
        )

    # We hit! Build real collision point using r(t) = O + tD

    collision_coordinates = Vec3_add(Vec3_scale(ray.origin, t), ray.direction)

    return CollisionResult(
        triangle=triangle,
        hit=True,
        distance=t,
        collision_point=collision_coordinates
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

            # print(f"({x}, {y}) = {world_coords}")

            ray = Ray(
                origin = world_coords,
                direction = (0., 0., 1.)  # into the world
            )

            raycast_result = perform_raycast(ray, scene.triangles)
            if raycast_result is None:
                color = background_color
            else:
                triangle = raycast_result.triangle
                hit_point = raycast_result.collision_point

                # Ambient
                color = raycast_result.triangle.color

                # Diffuse
                # take dot product between
                normal_ray = triangle.normal_at_point(hit_point)
                print(f"({x}, {y}) = {normal_ray}")

            screen[y][x] = color
