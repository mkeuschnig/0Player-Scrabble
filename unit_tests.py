# import checks as C
# import logic as L
# import settings as S

import pprint
from copy import deepcopy

from logic import Checks as C
from logic import Datatypes as D
from logic import Display
from logic import Game
from logic import Logic as L
from logic import Scratch
from logic import Settings as S
from logic import WordLog as WL
from logic import WordSearch as WS

gameSettings = S.get_game_settings()
S.set_game_settings(settings=gameSettings)


def basics():
    # checks.py
    assert C.is_position_valid("A1") is True
    assert C.is_position_valid("O15") is True
    assert C.is_position_valid("B52") is False
    assert C.is_position_valid("Z6") is False

    assert C.is_coordinate_valid(0, 0) is True
    assert C.is_coordinate_valid(99, 99) is False
    assert C.is_coordinate_valid(75, 0) is False
    assert C.is_coordinate_valid(-1, -1) is False

    assert C.is_position_empty("A1") is True
    assert C.is_position_empty("A2") is True
    assert C.is_position_empty("A3") is True
    assert C.is_position_empty("A4") is True
    assert C.is_position_empty("O15") is True

    whole_range = L.convert_positions_to_list("A1", "O1")
    broken_range = ["A1", "A3"]
    assert C.is_position_list_continuous(whole_range) is True
    assert C.is_position_list_continuous(broken_range) is False

    # logic_old.py
    assert list(L.find_substring("A", "ABRACADABRA")) == [0, 3, 5, 7, 10]
    assert list(L.find_substring("Z", "BANANA")) == []

    assert L.convert_coordinate_to_position(0, 0) == "A1"
    assert L.convert_coordinate_to_position(14, 14) == "O15"
    assert L.convert_coordinate_to_position(62, 52) is None
    assert L.convert_coordinate_to_position(2, 52) is None
    assert L.convert_coordinate_to_position(52, 2) is None

    assert L.convert_position_to_coordinate("A1") == (0, 0)
    assert L.convert_position_to_coordinate("O15") == (14, 14)
    assert L.convert_position_to_coordinate("Ö92") == (None, None)
    assert L.convert_position_to_coordinate("A92") == (None, None)
    assert L.convert_position_to_coordinate("Z6") == (None, None)

    assert L.modify_position_numeric("H8", -7, -7) == "A1"
    assert L.modify_position_numeric("A1", +7, +7) == "H8"
    assert L.modify_position_numeric("O15", -14, -14) == "A1"
    assert L.modify_position_numeric("H8", -10, -10) is None
    assert L.modify_position_numeric("B1", -4, -4) is None

    assert L.convert_positions_to_list("A1", "A5") == ["A1", "A2", "A3", "A4", "A5"]
    assert L.convert_positions_to_list("A1", "F1") == ["A1", "B1", "C1",
                                                       "D1", "E1", "F1"]
    assert L.convert_positions_to_list("A1", "A1") == ["A1"]
    assert L.convert_positions_to_list("A1") == ["A1"]
    assert L.convert_positions_to_list("A1", "B2") == []

    # Place "ERNST" on actual board
    L.set_letter_to_position("E", "A1")
    L.set_letter_to_position("R", "B1")
    L.set_letter_to_position("N", "C1")
    L.set_letter_to_position("S", "D1")
    L.set_letter_to_position("T", "E1")

    w = ""
    for currentPosition in L.convert_positions_to_list("A1", "E1"):
        w += "".join(L.get_letter_from_position(currentPosition,
                                                is_temporary=False))
    # print(w)
    assert w == "ERNST"

    # Place "TEMPORÄR" on temporary board
    # global recent temp. Positions are added automatically.
    L.set_letter_to_position("T", "A1", is_temporary=True)
    L.set_letter_to_position("E", "B1", is_temporary=True)
    L.set_letter_to_position("M", "C1", is_temporary=True)
    L.set_letter_to_position("P", "D1", is_temporary=True)
    L.set_letter_to_position("O", "E1", is_temporary=True)
    L.set_letter_to_position("R", "F1", is_temporary=True)
    L.set_letter_to_position("Ä", "G1", is_temporary=True)
    L.set_letter_to_position("R", "H1", is_temporary=True)

    w = ""
    for currentPosition in L.convert_positions_to_list("A1", "H1"):
        w += "".join(L.get_letter_from_position(currentPosition,
                                                is_temporary=True))
    # print(w)
    assert w == "TEMPORÄR"

    # get filled positions from both boards in various ways.
    # assert L.get_non_empty_positions("A1") == ["A1"]
    # assert L.get_non_empty_positions("A1", "A0") == []
    # assert L.get_non_empty_positions("A1", axis="X") is not None
    # assert L.get_non_empty_positions("A1", axis="Y") is not None
    # assert L.get_non_empty_positions("A1",
    #                                  axis="X",
    #                                  isTemporary=True) is not None
    # assert L.get_non_empty_positions("A1",
    #                                  axis="Y",
    #                                  isTemporary=True) is not None
    # assert L.get_non_empty_positions("A1",
    #                                  axis="X",
    #                                  isTemporary=True,
    #                                  returnLetters=True) is not None
    # assert L.get_non_empty_positions("A1",
    #                                  axis="Y",
    #                                  isTemporary=True,
    #                                  returnLetters=True) is not None
    # assert L.get_non_empty_positions(startPosition="A1",
    #                                  isTemporary=True,
    #                                  returnLetters=True,
    #                                  axis="X") == list("TEMPORÄR")
    # assert L.get_non_empty_positions("A1", "E1",
    #                                  returnLetters=True) == list("ERNST")
    # assert L.get_non_empty_positions("A1", "A10", returnLetters=True) == ["E"]
    # assert L.get_non_empty_positions("A1", "A10", returnLetters=True) == ["E"]
    # assert L.get_non_empty_positions("A1", "A10",
    #                                  returnLetters=True, axis="X") == list("ERNST")

    # see if "TEMPORÄR" is still in the global variable.
    w = ""
    for tempPosition in S.RECENT_TEMPORARY_POSITIONS:
        w += ''.join(L.get_letter_from_position(tempPosition, is_temporary=True))
    # print(w)

    # clear the recent temporary positions.
    assert len(S.RECENT_TEMPORARY_POSITIONS) > 0
    L.remove_temporary_positions()
    assert len(S.RECENT_TEMPORARY_POSITIONS) == 0

    # check if everything on the temporary Board is empty.
    # assert L.get_non_empty_positions("A1", isTemporary=True, axis="X") == []
    # assert L.get_non_empty_positions("A1", isTemporary=True, axis="Y") == []

    # get_word_from_position
    assert L.get_word_from_position("A1", "E1") == "ERNST"
    assert L.get_word_from_position("A0", "B12") == ""
    assert L.get_word_from_position("A1", "A15") == "E"

    # modifier-fields
    assert L.get_word_multiplier("A1", "A15") == 27
    assert L.get_word_multiplier("A1", "O1") == 27
    assert L.get_word_multiplier("A1", "A8") == 9
    assert L.get_word_multiplier("A1") == 3
    assert L.get_word_multiplier("A2") == 1
    assert L.get_word_multiplier("B2", "N2") == 4
    assert L.get_word_multiplier("B6") == 1

    assert L.get_letter_multiplier("B2") == 1
    assert L.get_letter_multiplier("F2") == 3
    assert L.get_letter_multiplier("B6") == 3
    assert L.get_letter_multiplier("B1") == 1

    # set entire words:
    L.set_word_to_position("ERNST", "A2", "E2")
    L.set_word_to_position("ER?ST", "A3", "E3",
                           joker_letters="N")
    L.set_word_to_position("ER??T", "A4", "E4",
                           joker_letters="NS")
    L.set_word_to_position("?????", "A5", "E5",
                           joker_letters="ERNST")
    # set word with wrong endPosition: should still only place from A8 to D8
    L.set_word_to_position("EINS", "A8", "O8", axis="X")

    # read entire words
    assert L.get_word_from_position("A2", "E2") == "ERNST"
    assert L.get_word_from_position("A8", "O8") == "EINS"

    # read jokers
    assert L.get_letter_from_position("A5", show_joker=False) == "E"
    assert L.get_letter_from_position("A5", show_joker=True) == "?"

    assert L.get_word_from_position("A3", "E3", show_joker=True) == "ER?ST"
    assert L.get_word_from_position("A4", "E4", show_joker=True) == "ER??T"
    assert L.get_word_from_position("A5", "E5", show_joker=True) == "?????"
    assert L.get_word_from_position("A5", "E5", show_joker=False) == "ERNST"

    # score letters
    assert L.score_letter("E", "O1") == 1
    assert L.score_letter("Q", "O1") == 10
    assert L.score_letter("Q", "M7") == 20
    assert L.score_letter("K", "N6") == 12

    # score Words
    # assert L.scoreWord("ERNST", "A1", "E1") == 15
    # assert L.scoreWord("ERNST", "A1", axis="X") == 15
    # assert L.scoreWord("WIEDERKEHRENDER", "O1", axis="Y") == 621

    # reset everything and make sure the reset worked.
    S.reset()
    assert L.get_word_from_position("A1", "E1") == ""

    # word searches
    # remove letters from the rack as they are placed

    S.set_rack("BEIN")

    ernst = D.Play("ERNST", "F8", "x")
    erde = D.Play("ERDE", "G7", "y")
    erbse = D.Play("ERBSE", "I5", "y")

    L.execute_play(ernst)
    S.increase_turn()
    L.execute_play(erde)
    S.increase_turn()
    L.execute_play(erbse)
    S.increase_turn()

    # allPlays = WS.find_all_plays()

    # usable_a = L.convert_positions_to_list("B8", "N8")
    # possibleWords_a = WS.createWords(usable_a, "x")
    # print(possibleWords_a)
    # startingPosition = WS.findStartingPosition("BERNSTEIN",
    #                                            usable_a,
    #                                            "x",
    #                                            ernst.used_positions)
    # print("starting position for BERNSTEIN:", startingPosition)
    # print("\n")
    #
    # usable_b = L.convert_positions_to_list("E5", "L5")
    # possibleWords_b = WS.createWords(usable_b, "x")
    # print(possibleWords_b)
    # startingPosition = WS.findStartingPosition("EBEN",
    #                                            usable_b,
    #                                            "x",
    #                                            erbse.used_positions)
    #  S.set_rack("HMLSA")
    #  L.set_letter_to_position("K5", "E")
    # # L.set_letter_to_position("M5", "A")
    #  usable_b = L.convert_positions_to_list("I5", "O5")
    #  possibleWords_b = WS.createWords(usable_b, "x")
    #  # TODO: add the tests for everything in WordSearch
    #  print(possibleWords_b)

    # print(allPlays)

    S.reset()
    print("RESET".center(20, "*"))
    return


