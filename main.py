from parsing import Config
from rendering import Renderer
from game import Game


def main() -> None:
    config_parser = Config()
    config = config_parser.check_config()
    renderer = Renderer()
    game = Game(config, renderer)

    game.run()


if __name__ == "__main__":
    main()
