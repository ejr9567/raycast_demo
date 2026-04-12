from dataclasses import dataclass
import math


# R, G, B values (0. = not present, 1. = completely present)
Color = tuple[float, float, float]

def invert_color(color: Color) -> Color:
    return 1. - color[0], 1. - color[1], 1. - color[2]


# List of pixel rows
Screen = list[list[Color]]


Vec3 = tuple[float, float, float]

def Vec3_add(v1: Vec3, v2: Vec3):
    return v1[0] + v2[0], v1[1] + v2[1], v1[2] + v2[2]

def Vec3_sub(v1: Vec3, v2: Vec3):
    return Vec3_add(v1, Vec3_scale(v2, -1.))

def Vec3_scale(v: Vec3, scale: float):
    return v[0] * scale, v[1] * scale, v[2] * scale

def Vec3_cross(a: Vec3, b: Vec3) -> Vec3:
    # a X b = < a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0] >
    return (

        (a[1] * b[2]) - (a[2] * b[1]),
        (a[2] * b[0]) - (a[0] * b[2]),
        (a[0] * b[1]) - (a[1] * b[0])

    )

def Vec3_dot(a: Vec3, b: Vec3) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

def Vec3_mag(v: Vec3) -> float:
    return math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])

def Vec3_norm(v: Vec3) -> Vec3:
    return Vec3_scale(v, 1. / Vec3_mag(v))


# Position of vertex (x, y, z)
Vertex = Vec3

@dataclass
class Ray:
    origin: Vec3

    # displacement from origin
    # (relative coordinate to origin)
    direction: Vec3

@dataclass
class Triangle:
    vertices: tuple[Vertex, Vertex, Vertex]
    color: Color

    def normal(self) -> Vec3:
        """
        Find normal vector from triangle surface.
        """
        # Direction is cross product
        # between two edges
        v1, v2, v3 = self.vertices
        e1 = Vec3_sub(v2, v1)
        e2 = Vec3_sub(v3, v1)

        direction = Vec3_cross(e1, e2)

        normalized_direction = Vec3_norm(direction)

        return normalized_direction


@dataclass
class Scene:
    triangles: list[Triangle]
    light: Vec3

    background_color: Color
