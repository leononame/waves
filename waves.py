import Game


def main():
    game = Game.Game()
    game.run()
    while(game.wants_repeat()):
        game.run()


if __name__ == '__main__':
    # Call main
    main()