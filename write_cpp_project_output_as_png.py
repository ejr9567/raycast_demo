from datatypes import *
from write_image_file import write_image_file

from pathlib import Path
from struct import unpack


def _read_uint64be(file) -> int:
    raw = file.read(8)
    assert len(raw) == 8
    return int.from_bytes(
        raw,
        byteorder = "big",
        signed = False
    )

def _read_floatbe(file) -> float:
    raw = file.read(4)
    assert len(raw) == 4

    return unpack(
        ">f",  # one item in buffer:
                      # big-endian float
        raw
    )[0]  # first unpacked item

def write_cpp_project_output_as_png(
    in_filename: str,
    out_filename: str
):
    with Path(in_filename).open("rb") as in_file:
        dim = _read_uint64be(in_file)

        screen: Screen = []
        for row in range(dim):
            row_data = []
            for col in range(dim):
                r = _read_floatbe(in_file)
                g = _read_floatbe(in_file)
                b = _read_floatbe(in_file)

                row_data.append((r, g, b))

            screen.append(row_data)


    write_image_file(screen, dim, out_filename)


def main():
    from sys import argv


    assert len(argv) == 3, f"usage: {argv[0]} <in filename> <out filename>"

    in_filename = argv[1]
    out_filename = argv[2]

    assert Path(in_filename).is_file(), f"{argv[0]}: input file does not exist"


    write_cpp_project_output_as_png(in_filename, out_filename)


if __name__ == '__main__':
    main()
