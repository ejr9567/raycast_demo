from datatypes import *
from PIL import Image


def _color_to_rgb8(color: Color) -> tuple[int, int, int]:
    return (
        int(max(0., min(color[0] * 255, 255.))),
        int(max(0., min(color[1] * 255, 255.))),
        int(max(0., min(color[2] * 255, 255.)))
    )

def write_image_file(
    screen: Screen,
    dim: int,
    out_filename: str
):
    img = Image.new(
        mode = "RGB",
        size = (dim, dim),
        color = (0, 0, 0)
    )

    for y in range(dim):
        for x in range(dim):
            try:
                img.putpixel((x, dim - 1 - y), _color_to_rgb8(screen[y][x]))
            except:
                print(x, y, screen[y][x])
                raise

    img.save(out_filename)
