# contains the main game-loop with applied settings
# TODO: split logic into different files
# TODO: make game_settings an actual object instead of a dict
# BUG: turns repeat

# import general modules
# from random import randint
# import re
# import shelve
from copy import deepcopy
import pprint
import logic

game_settings = logic.Settings.get_game_settings("german", "normal")
logic.Settings.set_game_settings(settings=game_settings)


def entire_game(is_automatic: bool = False,
                use_fixed_letters: bool = False,
                fixed_word="ERNSTLUA"):
    remaining_letters_initial = len(logic.Settings.INITIAL_SETTINGS['bag'])

    num_remaining_letters = deepcopy(remaining_letters_initial)
    turn_number = logic.Settings.GAME_SETTINGS['turn']
    all_turns = []
    incorrect_plays = []
    game_score = 0
    previous_best_play = None
    current_rack = []
    running = True

    print("Number of Letters:", num_remaining_letters)

    while running:

        if use_fixed_letters is True:
            num_letters_replaced = len(fixed_word) - len(logic.Settings.get_rack())
            print("number of letters replaced:", num_letters_replaced)

            if num_remaining_letters == 0:
                pass
            elif num_remaining_letters < num_letters_replaced:
                offset = len(fixed_word) - num_remaining_letters
                remaining_fixed_letters = fixed_word[0:-offset]
                logic.Settings.set_rack(remaining_fixed_letters)
            else:
                logic.Settings.set_rack(fixed_word)
            current_rack = logic.Settings.get_rack()
            num_remaining_letters -= num_letters_replaced

        else:
            logic.Settings.fill_rack()
            current_rack = logic.Settings.get_rack()
            num_remaining_letters = len(logic.Settings.GAME_SETTINGS['bag'])

        # highest_scoring_play = None
        print(f"  Turn No.: {turn_number}  ".center(80, "-"))
        logic.Display.print_board()

        turn = logic.Game.Turn(None, current_rack)
        highest_scoring_play = turn.highest_scoring_play

        # print("Total possible Plays for this turn:")
        # pprint.pprint(turn.possible_plays)

        logic.Display.print_board()

        print("The Highest scoring play is:".center(80))
        pprint.pprint(turn.highest_scoring_play)

        # TODO: this never fires, yet some turns repeat.
        if previous_best_play is not None:
            if highest_scoring_play == previous_best_play:
                raise NotImplementedError("Previous Best Play is identical to the current best Play.")

        if is_automatic is True:
            answer = "y"
        else:
            answer = ""

        while answer.casefold() not in ["y", "n"]:
            if answer == "":
                answer = input("Check against the board - is this play correct? [y/n]: >")
            if len(answer) == 0:
                continue
            elif answer.casefold() == "n":
                incorrect_plays.append(turn.highest_scoring_play)
                break
            elif answer.casefold() == "y":
                break

        print("  End of turn.  ".center(80, "-"))
        print("Remaining letters:", num_remaining_letters)
        logic.Logic.execute_play(turn.highest_scoring_play)
        # previous_best_play = highest_scoring_play
        game_score += turn.highest_scoring_play.score_total

        if num_remaining_letters < 0 and len(logic.Settings.get_rack()) == 0:
            # running = False
            break

        logic.Settings.increase_turn()

    print("Game has ended.")
    print("Total score:", game_score)
    print("Incorrect plays:")
    pprint.pprint(incorrect_plays)

    print("Play Log:")
    pprint.pprint(logic.WordLog.get_active_plays())


entire_game(is_automatic=True)