def word_search():
    # TODO: Redesign findPossibleWords.
    S.set_rack("ERNSTLUD")
    center = L.get_center_of_board()
    # L.set_letter_to_position(center, "E")
    print("Center Position:", center)
    # emptyRange = ["G8", "H8", "I8"]
    # what if we just plant a random letter onto the center?
    # rack = S.get_rack()
    # L.set_letter_to_position(center, rack[0])
    # rack.pop(0)
    # having no letters on the boeard should yield:
    # STERN, ERST, ER, ERNST, REST, LERN, URNE, LUST, DURST, STRUDEL
    # maybe the problem is with intersection_update()
    usable_range = WS.find_usable_positions(center, "x")
    start_at = usable_range[0]
    end_at = usable_range[-1]
    print("usable range", usable_range)
    # first_turn_plays = WS.find_open_plays(list(center), "x")
    # words = WS.createWords(usableRange, "x")

    # WARNING: STUPID
    test_range = D.Area(position_list=usable_range)
    # stupid_words = WS.create_words_stupid_for_testing(test_range)
    # unique_words_stupid = list(set(stupid_words))
    # print(unique_words_stupid)
    # print("length of unique_words_stupid:", len(unique_words_stupid))

    # OBJECTIVE: redesign create_words and find_starting_position
    # test against creat  e_words_stupid
    # both funxtions must work without letters on the board
    new_words = WS.create_words(test_range)
    unique_new_words = list(set(new_words))
    print(unique_new_words)
    print("length of unique_words_new:", len(unique_new_words))

    placeable_suggestions = []
    possible_plays = []
    for word in unique_new_words:
        start_position = WS.find_starting_position(word, test_range)
        if len(start_position) == 0:
            continue
        else:
            for s_pos in start_position:
                raw_word = D.Suggestion(word,
                                        s_pos,
                                        test_range.axis)
                if C.is_word_placeable(raw_word):
                    placeable_suggestions.append(raw_word)

    for suggestion in placeable_suggestions:
        possible_plays.append(D.Play(suggestion.word,
                                     suggestion.position,
                                     suggestion.axis))
    pprint.pprint(possible_plays)
    print(f"total possible plays for turn {S.GAME_SETTINGS['turn']}: {len(possible_plays)}")
    # Display.print_board()
    # startingPositions = []
    # for current_word in unique_words:
    #     startingPositions.extend(WS.findStartingPosition(current_word,
    #                                                      stupid_range.pos_list,
    #                                                      stupid_range.axis,
    #                                                      []))
    # print(startingPositions)
    print("PASSED.")
    return


