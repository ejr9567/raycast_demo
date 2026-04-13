from struct import pack, unpack


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

def _write_uint64be(val: int, file):
    raw = val.to_bytes(byteorder = "big", signed = False, length = 8)
    assert len(raw) == 8

    amt_written = file.write(raw)
    assert amt_written == 8

def _write_floatbe(val: float, file):
    raw = pack(">f", val)
    assert len(raw) == 4

    amt_written = file.write(raw)
    assert amt_written == 4
