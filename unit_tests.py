# import checks as C
# import logic as L
# import settings as S
from random import randint

import pprint
import operator

from logic_new import Display
from logic_new import Datatypes as D
from logic_new import Settings as S
from logic_new import Logic as L
from logic_new import Checks as C
from logic_new import Game
from logic_new import WordSearch as WS
from logic_new import WordLog as WL
from logic_new import Scratch


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

    # logic.py
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
    return


def rack_simple():
    S.reset()
    S.set_rack("ERNST")
    rack = S.get_rack()
    print("rack after reset:", rack)
    S.fill_rack()
    print("rack after fill_rack, without re-assignment:", rack)
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


def entire_turn():
    S.reset()
    # S.fill_rack()
    turn_number = S.GAME_SETTINGS['turn']
    S.set_rack("ERNSTLU?")
    # ERNSTLU? finds LÜSTERN the highest scoring play.
    # Joker-Letter would be Ü
    # should display as L(Ü)STERN

    while turn_number < 3:
        print(f"  Turn No.: {turn_number}  ".center(80, "-"))
        Display.print_board()

        # prepare the result-lists
        # placeable_suggestions = []
        # possible_plays = []

        if C.is_first_turn() is True:
            print("It's the first turn.")
            center = L.get_center_of_board()
            # the board is symmetrical, might as well start on the x-axis
            # find the usable area (x-axis along the center)

            usable_positions = WS.find_usable_positions(center, "x")
            # usable_area = D.Area(position_list=usable_positions)
            # convert to search parameters
            # find words according to those parameters

            first_subturn = Game.SubTurn(usable_positions)
            # possible_words = WS.create_words(usable_area)

            L.execute_play(first_subturn.highest_scoring_play)
        else:
            print("It's the second turn.")
            possible_plays = []
            S.set_rack("BEDARF")
            # TODO: encapsulate creating a Turn.
            # creating a turn requires:
            # the board state (the already placed words), the rack
            # the search-parameters

            # possible_plays = WS.find_all_plays()
            S.increase_turn()
            raise NotImplementedError("NYI")
            pass

        # if len(possible_plays) == 0:
        #     raise NotImplementedError("NYI. There's no available Play. Swap out some letters.")

        # sorted_plays = sorted(possible_plays,
        #                       key=operator.attrgetter('score'),
        #                       reverse=True)
        # highest_scoring_play = sorted_plays[0]
        # lowest_scoring = sorted_plays[-1]
        # print("highest scoring play:")
        # print(highest_scoring_play)
        #
        # print("lowest scoring play:")
        # print(lowest_scoring)


        # Display.print_board()

        print("  End of turn.  ".center(80, "-"))
        S.fill_rack()
        S.increase_turn()


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

def play_finding_parallel():
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

    parallel_subturn = Game.SubTurn(parallel_area.position_list)
    print("highest scoring play:")
    pprint.pprint(parallel_subturn.highest_scoring_play)
    print("Plays possible on I9 to L9:")
    pprint.pprint(parallel_subturn.possible_plays)
    #TODO: finish. Passes if DU and UR are parallel bonus-plays.


def read_from_position():
    S.reset()
    S.set_rack("ERDE")
    play_erde = D.Play("ERDE", "G8", "X")
    L.execute_play(play_erde)

    reader_word = L.read_on_position("G8", "X")
    print("reader_word", reader_word)
    print("word equals the word in the previous play:", reader_word == play_erde.word)




def log_searching():
    S.reset()
    # finding the plays.
    S.set_rack("ERNSTLÜ")
    play_lustern = D.Play("LÜSTERN", "G8", "X")
    L.execute_play(play_lustern)
    S.increase_turn()
    #Display.print_board()

    # Set BORSTE
    S.set_rack("BORTE")
    play_borste = D.Play("BORSTE", "I5", "Y")
    L.execute_play(play_borste)
    S.increase_turn()
    #Display.print_board()

    # Set ERBE
    S.set_rack("ERE")
    play_erbe = D.Play("ERBE", "G5", "X")
    L.execute_play(play_erbe)
    S.increase_turn()
    #Display.print_board()

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


def test_all():
    word_search()
    rack_simple()
    rack_complete()
    play_creating()
    entire_turn()
    position_finding()
    word_finding_by_entire_word()
    area_finding()
    play_finding_by_position()
    log_searching()

play_finding_parallel()
# read_from_position()