def rack_simple():
    S.reset()
    S.set_rack("ERNST")
    rack = S.get_rack()
    print("rack after reset:", rack)
    S.fill_rack()
    print("rack after fill_rack, without re-assignment:", rack)
    print("PASSED.")
    return


def rack_complete():
    S.reset()

    print("Drawing all letters from the bag...")
    letters_drawn = []
    bag = S.GAME_SETTINGS['bag']
    while len(bag) > 0:
        print("number of letters still in the bag:", len(bag))
        S.fill_rack()
        letters_drawn.extend(S.get_rack())
        print("letters drawn:", S.get_rack())
        S.set_rack("")
    print("total letters drawn:", len(letters_drawn))
    print("in order:", letters_drawn)
    print("PASSED.")


def play_creating():
    S.reset()
    S.set_rack("ERNSTL?")
    rack = S.get_rack()
    print("Rack:", rack)

    test_play_a = D.Play("LÜSTERN", "G8", "X")
    # print(WS.find_execution(test_play_a))
    print(test_play_a.find_execution())
    print(test_play_a)
    # passes with
    # [('L', 'G8'),
    # ('?', 'H8'),
    # ('S', 'I8'),
    # ('T', 'J8'),
    # ('E', 'K8'),
    # ('R', 'L8'),
    # ('N', 'M8')]
    L.execute_play(test_play_a)
    Display.print_board()
    S.increase_turn()

    S.set_rack("BEDARF")
    test_play_b = D.Play("BEDARF", "F3", "Y")
    print(test_play_b)
    # print(WS.find_execution(test_play_b))
    print(test_play_b.find_execution())
    L.execute_play(test_play_b)
    Display.print_board()

    print(L.get_word_from_position("F8", "N8", show_joker=True))
    print(L.get_word_from_position("F8", "N8", show_joker=False))
    # the complex play would be extending LÜSTERN to FLÜSTERN,
    # and create BEDARF in the process.

    # # Test-case with a letter already on the board
    # S.reset()
    # S.set_rack("T?")
    # rack = S.get_rack()
    # print("Rack:", rack)
    # L.set_letter_to_position("E", "H8")
    # test_play_a = D.Play("TEE", "G8", "x")
    # print(test_play_a)
    # # print(WS.find_execution(test_play_a))
    #
    # test_play_b = D.Play("TEE", "F8", "x")
    # print(test_play_b)

    # placeable_suggestions = []
    # possible_plays = []
    # center = L.get_center_of_board()
    # # the board is symmetrical, might as well start on the x-axis
    # # find the usable area (x-axis along the center)
    # usable_positions = WS.find_usable_positions(center, "x")
    # usable_area = D.Area(position_list=usable_positions)
    # # convert to search parameters
    # search_parameters = WS.create_search_parameters(usable_area)
    # # find words according to those parameters
    # possible_words = WS.create_words(search_parameters)
    #
    # # TODO: extract function
    # for current_word in possible_words:
    #     starting_positions = WS.find_starting_position(current_word,
    #                                                    search_parameters)
    #     if starting_positions == []:
    #         continue
    #     else:
    #         for s_pos in starting_positions:
    #             suggestion = D.Suggestion(current_word,
    #                                       s_pos,
    #                                       search_parameters.axis)
    #             if C.is_word_placeable(suggestion):
    #                 placeable_suggestions.append(suggestion)
    #
    # for current_suggestion in placeable_suggestions:
    #     possible_plays.append(D.Play(d_word=current_suggestion))
    #
    # sorted_plays = sorted(possible_plays,
    #                       key=operator.attrgetter('score'),
    #                       reverse=True)
    # highest_scoring_play = sorted_plays[0]
    # print("highest scoring play:")
    # print(highest_scoring_play)
    print("PASSED.")


