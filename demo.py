# Lightness values (0. = black, 1. = white)
Screen = list[list[float]]

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

    font = ("Consolas", int(0.2 * scale))
    bg = "#202020"
    fg = "#D0D0D0"

    def screen_to_canvas_coord(x: int, y: int) -> (float, float):
        # give coordinates of top-left corner of
        # canvas rectangle corresponding to screen coordinate

        return (
            # screen coord is relative to bottom-left corner
            # canvas coord is relative to top-left corner

            # left offset: start at the left side,
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

    # Grayscale rendering
    def color_amt_to_tkinter_color(color: float) -> str:
        screen_color_int = int(color * 256)

        if screen_color_int == 256:
            screen_color_int = 255

        # R, G, B components are all based on color
        screen_color = "#" + screen_color_int.to_bytes(length=1).hex().zfill(2) * 3

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
            overlay_color = color_amt_to_tkinter_color(1.0 - screen_color_flt)

            canvas.create_text(
                canvas_x + (scale / 2), canvas_y + (scale / 2),
                text = f"({screen_x}, {screen_y})",
                fill = overlay_color,
                font = font
            )

    toplevel.mainloop()


class Demo:
    def __init__(
        self,

        screen_dim: int
    ):
        self.screen_width = screen_dim
        self.screen_height = screen_dim

        self.screen: list[list[float]] = []
        for _ in range(self.screen_height):
            self.screen.append([0. for __ in range(self.screen_width)])

    def run(self, scale: int, pad: int):
        self.render()
        self.show(scale, pad)

    def render(self):
        # TODO: rendering algorithm
        for y in range(self.screen_height):
            for x in range(self.screen_width):
                self.screen[y][x] = ((x / self.screen_height) + (y / self.screen_width)) / 2

    def show(self, scale: int, pad: int):
        show_result(self.screen, scale, pad)


def main():
    screen_dim = 10
    demo = Demo(screen_dim)

    demo.run(50, 2)

if __name__ == '__main__':
    main()
