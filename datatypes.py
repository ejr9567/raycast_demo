from dataclasses import dataclass
import math
from datetime import datetime


# R, G, B values (0. = not present, 1. = completely present)
Color = tuple[float, float, float]

def invert_color(color: Color) -> Color:
    return 1. - color[0], 1. - color[1], 1. - color[2]

def Color_cpp_declaration(color: Color) -> str:
    return f"Color({color[0]}f, {color[1]}f, {color[2]}f)"


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

def Vec3_cpp_declaration(v: Vec3) -> str:
    return f"Vec3({v[0]}f, {v[1]}f, {v[2]}f)"


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

    @property
    def cpp_declaration(self) -> str:
        v1, v2, v3 = self.vertices

        return (
            "Triangle("
                f"{Vec3_cpp_declaration(v1)}, "
                f"{Vec3_cpp_declaration(v2)}, "
                f"{Vec3_cpp_declaration(v3)}, "
                f"{Color_cpp_declaration(self.color)}"
            ")"
        )


@dataclass
class Scene:
    triangles: list[Triangle]
    light: Vec3

    background_color: Color

    @property
    def cpp_declaration(self) -> str:
        time_fmt = "%m/%d/%Y, %I:%M:%S %p"
        decl = f"// Scene data export from {datetime.now().strftime(time_fmt)}\n"
        decl += f"\n"

        decl += f"#include \"common.hpp\"\n"
        decl += "\n"
        decl += "\n"

        decl += f"extern const size_t num_triangles = {len(self.triangles)};\n"
        decl += f"extern Triangle scene_data_arr[num_triangles] = {{\n"
        for n, triangle in enumerate(self.triangles):
            decl += f"    {triangle.cpp_declaration}"
            if n != len(self.triangles) - 1:
                decl += ","
            decl += "\n"
        decl += f"}};\n"
        decl += f"extern Triangle* scene_data = scene_data_arr;\n"

        decl += f"extern Vec3 light_pos = {Vec3_cpp_declaration(self.light)};\n"

        decl += (
            f"extern Color background_color"
               f" = {Color_cpp_declaration(self.background_color)};\n"
        )

        return decl