def finding_usable_positions():
    S.reset()
    S.set_rack("BEDARF")
    test_play_b = D.Play("BEDARF", "M3", "Y")
    print(test_play_b)
    # print(WS.find_execution(test_play_b))
    print(test_play_b.find_execution())
    L.execute_play(test_play_b)
    S.increase_turn()

    Display.print_board()
    S.set_rack("BEDARF")
    test_area = D.Area(position_list=WS.find_usable_positions("M3", "x"))
    starting_positions = WS.find_starting_position("FADER", test_area)
    print("starting positions for FARBE on M3, X:")
    print(starting_positions)


def first_turn():
    S.reset()
    S.set_rack("ERNSTLU?")

    filled_positions = []
    usable_positions = WS.find_usable_positions("H8", "x")
    print("Usable positions:")
    first_area = D.Area(position_list=usable_positions)
    starting_positions = WS.find_starting_position("STRUDELN", first_area)
    print("starting positions for STRUDELN:")
    print(starting_positions)
    Display.print_board()

    print("Subturn in Turn 1:")
    first_subturn = Game.SubTurn(first_area)
    highest_play = first_subturn.highest_scoring_play
    L.execute_play(highest_play)
    Display.print_board()
    # all_plays = WS.find_plays_for_area(first_area)

    # pprint.pprint(all_plays)


def area_find_occupied_neighbors():
    S.reset()
    S.set_rack("STRUDELN")
    first_play = D.Play("STRUDELN", "F8", "x")
    L.execute_play(first_play)
    S.increase_turn()

    S.set_rack("FARBE")
    second_play = D.Play("FARBEN", "M3", "y")
    L.execute_play(second_play)
    S.increase_turn()

    S.set_rack("BEDARF")
    Display.print_board()
    subturn_area = D.Area("L2", "L14")
    subturn_to_solve = Game.SubTurn(subturn_area)
    pprint.pprint(subturn_to_solve.possible_plays)


