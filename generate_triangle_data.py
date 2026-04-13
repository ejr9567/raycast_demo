from datatypes import *
from math import cos, sin

ROTATE_AXIS_X = 0
ROTATE_AXIS_Y = 1
ROTATE_AXIS_Z = 2

def rotate_about_origin(triangles: list[Triangle], angle: float, axis: int) -> list[Triangle]:
    cos_theta = cos(angle)
    sin_theta = sin(angle)

    rotated_triangles = []

    for triangle in triangles:
        v0, v1, v2 = triangle.vertices

        new_triangle = Triangle (
            vertices= (
                rotate_vertex(v0, cos_theta, sin_theta, axis),
                rotate_vertex(v1, cos_theta, sin_theta, axis),
                rotate_vertex(v2, cos_theta, sin_theta, axis)
            ),
            color = triangle.color
        )

        rotated_triangles.append(new_triangle)

    return rotated_triangles


def rotate_vertex(vertex: Vec3, cosine: float, sine: float, axis: int) -> Vec3:

    x, y, z = vertex

    if axis == ROTATE_AXIS_X:
        new_x = x
        new_y = y * cosine - z * sine
        new_z = y * sine + z * cosine
    elif axis == ROTATE_AXIS_Y:
        new_x = x * cosine + z * sine
        new_y = y
        new_z = -x * sine + z * cosine
    else:  # axis == ROTATE_AXIS_Z
        new_x = x * cosine - y * sine
        new_y = x * sine + y * cosine
        new_z = z


    result = (new_x, new_y, new_z)

    return result

def scale_vertex(vertex: Vec3, scale: Vec3) -> Vec3:
    v = vertex
    return (
        v[0] * scale[0],
        v[1] * scale[1],
        v[2] * scale[2]
    )


def scale_triangles(triangles: list[Triangle], scale: Vec3) -> list[Triangle]:
    new_triangles: list[Triangle] = []
    for triangle in triangles:
        v0, v1, v2 = triangle.vertices
        new_triangle = Triangle (
            vertices= (
                scale_vertex(v0, scale),
                scale_vertex(v1, scale),
                scale_vertex(v2, scale),
            ),
            color = triangle.color
        )
        new_triangles.append(new_triangle)
    return new_triangles


def translate_triangles(triangles: list[Triangle], origin: Vec3) -> list[Triangle]:
    new_triangles: list[Triangle] = []
    for triangle in triangles:
        v = triangle.vertices
        new_triangle = Triangle(
            vertices = (
                Vec3_add(v[0], origin),
                Vec3_add(v[1], origin),
                Vec3_add(v[2], origin)
            ),
            color = triangle.color
        )
        new_triangles.append(new_triangle)

    return new_triangles


@dataclass
class NewStructureProperties:
    rotations_rads: Vec3
    scale: Vec3
    origin: Vec3

    def apply(self, triangles: list[Triangle]) -> list[Triangle]:
        for ax in range(3):
            triangles = rotate_about_origin(
                triangles = triangles,
                angle = self.rotations_rads[ax],
                axis = ax
            )

        triangles = scale_triangles(triangles, self.scale)

        triangles = translate_triangles(triangles, self.origin)

        return triangles


def _triangles(*colors_and_coords: Color | Vec3) -> list[Triangle]:
    assert len(colors_and_coords) % 10 == 0

    triangles = []

    for tri_idx in range(len(colors_and_coords) // 10):
        colors_and_coords_part = colors_and_coords[tri_idx * 10:(tri_idx + 1) * 10]
        color = colors_and_coords_part[0]
        coords_part = colors_and_coords_part[1:]
        new_tri = Triangle(
            vertices = (
                (coords_part[0], coords_part[1], coords_part[2]),
                (coords_part[3], coords_part[4], coords_part[5]),
                (coords_part[6], coords_part[7], coords_part[8]),
            ),
            color = color
        )
        triangles.append(new_tri)

    return triangles

def make_triangular_prism(color_1: Color, color_2: Color, props: NewStructureProperties):
    triangles = _triangles(
        # Top, front face
        color_1,
        -1., 0., -1.,
        0., 1.5, 0.,
        1., 0., -1.,

        # Top, left side face
        color_2,
        -1., 0., 1.,
        0., 1.5, 0.,
        -1., 0., -1.,

        # Top, back face
        color_1,
        1., 0., 1.,
        0., 1.5, 0.,
        -1., 0., 1.,

        color_2,
        # Top, right side face
        1., 0., -1.,
        0., 1.5, 0.,
        1., 0., 1.,

        color_2,
        # Bottom, front face
        1., 0., -1.,
        0., -1.5, 0.,
        -1., 0., -1.,

        color_1,
        # Bottom, left side face
        -1., 0., -1.,
        0., -1.5, 0.,
        -1., 0., 1.,

        color_2,
        # Bottom, back face
        -1., 0., 1.,
        0., -1.5, 0.,
        1., 0., 1.,

        color_1,
        # Bottom, right side face
        1., 0., 1.,
        0., -1.5, 0.,
        1., 0., -1.,
    )

    return props.apply(triangles)


# def make_cube


def stringify_triangle_data(triangles: list[Triangle]) -> str:
    s = ""
    for t in triangles:
        v = t.vertices
        s += (
            f"Triangle(\n"
            f"    vertices = (\n"
            f"        ({v[0][0]}, {v[0][1]}, {v[0][2]}),\n"
            f"        ({v[1][0]}, {v[1][1]}, {v[1][2]}),\n"
            f"        ({v[2][0]}, {v[2][1]}, {v[2][2]})\n"
            f"    ),\n"
            f"    color = ({t.color[0]}, {t.color[1]}, {t.color[2]})\n"
            f"),\n"
        )
    return s


def load_obj_file(file_path: str, color: Color) -> list[Triangle]:
    vertices: list[Vec3] = []
    triangles: list[Triangle] = []

    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            parts = line.split()

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

                if len(parts) != 4:
                    # ignore ill-formed (untriangulated?) face
                    continue

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
