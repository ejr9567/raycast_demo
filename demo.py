from datatypes import *
from viewer import show_result
from renderer import render_onto_screen


def make_empty_screen(dim: int) -> Screen:
    screen: Screen = []

    for _ in range(dim):
        screen.append([(0., 0., 0.) for __ in range(dim)])

    return screen


def main():
    screen_dim = 20

    screen = make_empty_screen(screen_dim)

    scene = Scene(
        triangles = (
            Triangle(
                vertices = (
                    # △
                    (0.5, 1., 1.),
                    (0., 0., 1.),
                    (1., 0., 1.)
                ),
                color = (1., 0., 0.)  # red
            ),
        )
    )

    render_onto_screen(screen, screen_dim, scene)

    show_result(
        screen,
        scale = 30,  # 30 monitor pixels per scene pixel
        pad = 1  # 2 pixels' worth of padding on each side
    )

if __name__ == '__main__':
    main()