def entire_turn(number_of_turns: int = 5):
    # TODO: DEBUG A WHOLE LOT
    # BUG: # considers FARBEN a proper play on M2, y
    # only FARBE gets planted.
    # if there's no letter on the rack, it's still trying to find a valid play.
    # TODO: Add checks to ensure at least one Rack-letter must be used.
    # BUG: "FABEL" on L4-L8 is considered the best play on Turn 3 in this setup.
    # The available Area is F8 to F14...
    # Also doesn't check for bonus-plays
    # which would need to be: FA, AR, BB, and EE

    # tested in debugger:
    # expected
    # [STRUDELN                    F8-M8:x         score:20(20+0)      ,
    #  FARBEN                      M3-M8:y         score:24(24+0)      ,
    #  BEDARF                      K7-K12:y        score:22(22+0)      ,
    #  RAFFE                       H12-L12:x       score:24(24+0)      ,
    #  BEDARF                      I5-N5:x         score:22(22+0)      ]

    S.reset()
    # S.fill_rack()
    turn_number = S.GAME_SETTINGS['turn']
    all_turns = []

    while turn_number < number_of_turns:
        # TODO: finally make Game_settings a proper Object
        turn_number = S.GAME_SETTINGS['turn']
        if C.is_first_turn() is True:
            S.set_rack("ERNSTLU?")
        else:
            S.set_rack("BEDARF")
        print(f"  Turn No.: {turn_number}  ".center(80, "-"))
        Display.print_board()

        turn = Game.Turn(None, S.get_rack())
        all_turns.append(turn)
        # input("Press Enter to execute the highest scoring play from this turn...")
        L.execute_play(turn.highest_scoring_play)
        print("  End of turn.  ".center(80, "-"))
        # S.fill_rack()
        S.increase_turn()

        Display.print_board()
        pprint.pprint(WL.get_active_plays())
        print("PASSED.")


def position_finding():
    S.reset()
    S.set_rack("ERNSTL?")
    test_play_open = D.Play("LÜSTERN", "G8", "X")
    L.execute_play(test_play_open)
    S.increase_turn()
    Display.print_board()

    S.set_rack("BEDARF")
    test_play_perpendicular = D.Play("BEDARF,", "F3", "y")
    # also counts as extended, score for BEDARF and FLÜSTERN would be added
    L.execute_play(test_play_perpendicular)
    S.increase_turn()
    Display.print_board()

    S.set_rack("D")
    test_play_extended = D.Play("FLÜSTERND", "F8", "x")
    L.execute_play(test_play_extended)

    S.set_rack("RETEN")
    test_play_retten = D.Play("RETTEN", "J5", "y")
    L.execute_play(test_play_retten)
    S.increase_turn()
    Display.print_board()

    S.set_rack("USTRN")
    test_play_merge = D.Play("AUSTERN", "F6", "x")
    # this only counts as AUSTERN, since it  doesn't extend any existing words
    L.execute_play(test_play_merge)
    S.increase_turn()
    Display.print_board()

    word_log = WL.read_log()
    # all_positions = word_log[0]['used_positions']

    # types of plays:
    # open - ruler finds no fixed positions, except for the origin
    # also, all neighbors are open positions
    # example: LÜSTERN, G8, x
    # extended - ruler goes along a placed word to find letters to extend
    # in the same direction
    # example: LÜSTERND, G8, x
    # perpendicular - ruler finds a single letter to extend and places a word
    # along the perpendicular axis.
    # example: BEDARF, F3, y
    # extends LÜSTERND to FLÜSTERND
    # merging - ruler finds gaps with busy positions, tries to find a fitting
    # word to fill the gap

    # Iterate over all filled positions
    # merge overlapping positions
    # make plays according to the areas

    # TODO: Extend Area to consider its neighbors
    print("PASSED.")


def word_finding_by_entire_word():
    # works.
    S.reset()

    print("Max size on X is:", S.GAME_SETTINGS['size_x'])
    test_word = "STERN"
    found_words = WS.word_list_by_word(test_word, 6)
    print(f"words with {test_word}, length of 6 found:", len(found_words))
    pprint.pprint(found_words)

    found_words = WS.word_list_by_word(test_word, 8)
    print(f"words with {test_word}, length of 8 found:", len(found_words))
    pprint.pprint(found_words)

    found_words = WS.word_list_by_word(test_word)
    print(f"words with {test_word}, length of MAX found:", len(found_words))
    pprint.pprint(found_words)


def area_finding():
    S.set_rack("ERNSTL?")
    test_play_open = D.Play("LÜSTERN", "G8", "X")
    L.execute_play(test_play_open)
    S.increase_turn()
    Display.print_board()

    # Goal: make this consider FLÜSTERN by Building BEDARF on F3, along Y.
    S.set_rack("BEDARF")
    rack = S.get_rack()
    area_list = Scratch.find_all_areas_per_play(test_play_open, "y", rack)
    possible_plays = []
    for current_area in area_list:
        neighbors = current_area.get_area_neighbors()
        sub_turn = Game.SubTurn(current_area.position_list)
        possible_plays.append(sub_turn.highest_scoring_play)

    print(possible_plays)
    print("PASSED.")


