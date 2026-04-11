from datatypes import Color, Screen


def show_result(
    # Lightness of each pixel
    screen: Screen,

    # Number of user interface pixels
    # used to represent each pixel
    # in the rendering
    scale: int,

    # Number of pixels' worth of space
    # as a boundary on each side of the image
    pad: int
):
    import tkinter

    toplevel = tkinter.Tk()

    pad_amt_one_side = pad * scale

    screen_dim = len(screen)
    canvas_dim = (
        (scale * len(screen))  # for each pixel
        + (pad_amt_one_side * 2)  # padding
    )

    font = ("Comic Sans MS", int(0.2 * scale))
    bg = "#202020"
    fg = "#D0D0D0"

    def screen_to_canvas_coord(x: int, y: int) -> (float, float):
        # give coordinates of top-left corner of
        # canvas rectangle corresponding to screen coordinate

        return (
            # screen coord is relative to bottom-left corner
            # canvas coord is relative to top-left corner

            # left offset: start on the left side,
            # then skip left padding,
            # then one pixels' worth for each
            # value in the coordinate
            pad_amt_one_side + (x * scale),

            # top offset: start at the bottom side,
            # then skip bottom padding,
            # then one pixels' worth for each
            # value in the coordinate,
            # then one more pixels' worth to move
            # from the bottom of that pixel to
            # the top of that pixel
            canvas_dim - pad_amt_one_side - (y * scale) - scale
        )

    def invert_color(color: Color) -> Color:
        return 1. - color[0], 1. - color[1], 1. - color[2]

    # Grayscale rendering
    # 128 -> 80
    def color_component_to_tkinter_color_two_hex_char(color: float) -> str:
        screen_color_int = int(color * 256)

        if screen_color_int == 256:
            screen_color_int = 255

        screen_color = screen_color_int.to_bytes(length=1).hex().zfill(2)

        return screen_color

    # (64, 128, 192) -> "#4080C0"
    def color_amt_to_tkinter_color(color: Color) -> str:
        r = color_component_to_tkinter_color_two_hex_char(color[0])
        g = color_component_to_tkinter_color_two_hex_char(color[1])
        b = color_component_to_tkinter_color_two_hex_char(color[2])

        screen_color = "#" + r + g + b

        return screen_color

    canvas = tkinter.Canvas(toplevel, width = canvas_dim, height = canvas_dim, bg = bg)
    canvas.pack(padx = 0, pady = 0)

    # draw screen pixels on the canvas
    for screen_y in range(screen_dim):
        for screen_x in range(screen_dim):
            screen_color_flt = screen[screen_y][screen_x]
            pixel_color = color_amt_to_tkinter_color(screen_color_flt)

            canvas_x, canvas_y = screen_to_canvas_coord(screen_x, screen_y)
            canvas.create_rectangle(
                canvas_x, canvas_y, canvas_x + scale, canvas_y + scale,
                fill = pixel_color, outline = fg
            )

    # draw overlay displaying coordinates of each pixel
    for screen_y in range(screen_dim):
        for screen_x in range(screen_dim):
            canvas_x, canvas_y = screen_to_canvas_coord(screen_x, screen_y)

            screen_color_flt = screen[screen_y][screen_x]
            overlay_color = color_amt_to_tkinter_color(invert_color(screen_color_flt))

            canvas.create_text(
                canvas_x + (scale / 2), canvas_y + (scale / 2),
                text = f"({screen_x},{screen_y})",
                fill = overlay_color,
                font = font
            )

    toplevel.mainloop()
