from scenes import scenes
import sys
import pathlib


def main():
    if len(sys.argv) == 1:
        print(
            f"Usage: {sys.argv[0]} Scene Name out_file.scene",
            file=sys.stderr
        )
        sys.exit(1)

    scene_name = " ".join(sys.argv[1:-1])
    scene_out_path = sys.argv[-1]

    for scene in scenes:
        if scene.name == scene_name:
            scene.write_to_file(pathlib.Path(scene_out_path))


if __name__ == '__main__':
    main()