def play_finding_by_position():
    # This passes when the play BEDARF, F3, Y
    # gets points for the 2 plays it extends.
    # (DERBE, E5, X) and (FL?STERN, E8, X)

    # Start by setting LÜSTERN
    S.set_rack("ERNSTL?")
    test_play_open = D.Play("LÜSTERN", "G8", "X")
    L.execute_play(test_play_open)
    S.increase_turn()
    Display.print_board()

    # Set BORSTE
    S.set_rack("BORTE")
    test_play_borste = D.Play("BORSTE", "I5", "Y")
    L.execute_play(test_play_borste)
    S.increase_turn()
    Display.print_board()

    # Set ERBE
    S.set_rack("ERE")
    test_play_erbe = D.Play("ERBE", "G5", "X")
    L.execute_play(test_play_erbe)
    S.increase_turn()
    Display.print_board()

    # found_play = WL.find_active_play_by_position("G8")
    # print(found_play)
    # Find BEDARF,
    # Extends ERBE to DERBE
    # Extends LÜSTERN to FLÜSTERN
    # mark both extended-plays as "active" in the WordLog.
    # mark ERBE and LÜSTERN

    S.set_rack("BEDARF")
    test_area_bedarf = D.Area("F3", "F8")
    # empty_area_with_no_neighbors = D.Area("D3", "D8")

    # Works.
    bedarf_turn = Game.SubTurn(test_area_bedarf.position_list)
    L.execute_play(bedarf_turn.highest_scoring_play)
    S.increase_turn()
    S.set_rack("VERNDE")
    Display.print_board()
    # Works.
    area_verderbende = D.Area("A5", "O5")
    verderbende_turn = Game.SubTurn(area_verderbende.position_list)
    L.execute_play(verderbende_turn.highest_scoring_play)
    S.increase_turn()
    Display.print_board()

    S.set_rack("ZIERENDE")
    area_extends_right = D.Area("N1", "N15")
    extends_right_turn = Game.SubTurn(area_extends_right.position_list)

    print("highest scoring play:")
    pprint.pprint(extends_right_turn.highest_scoring_play)
    L.execute_play(extends_right_turn.highest_scoring_play)
    S.increase_turn()
    Display.print_board()

    # active_plays = WL.get_active_plays()
    # pprint.pprint(active_plays)
    # print("Length of active plays:", len(active_plays))
    #
    # print("All plays of extends_right_turn")
    # pprint.pprint(extends_right_turn.possible_plays)

    # for position in test_area_bedarf.neighbors:
    #     L.set_letter_to_position(".", position)
    # Display.print_board()
    # print("-"*30)
    # print("LÜSTERN can be expanded at:", test_play_open.extendable_at)
    # test_area_flsternd = D.Area("F8", "N8")
    # print("contested at:", test_area_flsternd.contested_at)
    # print("contested play(s):")
    # print(test_area_flsternd.contested_plays)
    # TODO: the exact same play can be contested twice.
    #  -> identical play on 2 different positions

    S.set_rack("ERNSTZUNEHMEND")
    area_non_continuous = D.Area("L1", "L15")
    turn_non_continuous = Game.SubTurn(area_non_continuous.position_list)
    print("Current Rack:", S.get_rack())
    print("Plays possible on L1 to L15:")
    pprint.pprint(turn_non_continuous.possible_plays)

    # TODO, testing:
    # select an area directly adjacent to an existing word, make sure all sub-plays are
    # counted as well

    # UR on E13-F13 should be possible
    # Bonus: DU, E12-E13 // ER, F12-F13
    S.set_rack("ERDE")
    play_erde = D.Play("ERDE", "C12", "X")
    L.execute_play(play_erde)
    S.increase_turn()

    S.set_rack("URNE")
    Display.print_board()
    parallel_area = D.Area("C13", "H13")
    affected_parallel_plays = parallel_area.contested_plays
    print("affected_parallel plays:")
    pprint.pprint(affected_parallel_plays)

    parallel_subturn = Game.SubTurn(parallel_area.position_list)
    print("highest scoring play:")
    pprint.pprint(parallel_subturn.highest_scoring_play)
    print("Plays possible on C13 to F13:")
    pprint.pprint(parallel_subturn.possible_plays)

    # TODO, for Testing.:
    # create a situation on the board where the entire rack is played,
    # the word is vertical and extends all already existing words (7 extensions)

    # TODO: Idea - in an area with 2 or more possible extension_crossovers,
    # try to find the extensions first, then fill the area via regex-words.
    # needs: a function to reserve letters from the rack,
    # the word_search by regex,
    print("PASSED.")


def play_finding_parallel():
    input("Starting: play_finding_parallel")
    S.reset()
    S.set_rack("ERDE")
    play_erde = D.Play("ERDE", "G8", "X")
    L.execute_play(play_erde)
    S.increase_turn()

    S.set_rack("URNE")
    Display.print_board()
    parallel_area = D.Area("I9", "L9")
    affected_parallel_plays = parallel_area.contested_plays
    print("affected_parallel plays:")
    pprint.pprint(affected_parallel_plays)

    parallel_subturn = Game.SubTurn(parallel_area)
    print("highest scoring play:")
    pprint.pprint(parallel_subturn.highest_scoring_play)
    print("Plays possible on I9 to L9:")
    pprint.pprint(parallel_subturn.possible_plays)
    print("PASSED.")


