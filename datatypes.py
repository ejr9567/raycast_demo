from dataclasses import dataclass


# R, G, B values (0. = not present, 1. = completely present)
Color = tuple[float, float, float]

# List of pixel rows
Screen = list[list[Color]]


Vec3 = tuple[float, float, float]

# Position of vertex (x, y, z)
Vertex = Vec3

@dataclass
class Triangle:
    vertices: tuple[Vertex, Vertex, Vertex]
    color: Color

@dataclass
class Scene:
    triangles: tuple[Triangle]
