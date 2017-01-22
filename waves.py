import Game


def main():
    game = Game.Game()
    repeat = True
    while repeat:
        game.run()
        repeat = game.wants_repeat()


if __name__ == '__main__':
    # Call main
    main()