def play_finding_multiple():
    # TODO: make this pass
    # input("Starting: play_finding_multiple")
    S.reset()
    S.set_rack("ERDE")
    play_erde = D.Play("ERDE", "G8", "X")
    L.execute_play(play_erde)
    S.increase_turn()

    S.set_rack("DEN")
    area_den = D.Area("K6", "K8")
    subturn_den = Game.SubTurn(area_den)
    # highest scoring play should be DEN, K6, Y with ERDEN as bonus.
    print("highest scoring play for Area of K6 to K8:")
    print(subturn_den.highest_scoring_play)
    # play_den = D.Play("DEN", "K6", "Y")
    L.execute_play(subturn_den.highest_scoring_play)
    # L.execute_play(play_den)
    S.increase_turn()

    S.set_rack("URNE")
    Display.print_board()
    parallel_area = D.Area("I9", "L9")
    affected_parallel_plays = parallel_area.contested_plays
    print("affected_parallel plays:")
    pprint.pprint(affected_parallel_plays)

    parallel_subturn = Game.SubTurn(parallel_area)
    print("highest scoring play:")
    # expected: Still URNE on I9, X
    # bonus, DU, ER, DENN
    pprint.pprint(parallel_subturn.highest_scoring_play)
    print("Plays possible on I9 to L9:")
    pprint.pprint(parallel_subturn.possible_plays)
    # TODO: the master-test: a word that now has parallel AND extending plays.

    # URNE                        I9-L9:x         score:22(5+17)
    # >> +DENN                   K6-K9:Y         score:4
    # >> +DU                     I7-I8:y         score:3
    # >> +ER                     J7-J8:y         score:2
    # print("PASSED.")


def read_from_position():
    S.reset()
    S.set_rack("ERDE")
    play_erde = D.Play("ERDE", "G8", "X")
    L.execute_play(play_erde)

    reader_word = L.suggestion_from_position("G8", "X")
    print("reader_word", reader_word)
    print("word equals the word in the previous play:", reader_word == play_erde.word)
    print("PASSED.")


def log_searching():
    S.reset()
    # finding the plays.
    S.set_rack("ERNSTLÜ")
    play_lustern = D.Play("LÜSTERN", "G8", "X")
    L.execute_play(play_lustern)
    S.increase_turn()
    # Display.print_board()

    # Set BORSTE
    S.set_rack("BORTE")
    play_borste = D.Play("BORSTE", "I5", "Y")
    L.execute_play(play_borste)
    S.increase_turn()
    # Display.print_board()

    # Set ERBE
    S.set_rack("ERE")
    play_erbe = D.Play("ERBE", "G5", "X")
    L.execute_play(play_erbe)
    S.increase_turn()
    # Display.print_board()

    # found_play = WL.find_active_play_by_position("G8")
    # print(found_play)
    # Find BEDARF,
    # Extends ERBE to DERBE
    # Extends LÜSTERN to FLÜSTERN
    # mark both extended-plays as "active" in the WordLog.
    # mark ERBE and LÜSTERN
    S.set_rack("BEDARF")
    test_area_bedarf = D.Area("F3", "F8")
    bedarf_turn = Game.SubTurn(test_area_bedarf.position_list)
    L.execute_play(bedarf_turn.highest_scoring_play)
    S.increase_turn()
    Display.print_board()

    print("All Plays:")
    all_plays = WL.read_log()
    pprint.pprint(all_plays)
    print("Length of all plays:", len(all_plays))

    print("updating to only active plays")
    WL.deactivate_extended_plays()

    print("Only the active plays:")
    active_plays = WL.get_active_plays()
    pprint.pprint(active_plays)
    print("Length of active plays:", len(active_plays))
    # test passes if the active plays are:
    # FLÜSTERN, DERBE, BORSTE and BEDARF
    print("PASSED.")


def entire_game(is_automatic: bool = False,
                always_ERNSTLUA: bool = False):
    # emulate the turns, from start to empty bag.
    # ask before executing a play whether it's correct,
    # write "incorrect" plays to a list for debugging.
    S.reset()
    remaining_letters_initial = len(S.INITIAL_SETTINGS['bag'])
    # remaining_letters_initial = len("AAAA")
    remaining_letters = deepcopy(remaining_letters_initial)
    turn_number = S.GAME_SETTINGS['turn']
    all_turns = []
    incorrect_plays = []
    game_score = 0
    previous_best_play = None
    current_rack = []
    running = True

    print("Number of Letters:", remaining_letters)

    while running:

        if always_ERNSTLUA is True:
            # 4 letters still in the bag: only "ERNS" should be on the rack.
            num_letters_replaced = len("ERNSTLUA") - len(S.get_rack())
            print("number of letters replaced:", num_letters_replaced)

            if remaining_letters == 0:
                pass
            elif remaining_letters < num_letters_replaced:
                offset = len("ERNSTLUA") - remaining_letters
                ernstlua_letters = "ERNSTLUA"[0:-offset]
                S.set_rack(ernstlua_letters)
            else:
                S.set_rack("ERNSTLUA")
            current_rack = S.get_rack()
            remaining_letters -= num_letters_replaced

        else:
            S.fill_rack()
            current_rack = S.get_rack()
            remaining_letters = len(S.GAME_SETTINGS['bag'])

        # highest_scoring_play = None
        print(f"  Turn No.: {turn_number}  ".center(80, "-"))
        Display.print_board()

        # BUG: sometimes yields the same turn?
        # see scatch.md

        turn = Game.Turn(None, current_rack)
        # highest_scoring_play = turn.highest_scoring_play

        # print("Total possible Plays for this turn:")
        # pprint.pprint(turn.possible_plays)

        Display.print_board()

        print("The Highest scoring play is:".center(80))
        pprint.pprint(turn.highest_scoring_play)

        # TODO: this never fires.
        # if previous_best_play is not None:
        #     if highest_scoring_play == previous_best_play:
        #         raise NotImplementedError("Previous Best Play is identical to the current best Play.")

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
        print("Remaining letters:", remaining_letters)
        L.execute_play(turn.highest_scoring_play)
        # previous_best_play = highest_scoring_play
        game_score += turn.highest_scoring_play.score_total

        if remaining_letters < 0 and len(S.get_rack()) == 0:
            running = False
            break

        S.increase_turn()

    print("Game has ended.")
    print("Total score:", game_score)
    print("Incorrect plays:")
    pprint.pprint(incorrect_plays)

    print("Play Log:")
    pprint.pprint(WL.get_active_plays())


def custom_turn():
    # Goal: all plays in the Area of L1 to L15 need bonus plays to be valid.
    # BUG: doesn't consider single letters along the way - investigate!
    # see also: Line 3378 in logic_new
    #
    S.reset()
    S.set_rack("ERNSTLUA")
    word_1 = D.Play("NEUTRAL", "F8", "x")
    L.execute_play(word_1)
    S.increase_turn()

    S.set_rack("ERNSTLUA")
    word_2 = D.Play("ANLAUTES", "K5", "y")
    L.execute_play(word_2)
    S.increase_turn()

    # S.set_rack("ERNSTLUA")
    S.set_rack("FASS")  # Fass should be valid on L2
    searching_area = D.Area("L1", "L15")
    possible_plays = Scratch.find_plays_for_area(searching_area)
    # pprint.pprint(possible_plays)

    max_length = len(searching_area.non_empty_letters) + len(S.get_rack()) + 1
    for current_length in range(max_length, 2, -1):
        highest_length = [item for item in possible_plays if len(item) == current_length]
        print("Plays with a length of", current_length)
        pprint.pprint(highest_length)
    Display.print_board()
    #expected: "Plays with a length of 4: FASS,L2,y and FASS,L3,y


def deterministic_outcome():
    # emulate 2 games where the rack always stays the same.
    # remaining log should be identical.
    # TODO: figure out a way to decide between same-scoring plays
    pass


def find_empty_area_on_higher_turns():
    # find_usable_areas should still find a area the length
    # of position+(length_of_rack*2) on the given axis
    pass


def find_position_ranges():
    S.reset()
    S.set_rack("TEST")  # length of 4

    print("Rack:", S.get_rack())
    # starting at the top-barrier of the board H1
    # initial field is empty
    # expected: H4
    print("H1, y")
    test = WS.find_position_range_for_position("H1", "y")
    print(test)
    assert (test == L.convert_positions_to_list("H1", "H4"))

    # starting at the bottom-barrier of the board H15,
    # initial field is empty
    print("H15, y")
    test = WS.find_position_range_for_position("H15", "y")
    print(test)
    assert (test == L.convert_positions_to_list("H12", "H15"))
    # expected: H12

    # starting at the center of the board H8
    # initial field is empty
    # expected: list from H5 to H11 (length of 7, center with 3 to either side)
    print("H8, y")
    test = WS.find_position_range_for_position("H8", "y")
    print(test)
    assert (test == L.convert_positions_to_list("H5", "H11"))

    # H8 stays free, H7 and H9 have a letter on them.
    # expected: list from H4 to H12 (+1 to either direction from before)
    print("letters on H7 and H9, starting on H8, y")
    L.set_letter_to_position("X", "H7")
    L.set_letter_to_position("X", "H9")
    test = WS.find_position_range_for_position("H8", "y")
    print(test)
    assert (test == L.convert_positions_to_list("H4", "H12"))

    # H8 stays free, 4 positions are empty: H1, H2, H8, H15
    # expected: all positions on H, so H1 to H15
    L.set_word_to_position("XXXX", "H3", axis="y")
    L.set_word_to_position("XXXXX", "H10", axis="y")
    test = WS.find_position_range_for_position("H8", "y")
    print(test)
    assert (test == L.convert_positions_to_list("H1", "H15"))


def test_all():
    word_search()
    rack_simple()
    rack_complete()
    play_creating()
    finding_usable_positions()
    position_finding()
    word_finding_by_entire_word()
    area_finding()
    play_finding_by_position()
    log_searching()
    play_finding_parallel()
    read_from_position()
    play_finding_multiple()
    find_position_ranges()
    first_turn()
    entire_turn()
    print("PASSED.")


# Actual execution:
# finding_usable_positions()
# test_all
entire_turn(5)
# area_find_occupied_neighbors()
# entire_game(always_ERNSTLUA=True, is_automatic=True)
# custom_turn()
# find_position_ranges()
# play_finding_parallel()
# play_finding_multiple()
