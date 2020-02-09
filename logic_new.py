# TODO: rename to solver.py
# TODO: "ER" is, strangely enough, not a word in german.txt
# TODO: implement complex_plays
# TODO: Cleanup. A whole lot.

# TODO: Datatype.Play needs to know what rack-letters are used
# TODO: also streamline a Turn - make that a datatype using the parameters
# TODO: Datatype.Play needs to know what Jokers are used for.
# TODO:


import re
import shelve
import threading

from typing import Union
from typing import Iterable
from copy import deepcopy
from os import path
import pprint
import operator
from random import shuffle, choice
from math import floor
from itertools import permutations


class Settings:
    # gameSettings are referred to a lot. Using a dirty global.
    GAME_SETTINGS = None
    # same dirty global for resetting the boards
    INITIAL_SETTINGS = None

    # TODO: read user-definable settings from a file
    app_path = path.abspath(path.curdir)

    searchPrecision = 0  # default: 100, 0 = search all.

    # LANGUAGE AND LETTER DISTRIBUTION
    languages = {"german": "German",
                 "english": "English (UK)"}

    dictionaries = {"german": path.join(app_path, "german.txt"),
                    "english": path.join(app_path, "english.txt")}

    # MODE
    # see https://en.wikipedia.org/wiki/Scrabble#Gameboard_formats
    modes = {"normal": "Regular Scrabble (15x15)",
             "super": "Super Scrabble (21x21)"}

    boards = {"normal":  # columns A-O, rows 1-15
        [
            # A   B  C   D   E   F   G   H   I   J   K   L   M   N   O
            ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 1
            ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 2
            ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 3
            ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 4
            ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 5
            ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 6
            ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 7
            ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 8
            ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 9
            ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 10
            ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 11
            ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 12
            ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 13
            ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 14
            ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '']  # 15
        ],
        "super":  # columns A-U, rows 1-21
            [
                # A  B   C   D   E   F   G   H   I   J   K   L   M   N   O   P   Q   R   S   T   U
                ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 1
                ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 2
                ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 3
                ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 4
                ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 5
                ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 6
                ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 7
                ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 8
                ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 9
                ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 10
                ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 11
                ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 12
                ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 13
                ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 14
                ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 15
                ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 16
                ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 17
                ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 18
                ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 19
                ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 20
                ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']  # 21
            ]}

    # Board for the Word- and Letter-modifiers:
    # global BOARD_MODIFIERS
    board_modifiers = {
        "normal": [  # center on H8
            # A   B   C   D    E    F    G    H    I    J    K    L    M    N    O
            ['TW', '', '', 'DL', '', '', '', 'TW', '', '', '', 'DL', '', '', 'TW'],  # 1
            ['', 'DW', '', '', '', 'TL', '', '', '', 'TL', '', '', '', 'DW', ''],  # 2
            ['', '', 'DW', '', '', '', 'DL', '', 'DL', '', '', '', 'DW', '', ''],  # 3
            ['DL', '', '', 'DW', '', '', '', 'DL', '', '', '', 'DW', '', '', 'DL'],  # 4
            ['', '', '', '', 'DW', '', '', '', '', '', 'DW', '', '', '', ''],  # 5
            ['', 'TL', '', '', '', 'TL', '', '', '', 'TL', '', '', '', 'TL', ''],  # 6
            ['', '', 'DL', '', '', '', 'DL', '', 'DL', '', '', '', 'DL', '', ''],  # 7
            ['TW', '', '', 'DL', '', '', '', 'c', '', '', '', 'DL', '', '', 'TW'],  # 8
            ['', '', 'DL', '', '', '', 'DL', '', 'DL', '', '', '', 'DL', '', ''],  # 9
            ['', 'TL', '', '', '', 'TL', '', '', '', 'TL', '', '', '', 'TL', ''],  # 10
            ['', '', '', '', 'DW', '', '', '', '', '', 'DW', '', '', '', ''],  # 11
            ['DL', '', '', 'DW', '', '', '', 'DL', '', '', '', 'DW', '', '', 'DL'],  # 12
            ['', '', 'DW', '', '', '', 'DL', '', 'DL', '', '', '', 'DW', '', ''],  # 13
            ['', 'DW', '', '', '', 'TL', '', '', '', 'TL', '', '', '', 'DW', ''],  # 14
            ['TW', '', '', 'DL', '', '', '', 'TW', '', '', '', 'DL', '', '', 'TW']  # 15
        ],
        "super": [  # center on K11
            # A   B    C    D    E   F   G    H    I   J    K   L    M    N    O   P   Q   R   S   T   U
            ['QW', '', '', 'DL', '', '', '', 'TW', '', '', 'DL', '', '', 'TW', '', '', '', 'DL', '', '', 'QW'],  # 1
            ['', 'DW', '', '', 'TL', '', '', '', 'DW', '', '', '', 'DW', '', '', '', 'TL', '', '', 'DW', ''],  # 2
            ['', '', 'DW', '', '', 'QL', '', '', '', 'DW', '', 'DW', '', '', '', 'QL', '', '', 'DW', '', ''],  # 3
            ['DL', '', '', 'TW', '', '', 'DL', '', '', '', 'TW', '', '', '', 'DL', '', '', 'TW', '', '', 'DL'],  # 4
            ['', 'TL', '', '', 'DL', '', '', '', 'TL', '', '', '', 'TL', '', '', '', 'DL', '', '', 'TL', ''],  # 5
            ['', '', 'QL', '', '', 'DW', '', '', '', 'DL', '', 'DL', '', '', '', 'DW', '', '', 'QL', '', ''],  # 6
            ['', '', '', 'DL', '', '', 'DW', '', '', '', 'DL', '', '', '', 'DW', '', '', 'DL', '', '', ''],  # 7
            ['TW', '', '', '', '', '', '', 'DW', '', '', '', '', '', 'DW', '', '', '', '', '', '', 'TW'],  # 8
            ['', 'DW', '', '', 'TL', '', '', '', 'TL', '', '', '', 'TL', '', '', '', 'TL', '', '', 'DW', ''],  # 9
            ['', '', 'DW', '', '', 'DL', '', '', '', 'DL', '', 'DL', '', '', '', 'DL', '', '', 'DW', '', ''],  # 10
            ['DL', '', '', 'TW', '', '', 'DL', '', '', '', 'c', '', '', '', 'DL', '', '', 'TW', '', '', 'DL'],  # 11
            ['', '', 'DW', '', '', 'DL', '', '', '', 'DL', '', 'DL', '', '', '', 'DL', '', '', 'DW', '', ''],  # 12
            ['', 'DW', '', '', 'TL', '', '', '', 'TL', '', '', '', 'TL', '', '', '', 'TL', '', '', 'DW', ''],  # 13
            ['TW', '', '', '', '', '', '', 'DW', '', '', '', '', '', 'DW', '', '', '', '', '', '', 'TW'],  # 14
            ['', '', '', 'DL', '', '', 'DW', '', '', '', 'DL', '', '', '', 'DW', '', '', 'DL', '', '', ''],  # 15
            ['', '', 'QL', '', '', 'DW', '', '', '', 'DL', '', 'DL', '', '', '', 'DW', '', '', 'QL', '', ''],  # 16
            ['', 'TL', '', '', 'DL', '', '', '', 'TL', '', '', '', 'TL', '', '', '', 'DL', '', '', 'TL', ''],  # 17
            ['DL', '', '', 'TW', '', '', 'DL', '', '', '', 'TW', '', '', '', 'DL', '', '', 'TW', '', '', 'DL'],  # 18
            ['', '', 'DW', '', '', 'QL', '', '', '', 'DW', '', 'DW', '', '', '', 'QL', '', '', 'DW', '', ''],  # 19
            ['', 'DW', '', '', 'TL', '', '', '', 'DW', '', '', '', 'DW', '', '', '', 'TL', '', '', 'DW', ''],  # 20
            ['QW', '', '', 'DL', '', '', '', 'TW', '', '', 'DL', '', '', 'TW', '', '', '', 'DL', '', '', 'QW']  # 21
        ]
    }

    # Dict for the Word- and Letter-Modifiers:
    # global MODIFIER_WORD
    MODIFIER_WORD = {"DW": 2,  # Double Word
                     "TW": 3,  # Triple Word
                     "QW": 4,  # Quadruple Word
                     "DL": 1,  # Double Letter
                     "TL": 1,  # Triple Letter
                     "QL": 1,  # Quadruple Letter
                     "c": 2,  # Center Square
                     "": 1}  # Empty Square

    MODIFIER_LETTER = {"DW": 1,  # Double Word
                       "TW": 1,  # Triple Word
                       "QW": 1,  # Quadruple Word
                       "DL": 2,  # Double Letter
                       "TL": 3,  # Triple Letter
                       "QL": 4,  # Quadruple Letter
                       "c": 1,  # Center Square
                       "": 1}  # Empty Square

    # list for temporary Positions
    RECENT_TEMPORARY_POSITIONS = []

    # Point-values for letters:
    # Keys are letters, values are point-values in the game.
    # German: https://en.wikipedia.org/wiki/Scrabble_letter_distributions#German
    # English: https://en.wikipedia.org/wiki/Scrabble_letter_distributions#English
    LETTERS = {
        "normal": {
            "german": {
                "E": 1, "N": 1, "S": 1, "I": 1, "R": 1,
                "U": 1, "A": 1, "D": 1, "H": 2, "G": 2,
                "L": 2, "O": 2, "M": 3, "B": 3, "W": 3,
                "Z": 3, "C": 4, "F": 4, "K": 4, "P": 4,
                "Ä": 6, "J": 6, "Ü": 6, "V": 6, "Ö": 8,
                "X": 8, "Q": 10, "Y": 10, "?": 0, "T": 1
            },
            "english": {
                "L": 1, "S": 1, "U": 1, "N": 1, "R": 1,
                "T": 1, "O": 1, "A": 1, "I": 1, "E": 1,
                "G": 2, "D": 2, "B": 3, "C": 3, "M": 3,
                "P": 3, "F": 4, "H": 4, "V": 4, "W": 4,
                "Y": 4, "K": 5, "J": 8, "X": 8, "Q": 10,
                "Z": 10, "?": 0
            }
        },
        "super": {
            "german": {
                "E": 1, "N": 1, "S": 1, "I": 1, "R": 1,
                "U": 1, "A": 1, "D": 1, "H": 2, "G": 2,
                "L": 2, "O": 2, "M": 3, "B": 3, "W": 3,
                "Z": 3, "C": 4, "F": 4, "K": 4, "P": 4,
                "Ä": 6, "J": 6, "Ü": 6, "V": 6, "Ö": 8,
                "X": 8, "Q": 10, "Y": 10, "?": 0, "T": 1
            },
            "english": {
                "L": 1, "S": 1, "U": 1, "N": 1, "R": 1,
                "T": 1, "O": 1, "A": 1, "I": 1, "E": 1,
                "G": 2, "D": 2, "B": 3, "C": 3, "M": 3,
                "P": 3, "F": 4, "H": 4, "V": 4, "W": 4,
                "Y": 4, "K": 5, "J": 8, "X": 8, "Q": 10,
                "Z": 10, "?": 0
            }
        }
    }

    # Letter distribution
    # Keys are letters,
    # values are the amount of that letter in the bag at the start of the game.
    AMOUNT = {
        "normal": {
            "german": {
                "E": 15, "N": 9, "S": 7, "I": 6, "R": 6,
                "U": 6, "A": 5, "D": 4, "H": 4, "G": 3,
                "L": 3, "O": 3, "M": 4, "B": 2, "W": 1,
                "Z": 1, "C": 2, "F": 2, "K": 2, "P": 1,
                "Ä": 1, "J": 1, "Ü": 1, "V": 1, "Ö": 1,
                "X": 1, "Q": 1, "Y": 1, "?": 0  # TODO: reset to 2
            },
            "english": {
                "L": 4, "S": 4, "U": 4, "N": 6, "R": 6,
                "T": 6, "O": 8, "A": 9, "I": 9, "E": 12,
                "G": 3, "D": 4, "B": 2, "C": 2, "M": 2,
                "P": 2, "F": 2, "H": 2, "V": 2, "W": 2,
                "Y": 2, "K": 1, "J": 1, "X": 1, "Q": 1,
                "Z": 1, "?": 2
            }
        },
        "super": {
            "german": {
                # double the letters from the normal game,
                # but remove one E, I, N, R each.
                "E": 29, "N": 17, "S": 14, "I": 11, "R": 11,
                "U": 12, "A": 10, "D": 8, "H": 8, "G": 6,
                "L": 6, "O": 6, "M": 8, "B": 4, "W": 2,
                "Z": 2, "C": 4, "F": 4, "K": 4, "P": 2,
                "Ä": 2, "J": 2, "Ü": 2, "V": 2, "Ö": 2,
                "X": 2, "Q": 2, "Y": 2, "?": 4
            },
            "english": {
                "L": 7, "S": 10, "U": 7, "N": 13, "R": 13,
                "T": 15, "O": 15, "A": 16, "I": 13, "E": 24,
                "G": 5, "D": 8, "B": 4, "C": 6, "M": 6,
                "P": 4, "F": 4, "H": 5, "V": 3, "W": 4,
                "Y": 4, "K": 2, "J": 2, "X": 2, "Q": 2,
                "Z": 2, "?": 4
            }
        }
    }

    @staticmethod
    def get_game_settings(game_mode: str = "normal",
                          game_language: str = "german",
                          max_rack_letters: int = 7,
                          shuffle_bag_after_drawing=True) -> dict:
        mode_string = game_mode.casefold()
        language_string = game_language.casefold()

        # guard clause: Language and Mode are available
        if mode_string not in Settings.modes.keys():
            raise ValueError(f"""{mode_string} is not a mode.
            Valid modes: {list(Settings.modes.keys())}""")
        if language_string not in Settings.languages.keys():
            raise ValueError(f"""{language_string} is not a language.
            Valid languages: {list(Settings.languages.keys())}""")

        size_x = len(Settings.boards[mode_string])
        size_y = len(Settings.boards[mode_string][0])

        center_x = floor(size_x / 2)
        center_y = floor(size_y / 2)

        bag = Settings.create_bag(Settings.AMOUNT[mode_string][language_string])
        shuffle(bag)
        print("DEBUG: Bag is now...")
        print(bag)

        return {"language": language_string,
                "mode": mode_string,
                "dictionary": Settings.dictionaries[language_string],
                "words": Dictionary.load_shelve(language_string),
                "letter_score": Settings.LETTERS[mode_string][language_string],
                "letter_amounts": Settings.AMOUNT[mode_string][language_string],
                "bag": bag,
                "shuffle_after_drawing": shuffle_bag_after_drawing,
                "rack": [],
                "max_rack_letters": max_rack_letters,
                "board_actual": deepcopy(Settings.boards[mode_string]),
                "board_temporary": deepcopy(Settings.boards[mode_string]),
                "board_modifiers": deepcopy(Settings.board_modifiers[mode_string]),
                "size_x": size_x,
                "size_y": size_y,
                "center": (center_x, center_y),
                "turn": 1
                }

    @classmethod
    def set_game_settings(cls, settings: dict):
        cls.GAME_SETTINGS = deepcopy(settings)
        cls.INITIAL_SETTINGS = deepcopy(settings)

    @classmethod
    def reset(cls):
        cls.GAME_SETTINGS = deepcopy(cls.INITIAL_SETTINGS)
        print("*" * 80)
        print("RESET".center(80, " "))
        print("*" * 80)

    @classmethod
    def get_turn(cls):
        return cls.GAME_SETTINGS['turn']

    @classmethod
    def increase_turn(cls):
        cls.GAME_SETTINGS['board_temporary'] = deepcopy(cls.GAME_SETTINGS['board_actual'])
        cls.GAME_SETTINGS['turn'] += 1

    @staticmethod
    def create_bag(letter_distribution: dict) -> list:
        print("creating bag...")

        keys = letter_distribution.keys()
        # print("all keys:", keys)
        result_list = []
        for letter in keys:
            # print("filling with letter:", letter)
            amount = letter_distribution[letter]
            # print("# in distribution:", amount)
            result_list.extend([letter] * amount)
        #     print("added into the bag:", [letter]*amount)
        # print("Bag done.")
        # print(result_list)
        shuffle(result_list)
        return result_list

    @classmethod
    def fill_rack(cls):
        current_rack = cls.get_rack()
        length_on_rack = len(current_rack)
        # print("length of rack on initiation:", length_on_rack)
        max_length = cls.GAME_SETTINGS['max_rack_letters']
        bag = cls.GAME_SETTINGS['bag']
        shuffle_bag = cls.GAME_SETTINGS['shuffle_after_drawing']
        # print("maximum no. of letters:", max)

        if length_on_rack == max_length:
            return

        # print("letters in bag:", bag)
        # print("amount:", len(bag))

        while length_on_rack < max_length and len(bag) > 0:
            # print("while loop reset")
            letter_to_draw = choice(bag)
            # print("letter to be drawn:", letter_to_draw)

            amount_of_letter_in_bag = bag.count(letter_to_draw)
            # print(f"amount of letter <{letter_to_draw}> in bag: {amount_of_letter_in_bag}")
            if amount_of_letter_in_bag >= 1:
                current_rack.append(letter_to_draw)
                bag.pop(bag.index(letter_to_draw))
                # print("appended to the rack.")
                # print("rack now:", current_rack)
                # amount_of_letter_in_bag -= 1
            else:
                # print("no letters in the bag.")
                # bag.pop(bag.index(letter_to_draw))
                continue
            # print("length of rack in loop:", length_on_rack)
            length_on_rack = len(current_rack)

            if shuffle_bag is True:
                shuffle(bag)

        cls.GAME_SETTINGS['rack'] = current_rack
        return

    # Debug-Method
    @classmethod
    def get_rack(cls):
        return cls.GAME_SETTINGS['rack']

    # Debug-Method
    @classmethod
    def set_rack(cls, letters: Union[str, list]):
        # global GAMESETTINGS
        # GAMESETTINGS['rack'] = list(letters)
        if isinstance(letters, str) is True:
            cls.GAME_SETTINGS['rack'] = list(letters)
        elif isinstance(letters, list) is True:
            cls.GAME_SETTINGS['rack'] = letters
        else:
            raise TypeError("set_rack() takes either str or list.")


class Datatypes:
    class GameSettings(object):
        # TODO: make GameSettings an Object and rewrite all the calls to it.
        def __init__(self,
                     game_mode: str = "normal",
                     game_language: str = "german",
                     max_rack_letters: int = 7,
                     shuffle_bag_after_drawing: bool = True):
            mode_string = game_mode.casefold()
            language_string = game_language.casefold()

            # guard clause: Language and Mode are available
            if mode_string not in Settings.modes.keys():
                raise ValueError(f"""{mode_string} is not a mode.
                Valid modes: {list(Settings.modes.keys())}""")
            if language_string not in Settings.languages.keys():
                raise ValueError(f"""{language_string} is not a language.
                Valid languages: {list(Settings.languages.keys())}""")

            size_x = len(Settings.boards[mode_string])
            size_y = len(Settings.boards[mode_string][0])

            center_x = floor(size_x / 2)
            center_y = floor(size_y / 2)

            bag = Settings.create_bag(Settings.AMOUNT[mode_string][language_string])
            shuffle(bag)
            # print("DEBUG: Bag is now...")
            # print(bag)

            # return {"language": anguage_string,
            #         "mode": mode_string,
            #         "dictionary": Settings.dictionaries[language_string],
            #         "words": Dictionary.load_shelve(language_string),
            #         "letter_score": Settings.LETTERS[mode_string][language_string],
            #         "letter_amounts": Settings.AMOUNT[mode_string][language_string],
            #         "bag": bag,
            #         "shuffle_after_drawing": shuffle_bag_after_drawing,
            #         "rack": [],
            #         "max_rack_letters": max_rack_letters,
            #         "board_actual": deepcopy(Settings.boards[mode_string]),
            #         "board_temporary": deepcopy(Settings.boards[mode_string]),
            #         "board_modifiers": deepcopy(Settings.board_modifiers[mode_string]),
            #         "size_x": size_x,
            #         "size_y": size_y,
            #         "center": (center_x, center_y),
            #         "turn": 1
            #         }
            pass

        pass

    class Suggestion(object):
        def __init__(self,
                     word: str,
                     position: str,
                     axis: str):
            self.word = word
            self.position = position
            self.axis = axis
            self.end = Logic.get_end_position(word, position, axis)
            self.used_positions = Logic.convert_positions_to_list(self.position, self.end)

        def __repr__(self):
            return f"<{self.word}, {self.position}, {self.axis}>"

    class Play(object):

        # TODO: move WordSearch.CreatePlay here
        def __init__(self,
                     word: str,
                     position: str,
                     axis: str,
                     rack_for_play: Union[str, list, None] = None,
                     play_type: str = "default",
                     is_temporary: bool = False):
            self.word = word
            self.position = position
            self.start = position
            self.is_temporary = is_temporary
            self.end = Logic.get_end_position(word, position, axis)
            self.axis = axis
            self.type = play_type
            self.used_rack = rack_for_play
            self.used_positions = Logic.convert_positions_to_list(self.start, self.end)
            self.length = len(self.used_positions)
            self.extendable_at = Logic.get_axial_neighbors_of_list(self.used_positions, self.axis)
            self.extended_plays = []
            self.play_previous = []
            self.execution, \
            self.joker_letters, \
            self.joker_positions = self.find_execution()
            self.bonus_plays = []
            self.score_bonus = 0
            self.score_basic = Logic.score_play(self, is_temporary)
            self.score_total = 0
            self.turn = Settings.get_turn()
            self.active = True

            self.update_total_score()
            # self.non_empty_tuple = []

        def __cmp__(self, other):
            if isinstance(other, Datatypes.Play) is False:
                return False
            else:
                same_axis = self.axis == other.axis
                same_start = self.start == other.start
                same_end = self.end == other.end
                same_word = self.word == other.word
                if same_axis and same_start and same_end and same_word:
                    return True

        def set_inactive(self):
            self.active = False

        def extend_play(self, list_of_plays: list):
            for extension_play in list_of_plays:
                self.bonus_plays.append(extension_play)
                self.score_bonus += extension_play.score_basic
                self.extended_plays.append(extension_play)
                # old_score = self.score_bonus
                # new_score = old_score + extension_play.score_basic
                # self.score_bonus = new_score
                self.update_total_score()
            # clean version:
            #

        def update_total_score(self):
            if self.type == "extension":
                self.score_total = self.score_basic
            else:
                self.score_total = self.score_basic + self.score_bonus

        def find_execution(self) -> tuple:
            # combine find_jokers and find_used_rack_letters
            # Rack:             ERNSTL?
            # Play.Word:        LÜSTERN
            # Play.Position:    "G8"
            # Play.Execution: [(G8, "L"), (H8, "?"), (I8, "S"), (J8, "T")...]
            result = []
            jokers = []
            joker_positions = []

            if self.used_rack is None:
                temp_rack = deepcopy(Settings.get_rack())
            else:
                temp_rack = self.used_rack

            # print("calling find_execution with self:", self)
            # print("rack:", temp_rack)

            non_empty_positions, \
            non_empty_letters = Logic.get_non_empty_tuple(self.position,
                                                          self.used_positions[-1])

            # find which letters (or jokers) go to which position.
            for letter_index, play_position in enumerate(self.used_positions):
                play_letter = self.word[letter_index]
                result_letter = None
                if play_position in non_empty_positions:
                    continue
                else:
                    if play_letter in temp_rack:
                        result_letter = temp_rack.pop(temp_rack.index(play_letter))
                    else:
                        if "?" in temp_rack:
                            result_letter = temp_rack.pop(temp_rack.index("?"))
                            jokers.append(play_letter)
                            joker_positions.append(play_position)
                    if result_letter is None:
                        continue
                    else:
                        result.append((result_letter, play_position))
                        # print("appending:", (letter, play_position))
            return result, jokers, joker_positions

        def __repr__(self):
            left = f"{self.word}".ljust(28)
            center = f"{self.start}-{self.end}:{self.axis}".ljust(16)
            right = f"score:{self.score_total}({self.score_basic}+{self.score_bonus})".ljust(20)
            bonus = ""
            # bonus_left = ""
            # bonus_center = ""
            # bonus_right = ""
            if len(self.bonus_plays) > 0:
                for bonus_play in self.bonus_plays:
                    bonus += f"\n>> +{bonus_play.word}".ljust(28)
                    bonus += f"{bonus_play.start}-{bonus_play.end}:{bonus_play.axis}".ljust(16)
                    bonus += f"score:{bonus_play.score_basic}".ljust(20)
            rep_string = "".join([left, center, right, bonus])
            return rep_string

    class Area:
        def __init__(self,
                     start: str = None,
                     end: str = None,
                     position_list: list = None,
                     rack: Union[str, list] = None):


            if rack is None:
                self.rack = Settings.get_rack()
            else:
                self.rack = list(rack)

            if position_list is None:
                self.start = start
                self.end = end
                self.position_list = Logic.convert_positions_to_list(start, end)
                self.axis = Logic.get_axis(start, end)
            else:
                self.position_list = position_list
                self.start = position_list[0]
                self.end = position_list[-1]
                self.axis = Logic.get_axis(self.start, self.end)

            both_axes = {"x", "y"}
            self.opposite_axis = both_axes.difference(set(self.axis))

            print(f"Area from {self.start} to {self.end}:")
            self.non_empty_positions, \
            self.non_empty_letters = Logic.get_non_empty_tuple(self.start,
                                                               self.end)
            self.is_continuous = Checks.is_position_list_continuous(self.non_empty_positions)

            self.available_letters = self.rack + self.non_empty_letters
            self.unique_letters = list(set(self.available_letters))

            if len(self.available_letters) >= len(self.position_list):
                self.max_length = len(self.position_list)
            else:
                self.max_length = len(self.available_letters)
            self.min_length = len(self.non_empty_letters)
            if self.min_length < 2:
                self.min_length = 2

            self.neighbors = self.get_area_neighbors()
            # print("neighbors:", self.neighbors)
            self.contested_at = self.get_occupied_neighbors()
            # print("contested at these positions:", self.contested_at)
            # self.contested_plays = [WordLog.find_active_play_by_position(contested_pos)
            #                         for contested_pos
            #                         in self.contested_at]
            self.contested_plays = WordLog.find_active_play_by_position(self.contested_at)
            # convert contested_at to position-lists


            print("contested plays:")
            pprint.pprint(self.contested_plays, indent=2)
            # the name is confusing.
            self.extension_crossover_positions = self.get_extension_crossovers()

        def get_extension_crossovers(self) -> list:
            # compares the given position_list with any contested plays
            if len(self.contested_at) == 0:
                return []
            else:
                result_list = []
                if len(self.contested_at) != len(self.contested_plays):
                    raise ValueError("contested_plays and contested_at have different lengths.")
                for contest_position, contest_play in zip(self.contested_at,
                                                          self.contested_plays):
                    extension_set = set(contest_play.extendable_at)
                    area_position_set = set(self.position_list)
                    intersecting_positions = list(area_position_set.intersection(extension_set))

                    result_list.extend(intersecting_positions)
                return result_list

        def get_area_neighbors(self) -> list:
            neighbor_list = []
            positions_to_check = [position for position
                                  in self.position_list
                                  if position not in self.non_empty_positions]

            for current_position in positions_to_check:
                all_neighbors = Logic.get_all_neighbors(current_position)
                neighbor_list.extend(list(all_neighbors.values()))
            unique_neighbors = list(set(neighbor_list))
            result_list = [position for position
                           in unique_neighbors
                           if position not in self.position_list
                           and Checks.is_position_valid(position) is True]
            return result_list

        def get_occupied_neighbors(self) -> list:
            if len(self.neighbors) == 0:
                return []

            result_list = [position for position
                           in self.neighbors
                           if Checks.is_position_empty(position) is False]
            return result_list

        def __repr__(self):
            repr_str = f"""
                start:\t{self.start}
                end:\t{self.end}
                position_list{self.position_list}
                axis:\t{self.axis}
                rack:\t{self.rack}
                non_empty_positions:\t{self.non_empty_positions}
                non_empty_letters:\t{self.non_empty_letters}
                is_continuous:\t{self.is_continuous}
                available_letters:\t{self.available_letters}
                max_length:\t{self.max_length}
                min_length:\t{self.min_length}
                unique_letters:\t{self.available_letters}
                """
            return repr_str


class Game:
    class SubTurn(Datatypes.Area):
        # Subturn: Plays possible for an Area in a single direction -
        # ex. Position H8 along X
        # read: The collection of Plays around a single position

        def __init__(self,
                     position_list_subturn):
            super().__init__(position_list=position_list_subturn)

            self.possible_plays = WordSearch.find_plays_for_area(self)

            if len(self.possible_plays) > 0:
                self.highest_scoring_play = sorted(self.possible_plays,
                                                   key=operator.attrgetter('score_total'),
                                                   reverse=True)[0]
                print("Highest Scoring Play:")
                print(self.highest_scoring_play)
            else:
                self.highest_scoring_play = None

    class Turn(object):
        # Turn: The collection of Subturns, the Board-State and the Rack
        def __init__(self,
                     previous_plays: list,
                     rack: list):
            # raise NotImplementedError("still TODO.")
            # TODO:
            # look at all filled positions (either via the given board_state or the global WordLog)
            # find the usable areas/subturns around each position
            # TODO: make the search for usable areas consider extensions and combinations too
            # >make it a "ruler" around any position, given the No. of Letters on the rack
            # !!todo from here.
            # >consider filled positions along the way too -
            # >extensions, open plays and "complex" (merging gaps between filled positions)
            # >(or extending a word by a single letter with a play perpendicular to its last letter)
            # >are supposed to be found in a single function
            # >draw this up.
            # create words/plays
            # execute the highest scoring play

            # play-type-matrix:
            # open: opposite axis to an existing word, no occupied neighbors along the area
            # extension: same axis to existing word, no occupied neighbors along the area
            # merge: either axis, but tries to combine occupied positions
            # perpendicular: single-letter extension, but opposite axis to existing word.
            # if any of these has occupied neighbors, check if the touching word exists.
            # maybe make a global setting for the word-search to even consider touching-words
            # if so, search for 2 areas: one that's standard (unoccupied neighbors),
            # the other ignoring occupied neighbors for its searches.

            pass

            raise NotImplementedError("TODO")


class Checks:
    @staticmethod
    def is_position_valid(position_string: str) -> bool:
        """
        Takes a position, returns True if the position is on the board.
        "A1" --> True
        "Y28" --> False
        """
        if position_string is None:
            return False

        x, y = Logic.convert_position_to_coordinate(position_string)
        if x is None or y is None:
            return False
        elif Checks.is_coordinate_valid(x, y) is False:
            return False
        else:
            return True

    @staticmethod
    def is_coordinate_valid(x: int,
                            y: int) -> bool:
        """
        Take x,y-coordinate, return True if the coordinate is on the board.
        """
        if (0 <= x <= (Settings.GAME_SETTINGS["size_x"] - 1)) and (
                0 <= y <= (Settings.GAME_SETTINGS["size_y"] - 1)):
            return True
        else:
            return False

    @staticmethod
    def is_position_empty(position: str,
                          is_temporary: bool = False) -> bool:
        """
        Take a position (optionally on the temporary board),
        return True if the Square is empty.
        """
        x, y = Logic.convert_position_to_coordinate(position)

        # positions outside of the board can't have letters on them,
        # but still count as empty.
        if Checks.is_coordinate_valid(x, y) is False:
            return True

        function_board = Logic.get_board(is_temporary)

        if len(function_board[y][x]) == 0:
            return True
        else:
            return False

    @staticmethod
    def is_position_open(position_to_check: str,
                         original_position: str,
                         neighbors: dict = None) -> bool:
        """
        Look at all neighbors of positionToCheck, return True
        if all of them are empty.
        A non-empty originalPosition is ignored.
        :param position_to_check:
        :param original_position:
        :param neighbors:
        :return:
        """
        if position_to_check == original_position:
            return True

        if neighbors is None:
            neighbors = Logic.get_all_neighbors(position_to_check)

        neighbor_positions = list(neighbors.values())
        # print(f"neighborPositions for {position_to_check}: \t {neighborPositions}")
        for position in neighbor_positions:
            # TODO: Squash Bug that considers the original position closed....
            if position == original_position:
                continue
            # Positions at the edges of the field have None as a neighbor.
            if Checks.is_position_valid(position) is False:
                continue
            if Checks.is_position_empty(position) is False:
                return False
        return True

    @staticmethod
    def is_position_closed(position_to_check: str,
                           neighbors: dict = None) -> bool:
        """
        Look at all neighbors of position_to_check.
        Return True if *all* of them already contain letters.

        :param position_to_check:
        :param neighbors:
        :return:
        """
        if neighbors is None:
            neighbors = Logic.get_all_neighbors(position_to_check)

        neighbor_positions = list(neighbors.values())
        for position in neighbor_positions:
            if Checks.is_position_empty(position) is True:
                return False
        return True

    @staticmethod
    def is_end_position_and_axis_not_none(end_position: str = None,
                                          axis: str = None) -> bool:
        """
        Take end_position and an axis, raise ValueError if both are None.
        Return True otherwise.
        """
        if axis is None and end_position is None:
            raise ValueError("""
            Either axis or end_position must be given.
            """)
        else:
            return True

    @staticmethod
    def is_position_neighbor(position_a: str,
                             position_b: str) -> bool:
        neighbors = list(Logic.get_all_neighbors(position_a).values())
        if position_b in neighbors:
            return True
        else:
            return False

    @staticmethod
    def is_position_list_continuous(position_list: list) -> bool:
        # print("position_list:", position_list)
        # print(type(position_list))
        # guard clause: more than one position is required.
        if len(position_list) <= 1:
            return False

        # check if all given positions are neighbors in any direction
        previous_x, previous_y = Logic.convert_position_to_coordinate(position_list[0])
        for currentPosition in position_list:
            current_x, current_y = Logic.convert_position_to_coordinate(currentPosition)
            if -1 <= previous_x - current_x <= 1 and -1 <= previous_y - current_y <= 1:
                previous_x = current_x
                previous_y = current_y
                continue
            else:
                return False
        return True

    @staticmethod
    def is_word_placeable(word: Datatypes.Suggestion) -> bool:
        # attempts to place the given word on the temporary board
        # return True if the word from the temporary board equals word_to_place
        length = len(word.word)
        end_position = Logic.modify_position_by_axis(word.position,
                                                     length,
                                                     word.axis)
        Logic.set_word_to_position(word.word,
                                   word.position,
                                   end_position,
                                   word.axis,
                                   is_temporary=True)
        temporary_word = Logic.get_word_from_position(word.position,
                                                      end_position,
                                                      is_temporary=True)
        # print("temporary word reads:", temporary_word)
        is_placeable = (temporary_word == word.word)
        # else:
        #     raise ValueError("Unsupported type given to parameter 'word':", type(word))

        Logic.remove_temporary_positions(length)
        return is_placeable

    @staticmethod
    def is_number_of_jokers_correct(word: str,
                                    jokers: str = '') -> bool:
        if "?" in word:
            if jokers == '' or (word.count("?") != len(jokers)):
                raise ValueError(f"""
                    Mismatch: 
                    Jokers: {word.count("?")}
                    Replacement letters: {len(jokers)}
                    """)
        return True

    @staticmethod
    def is_number_of_sub_plays_valid(list_sub_plays: list,
                                     list_cross_positions: list):
        if len(list_sub_plays) == len(list_cross_positions):
            return True
        else:
            return False

    @staticmethod
    def is_any_letter_in_word(word_to_check: str, given_letters: list) -> bool:
        """
        Return True if any of given_letters is in wordToCheck.
        Return False if *none* of the given_letters are in the word.

        :param word_to_check:
        :param given_letters:
        :return: Boolean
        """
        for letter in given_letters:
            if letter in word_to_check:
                return True
            else:
                continue
        return False

    @staticmethod
    def is_any_element_in_list(element_to_find: Iterable,
                               list_to_search: list) -> bool:
        items_to_find = set(element_to_find)
        set_to_search = set(list_to_search)

        for item in items_to_find:
            if item in set_to_search:
                return True
        return False

    @staticmethod
    def is_word_buildable(word_to_check: str,
                          letters_given: str,
                          max_length: int = 0):
        num_jokers = letters_given.count("?")
        if max_length > 0:
            if len(word_to_check) > max_length:
                return False

        for letter in set(word_to_check):
            count_source = letters_given.count(letter)
            count_target = word_to_check.count(letter)
            if count_source < count_target:
                # must have at least 1 joker,
                # and the number of Letters in Source need to be
                # equal to counted letters + number of jokers
                if num_jokers > 0 and count_source + num_jokers >= count_target:
                    num_jokers -= 1
                    continue
                return False
            else:
                continue
        return True

    @staticmethod
    def is_letter_on_actual_board(position: str):
        letter_temporary = Logic.get_letter_from_position(position, is_temporary=True)
        letter_actual = Logic.get_letter_from_position(position, is_temporary=False)

        return letter_temporary == letter_actual

    @staticmethod
    def is_first_turn():
        return Settings.GAME_SETTINGS['turn'] == Settings.INITIAL_SETTINGS['turn']

    @staticmethod
    def is_word_in_dictionary(word: str):
        # returns True if a word exists in the dictionary.
        # TODO: optimisation: take the shortest wordlist to check for the word.
        first_letter = word[0]
        second_letter = word[1]
        word_length = len(word)
        word_list = WordSearch.word_list_by_letters(word_length,
                                                    first_letter,
                                                    second_letter)
        if word in word_list:
            return True
        return False


class Logic:
    # Helper-function to return either the temporary or actual board.
    @staticmethod
    def get_board(is_temporary: bool):
        if is_temporary is True:
            return Settings.GAME_SETTINGS["board_temporary"]
        else:
            return Settings.GAME_SETTINGS["board_actual"]

    @staticmethod
    def get_center_of_board() -> str:
        # x = floor(Settings.GAME_SETTINGS["size_x"] / 2)
        # y = floor(Settings.GAME_SETTINGS["size_y"] / 2)
        # return Logic.convert_coordinate_to_position(x, y)
        x, y = Settings.GAME_SETTINGS['center']
        return Logic.convert_coordinate_to_position(x, y)

    @staticmethod
    def find_substring(string_to_find: str,
                       word_to_search: str) -> list:
        # # search_substring_indices from StackExchange
        # # https://codereview.stackexchange.com/questions/146834/function-to-find-all-occurrences-of-substring
        # """
        # Generate indices of where substring begins in string
        # >>> find_substring('me', "The cat says meow, meow"))
        # [13, 19]
        #
        # Returns -1 if no letter is found.
        # """
        last_found = -1  # Begin at -1 so the next position to search from is 0
        while True:
            # Find next index of substring, by starting after its
            # last known position
            last_found = word_to_search.find(string_to_find, last_found + 1)
            if last_found == -1:
                break  # All occurrences have been found
            yield last_found

    @staticmethod
    def convert_coordinate_to_position(x: int, y: int):
        """
        Convert the x/y-coordinate to the Scrabble-Notation.
        Returns None if the given x/y-value is invalid.

        0, 0    -> "A1"
        14, 14  -> "O15"
        26, 65  -> None
        """
        if Checks.is_coordinate_valid(x, y) is False:
            return None
        else:
            # chr(65) = "A"
            result_x = chr(x + 65)
            result_y = str(y + 1)

        return str(result_x + result_y)

    @staticmethod
    def convert_position_to_coordinate(position_string: str) -> tuple:
        """
        Convert the given Position-String of a square back to x/y-coordinates.
        Returns None if the Position is invalid.

        "A1" -> 0,0
        "O15" -> 14,14
        "Z65" -> None, None
        """
        # ord("A") = 65
        x = int(ord(position_string[0]) - 65)
        y = int(position_string[1:]) - 1
        if Checks.is_coordinate_valid(x, y) is False:
            return None, None
        else:
            return x, y

    @staticmethod
    def get_value_from_board(board: list,
                             x: int = None,
                             y: int = None,
                             position: str = None) -> str:
        """
        Return the value of a given position/coordinate from a given board
        (BOARD_ACTUAL, BOARD_TEMPORARY, BOARD_MODIFIERS).
        """
        if position is not None:
            x, y = Logic.convert_position_to_coordinate(position)
        return board[y][x]

    @staticmethod
    def set_value_to_board(value: str,
                           board: list,
                           x: int = None,
                           y: int = None,
                           position: str = None):
        """
        Set a value to a given position/coordinate onto the given board
        (BOARD_ACTUAL, BOARD_TEMPORARY, BOARD_MODIFIERS).
        """
        if position is not None:
            x, y = Logic.convert_position_to_coordinate(position)
        board[y][x] = value

    @staticmethod
    def modify_position_by_axis(position: str,
                                modify_by: int,
                                axis: str,
                                use_nearest_valid: bool = False):
        if axis.casefold() == "x":
            new_position = Logic.modify_position_numeric(position,
                                                         modify_x=modify_by,
                                                         use_nearest_valid=use_nearest_valid)
        elif axis.casefold() == "y":
            new_position = Logic.modify_position_numeric(position,
                                                         modify_y=modify_by,
                                                         use_nearest_valid=use_nearest_valid)
        else:
            raise ValueError(f"Parameter 'axis' takes x or y. Given:{axis}")

        return new_position

    @staticmethod
    def modify_position_numeric(position: str,
                                modify_x: int = 0,
                                modify_y: int = 0,
                                use_nearest_valid: bool = False):
        """
        Take a position-string, Return a position-string
        with the X/Y value changed.

        Return None if the resulting position is invalid.
        When use_nearest_valid is True, return the position closest
        to the boundary of the board instead of None.

        Either modify_x/Y or modValue/axis
        "H8", (-7, -7) -> "A1"
        "A1", (-20, -20) -> None

        """
        if position is None:
            return None  # return invalid position

        x, y = Logic.convert_position_to_coordinate(position)

        new_x = x + modify_x
        new_y = y + modify_y

        if Checks.is_coordinate_valid(new_x, new_y) is True:
            return Logic.convert_coordinate_to_position(new_x, new_y)
        elif use_nearest_valid is True:
            min_x = 0
            min_y = 0
            max_x = Settings.GAME_SETTINGS['size_x'] - 1
            max_y = Settings.GAME_SETTINGS['size_y'] - 1

            if new_x < min_x:
                new_x = 0
            elif new_x > max_x:
                new_x = max_x

            if new_y < min_y:
                new_y = 0
            elif new_y > max_y:
                new_y = max_y

            return Logic.convert_coordinate_to_position(new_x, new_y)
        else:
            return None

    @staticmethod
    def get_axis(start_position: str, end_position: str = None):
        if start_position[0] == end_position[0]:  # Vertical axis
            return "Y"
        elif start_position[1:] == end_position[1:]:  # Horizontal axis
            return "X"
        else:
            # print(f"""
            # Warning: get_axis({start_position}, {end_position}):
            # \t {start_position} and {end_position} are not on the same X or Y-Axis.
            # """)
            return None

    @staticmethod
    def get_end_position(word: str, start_position: str, axis: str):
        # -1 since we already know the start_position
        offset = len(word) - 1

        if axis.casefold() == "x":
            end_position = Logic.modify_position_numeric(start_position,
                                                         modify_x=offset)
        elif axis.casefold() == "y":
            end_position = Logic.modify_position_numeric(start_position,
                                                         modify_y=offset)
        else:
            raise ValueError("Axis' arguments are either 'X' or 'Y'.")
        if Checks.is_position_valid(end_position):
            return end_position
        else:
            return None

    @staticmethod
    def get_end_position_and_axis(word: str,
                                  start_position: str,
                                  end_position: str,
                                  axis: str) -> tuple:
        """
        Determine the end_position and axis of a word, given its starting position
        and either the intended axis or the end_position.

        Returning: end_position, axis

        "TEST", "A1", axis = "X"-> "D1", "X"
        "TEST", "A1", "A4"      -> "A4", "Y"
        """
        # guard clause: end_position and axis are already given.
        if end_position is not None and axis is not None:
            return end_position, axis

        if Checks.is_end_position_and_axis_not_none(end_position, axis) is True:
            if axis is None:
                axis = Logic.get_axis(start_position,
                                      end_position)
                return end_position, axis
            if end_position is None:
                end_position = Logic.get_end_position(word,
                                                      start_position,
                                                      axis)
                return end_position, axis

    @staticmethod
    def convert_positions_to_list(start_position: str,
                                  end_position: str = None) -> list:
        """
        Create a list of Positions from start_position to end_position (inclusive).

        A1", "A5" -> ["A1", "A2", "A3", "A4", "A5"]
        """
        result_list = []

        start_x, start_y = Logic.convert_position_to_coordinate(start_position)

        if end_position is None or end_position == start_position:
            return [start_position]
        else:
            end_x, end_y = Logic.convert_position_to_coordinate(end_position)

        axis = Logic.get_axis(start_position, end_position)

        if axis is None:
            # print(f"""
            # Warning: convert_positions_to_list({start_position}, {end_position}):
            # \t {start_position} and {end_position} are not on the same X or Y-Axis.
            # """)
            return []
        else:
            if axis.casefold() == "y":  # Vertical
                # endY+1 so the ending coordinate is included
                for currentY in range(start_y, end_y + 1):
                    result_list.append(
                        Logic.convert_coordinate_to_position(start_x, currentY))
            elif axis.casefold() == "x":  # Horizontal
                for currentX in range(start_x, end_x + 1):
                    result_list.append(
                        Logic.convert_coordinate_to_position(currentX, start_y))

        return result_list

    @staticmethod
    def sort_position_list(position_list: list, axis: str):

        coordinate_list = [(Logic.convert_position_to_coordinate(position))
                           for position
                           in position_list]
        if axis.casefold() == "x":
            sorted_coordinates = sorted(coordinate_list)
        else:
            reversed_list = []
            # reverse the value pairs
            for coordinate in coordinate_list:
                x = coordinate[0]
                y = coordinate[1]
                reversed_list.append((y, x))
            sorted_reversed = sorted(reversed_list)
            sorted_coordinates = []
            for reversed_coordinate in sorted_reversed:
                y = reversed_coordinate[0]
                x = reversed_coordinate[1]
                sorted_coordinates.append((x, y))

        sorted_positions = [Logic.convert_coordinate_to_position(x, y)
                            for (x, y)
                            in sorted_coordinates]
        return sorted_positions

    @staticmethod
    def get_axial_neighbors_of_list(position_list: list, axis: str) -> list:
        """
        Find 2 direct neighbors of the start and end of position_list along axis.
        Returns only valid, unoccupied positions or an empty list if no valid
        positions are found.

        :param position_list: ["B1", "C1", "D1"]
        :param axis: "X"
        :return: ["A1", "E1"]
        """
        result_list = []
        offset = -1
        end_positions = (position_list[0], position_list[-1])
        for position in end_positions:
            if offset > 1:
                break
            extension = Logic.modify_position_by_axis(
                position,
                offset,
                axis)

            if extension is not None and Checks.is_position_empty(extension):
                result_list.append(extension)
            offset += 2

        return result_list

    @staticmethod
    def get_letter_from_position(position: str,
                                 is_temporary: bool = False,
                                 show_joker: bool = False):
        """
        Return a Letter from a given position (optionally from the temporary board).
        If the position contains a joker, show_joker = True returns "?"
        instead of the letter, and the regular Letter otherwise.
        """
        x, y = Logic.convert_position_to_coordinate(position)

        if x is None or y is None:
            return None
        else:
            function_board = Logic.get_board(is_temporary)
            position_value = Logic.get_value_from_board(function_board, x, y)
            # length of the returned Value is 2 if there's a Joker on it.
            if len(position_value) == 2:
                if show_joker is True:
                    # Joker is always on index 0 on a Square.
                    return position_value[0]
                else:
                    return position_value[1]
            else:
                return position_value

    @staticmethod
    def delete_letter_from_position(position: str = None,
                                    x: int = None, y: int = None,
                                    is_temporary: bool = False):
        """
        Write an empty string to the position of a board
        (either Settings.BOARD_TEMPORARY or Settings.BOARD_ACTUAL).
        """
        function_board = Logic.get_board(is_temporary)

        if position is not None:
            f_x, f_y = Logic.convert_position_to_coordinate(position)
            # function_board[y][x] = ''
        else:
            f_x, f_y = x, y

        Logic.set_value_to_board('', function_board, f_x, f_y)

    @staticmethod
    def set_letter_to_position(letter: str,
                               position: str,
                               is_temporary=False):
        """
        Write a letter to a position on the actual or temporary board.
        Does not remove a letter from the player's Rack.
        """
        function_board = Logic.get_board(is_temporary)

        x, y = Logic.convert_position_to_coordinate(position)

        if Checks.is_position_empty(position, is_temporary) is True:
            # function_board[y][x] = letter
            Logic.set_value_to_board(letter, function_board, x, y)
            if is_temporary is True:
                Logic.add_temporary_position(position)
        else:
            pass
            # print(f"set_letter_to_position: position {position} is not empty, taken up by {function_board[y][x]}")

    @staticmethod
    # TODO: simplify this (extract functions)
    def get_non_empty_tuple(start_position: str,
                            end_position: str = None,
                            is_temporary: bool = False,
                            axis: str = None) -> tuple:
        """
        Returns a tuple with 2 lists:
        (position_list, result_letters)
        given start_position to end_position (optionally from the temporary board).
        If no end_position is given and axis is given "X" or "Y",
        return non-empty positions from entire row (X) / column (Y) of start_position.
        """

        result_positions = []
        result_letters = []

        x, y = Logic.convert_position_to_coordinate(start_position)

        # guard clause: invalid positions of start and end.
        if Checks.is_coordinate_valid(x, y) is False:
            return [], []

        if end_position is not None:
            if Checks.is_position_valid(end_position) is False:
                return [], []

        if axis is not None:
            if axis.casefold() == "x":
                # start_position and end_position become the outermost squareSettings.
                size_x = Settings.GAME_SETTINGS['size_x'] - 1
                start_position = Logic.convert_coordinate_to_position(0, y)
                end_position = Logic.convert_coordinate_to_position(size_x - 1, y)

            elif axis.casefold() == "y":
                size_y = Settings.GAME_SETTINGS['size_y'] - 1
                start_position = Logic.convert_coordinate_to_position(x, 0)
                end_position = Logic.convert_coordinate_to_position(x, size_y)
            else:
                raise ValueError("axis takes either 'X' or 'Y'.")
            position_list = Logic.convert_positions_to_list(start_position,
                                                            end_position)

        else:  # axis IS None:
            if end_position is None:
                end_position = start_position
            position_list = Logic.convert_positions_to_list(start_position,
                                                            end_position)

        for current_position in position_list:
            if Checks.is_position_empty(current_position, is_temporary) is False:
                result_letters.append(Logic.get_letter_from_position(current_position,
                                                                     is_temporary))
                result_positions.append(current_position)

        return result_positions, result_letters

    @staticmethod
    def add_temporary_position(position: str):
        """
        Write a position to the global list of temporary positions.
        """
        Settings.RECENT_TEMPORARY_POSITIONS.append(position)

    @staticmethod
    def remove_temporary_positions(number_of_entries: int = 0):
        max_length = len(Settings.RECENT_TEMPORARY_POSITIONS)
        if number_of_entries == 0:
            end = max_length
        else:
            end = number_of_entries
        for counter in range(0, end):
            if len(Settings.RECENT_TEMPORARY_POSITIONS) == 0:
                return
            recent_position = Settings.RECENT_TEMPORARY_POSITIONS.pop(-1)
            if Checks.is_letter_on_actual_board(recent_position) is True:
                continue
            else:
                Logic.delete_letter_from_position(recent_position, is_temporary=True)

    @staticmethod
    def get_word_from_position(start_position: str,
                               end_position: str,
                               is_temporary: bool = False,
                               show_joker: bool = False) -> str:
        """
        Return a string from start_position to end_position on the actual
        or temporary board.

        Word "TESTING" from A1 to A7 (vertical, along column "A"):
        "A1", "A4" -> "TEST"
        """
        position_list = Logic.convert_positions_to_list(start_position,
                                                        end_position)
        result_string = ""

        if len(position_list) == 0:
            return result_string

        for position in position_list:
            letter = Logic.get_letter_from_position(position,
                                                    is_temporary,
                                                    show_joker)
            result_string = "".join([result_string, letter])
            # resultString += get_letter_from_position(position, is_temporary, show_joker)
        return result_string

    @staticmethod
    def set_word_to_position(word: str,
                             start_position: str,
                             end_position: str = None,
                             axis: str = None,
                             joker_letters: str = '',
                             is_temporary: bool = False):

        """
        Place a Word onto the board, given the word-string and a start_position.
        Either end_position or axis is required.

        If jokers are in word, the same number of jokerReplacements is needed.
        jokerReplacement(s) are placed alongside their jokers into a Position.

        Example:
        Set word "STAR" from A1 to A4:
        "STAR", "A1", "A4"
        "STAR", "A1", axis = "X"
        "ST?R", "A1", "A4", jokerReplacements = "A" -> A3 contains "?A"
        """
        # IDEA: print a warning-message if the end_position gets overwritten.
        # this is quite a cumbersome solution...

        # check if number of jokers and replacements match
        Checks.is_number_of_jokers_correct(word, joker_letters)

        jokers_used_index = 0
        end_position, axis = Logic.get_end_position_and_axis(word,
                                                             start_position,
                                                             end_position,
                                                             axis)

        position_list = Logic.convert_positions_to_list(start_position,
                                                        end_position)

        for positionIndex, currentLetter in enumerate(word):
            if currentLetter == "?":
                # join the intended letter for the word to the right of the joker.
                currentLetter += ''.join(joker_letters[jokers_used_index])
                jokers_used_index += 1
            current_position = position_list[positionIndex]
            Logic.set_letter_to_position(currentLetter,
                                         current_position,
                                         is_temporary)

    @staticmethod
    def get_word_multiplier(start_position: str,
                            end_position: str = None,
                            is_temporary: bool = False) -> int:
        # TODO: check if the current field is

        """
        Return the total Word-Multiplier for the area from start_position to end_position.
        Word-multipliers stack multiplicatively and each can only be used once.

        on gameMode "normal":
        "A1", "A15" -> 27 (3 * 3 * 3)
        """
        multiplier = 1
        board_modifiers = Settings.GAME_SETTINGS["board_modifiers"]

        if end_position is None or end_position == start_position:
            field = Logic.get_value_from_board(board_modifiers,
                                               position=start_position)

            multiplier *= Settings.MODIFIER_WORD.get(field)
        else:
            position_list = Logic.convert_positions_to_list(start_position, end_position)
            for currentPosition in position_list:
                if Checks.is_position_empty(currentPosition,
                                            is_temporary) is False:
                    continue

                field = Logic.get_value_from_board(board_modifiers,
                                                   position=currentPosition)
                if field is None or len(field) == 0:  # "" is returned on an empty field.
                    continue
                else:
                    multiplier *= Settings.MODIFIER_WORD.get(field)

        return multiplier

    @staticmethod
    def get_letter_multiplier(position: str) -> int:
        """
        Return the Letter-Multiplier for a position.
        Letter-multipliers are counted before word-multipliers and can
        only be used once.
        """
        multiplier = 1
        field = Logic.get_value_from_board(Settings.GAME_SETTINGS["board_modifiers"], position=position)
        multiplier *= Settings.MODIFIER_LETTER.get(field)
        return multiplier

    @staticmethod
    def score_play(play: Datatypes.Play,
                   is_temporary: bool):
        """
        Return the total score of a word placed on a board (temporary or actual).
        """
        score = 0
        word_multiplier = Logic.get_word_multiplier(play.position,
                                                    play.used_positions[-1],
                                                    is_temporary)

        # if len(play.execution) == 0:
        #     for positionIndex, currentLetter in enumerate(play.word):
        #         current_position = play.used_positions[positionIndex]
        #         score += Logic.score_letter(currentLetter,
        #                                     current_position,
        #                                     is_temporary)
        # else:
        #     for letter, position in play.execution:
        #         score += Logic.score_letter(letter, position, is_temporary)

        for positionIndex, currentLetter in enumerate(play.word):
            current_position = play.used_positions[positionIndex]
            # TODO: Joker still gets scored like the actual letter
            # find the joker-letter in the execution and take that position.
            if current_position in play.joker_positions:
                continue

            score += Logic.score_letter(currentLetter,
                                        current_position,
                                        is_temporary)

        return score * word_multiplier

    @staticmethod
    def score_letter(letter: str,
                     position: str,
                     is_temporary: bool = False) -> int:
        """
        Return the Score of a single Letter on a Position (temporary or actual board).
        """
        if letter == "?":
            return 0

        points = Settings.GAME_SETTINGS["letter_score"].get(letter)

        if Checks.is_position_empty(position, is_temporary) is True:
            multiplier = Logic.get_letter_multiplier(position=position)
            return points * multiplier
        else:
            # letter = Logic.get_letter_from_position(position, is_temporary)
            # points = Settings.GAME_SETTINGS["letter_score"].get(letter)
            return points

    @staticmethod
    def execute_play(play: Datatypes.Play,
                     is_temporary: bool = False,
                     add_to_log: bool = True):

        temporary_rack = deepcopy(Settings.get_rack())
        joker_index = 0

        # Logic.remove_from_rack(play.used_rack)

        # Logic.set_word_to_position(play.word,
        #                            play.position,
        #                            axis=play.axis,
        #                            is_temporary=is_temporary)
        # if len(play.execution) == 2:
        #     # play.execution, play.joker_letters = WordSearch.find_execution(play)
        #     raise ValueError("Execution not found")
        #     # print("execution in execute_play:", play.execution)

        # Figure out if the execution differs from the
        # if it does, replace play.word with the changed word
        for letter, position in play.execution:
            if letter == "?":
                replaced_letter = play.joker_letters[joker_index]
                both_letters = ''.join([letter, replaced_letter])
                # print(both_letters)
                # set both letters to the boeard
                Logic.set_letter_to_position(both_letters,
                                             position,
                                             is_temporary)
                joker_index += 1
            else:
                Logic.set_letter_to_position(letter, position, is_temporary)
            temporary_rack.remove(letter)

        if is_temporary is False:
            Settings.set_rack(temporary_rack)

        if add_to_log is True:
            WordLog.write_log(play)

    @staticmethod
    def remove_from_rack(letters: str):
        # TODO: not an elegant solution - Settings.get_rack() points to a global
        # find solution that takes the value from the global and updates once
        # instead of letter-by-letter.
        current_rack = deepcopy(Settings.get_rack())
        for current_letter in letters:
            current_rack.remove(current_letter)
        Settings.set_rack(current_rack)

    @staticmethod
    def get_one_neighbor(position: str,
                         cardinal_direction: str,
                         show_letters: bool = False) -> str:

        cardinals = ["north", "east", "south", "west"]
        if cardinal_direction not in cardinals:
            raise ValueError(f"{cardinal_direction} is not a cardinal.")

        directions = {"north": (0, -1),
                      "east": (+1, 0),
                      "south": (0, +1),
                      "west": (-1, 0)}
        mod_x, mod_y = directions[cardinal_direction]
        neighbor_position = Logic.modify_position_numeric(position,
                                                          mod_x,
                                                          mod_y)

        if show_letters is False:
            return neighbor_position
        else:
            return Logic.get_letter_from_position(neighbor_position)

    @staticmethod
    def get_all_neighbors(position: str,
                          show_letters: bool = False) -> dict:

        north = Logic.get_one_neighbor(position, "north", show_letters)
        east = Logic.get_one_neighbor(position, "east", show_letters)
        south = Logic.get_one_neighbor(position, "south", show_letters)
        west = Logic.get_one_neighbor(position, "west", show_letters)
        all_neighbors = {
            "north": north,
            "east": east,
            "south": south,
            "west": west
        }
        return all_neighbors


class WordLog:
    all_plays = []
    active_plays = []

    @classmethod
    def get_active_plays(cls) -> list:
        if len(cls.all_plays) == 0:
            return []

        active_plays = [play for play
                        in cls.all_plays
                        if play.active is True]
        return active_plays

    @classmethod
    def write_log(cls, play: Datatypes.Play):
        # global GAMESETTINGS
        # end_position = Logic.get_end_position(play.word,
        #                                       play.position,
        #                                       play.axis)
        # used_positions = Logic.convert_positions_to_list(play.position,
        #                                                  end_position)
        #
        # log_dict = {"word": play.word,
        #             "position": play.position,
        #             "axis": play.axis,
        #            "used_positions": used_positions,
        #             "score": play.score,
        #             "type": play.type,
        #             "turn": Settings.GAME_SETTINGS['turn']}
        # cls.all_plays.append(log_dict)
        if len(play.bonus_plays) > 0:
            for bonus_play in play.bonus_plays:
                cls.write_log(bonus_play)

        cls.all_plays.append(play)
        cls.deactivate_extended_plays()
        cls.active_plays = cls.get_active_plays()

    @classmethod
    def read_log(cls, index=None):
        if index is None:
            return cls.all_plays
        else:
            return cls.all_plays[index]

    @classmethod
    def deactivate_extended_plays(cls):
        # Goal:
        # iterate over the entire log
        # only mark the plays with the highest length active
        # if there's more than one play on a position with the same axis
        # (find_plays_by_position needs to be accurate for this)

        all_play_tuples = [(logged_play.start, logged_play.axis)
                           for logged_play
                           in cls.read_log()]
        # print("all_starting_positions:", all_play_tuples)

        for current_play_tuple in all_play_tuples:
            # find all plays that one starting position uses along an axis
            # if there's only one play, skip
            # find the longest
            start, axis = current_play_tuple
            plays_on_positon = cls.find_plays_with_axis(start, axis)
            if len(plays_on_positon) == 1:
                continue
            else:
                lengths_of_all_plays = [list_ex_play.length
                                        for list_ex_play
                                        in plays_on_positon]
                length_longest_play = max(lengths_of_all_plays)
                for play in plays_on_positon:
                    if play.length < length_longest_play:
                        play.set_inactive()

    @classmethod
    def find_plays_with_axis(cls, position: str, axis: str) -> list:
        # find the latest play on a given filled position
        # TODO: make this able to use multiple positions as well
        # TODO: combine this function with finx_play_by_extension
        result_list = []
        for logged_play in cls.all_plays:
            if logged_play.active is False:
                continue
            is_in_used_positions = position in logged_play.used_positions
            is_on_same_axis = axis.casefold() == logged_play.axis.casefold()

            if is_in_used_positions and is_on_same_axis:
                result_list.append(logged_play)
        return result_list

    @classmethod
    def find_active_play_by_position(cls,
                                     position: Union[str, list]) -> list:
        result_list = []
        # print("calling find_active_play_by_position...")
        called_active_plays = cls.get_active_plays()

        if isinstance(position, str):
            position_list = [position]
        else:
            position_list = position
        # TODO: line 625
        # See line 625 - find ALL active plays by position
        for current_position in position_list:
            for logged_play in called_active_plays:
                position_in_used = current_position in logged_play.used_positions
                # axis_is_equal = axis in logged_play.axis
                if position_in_used and logged_play not in result_list:
                    result_list.append(logged_play)
        return result_list

    @classmethod
    # TODO: this is also wonky.
    def find_active_play_by_extension_position(cls, position: str) -> list:
        # find the latest play on a given extension-position
        result_list = []
        # for logged_play in cls.all_plays[-1::-1]:
        for logged_play in cls.active_plays[-1::-1]:
            if position in logged_play.extendable_at:
                result_list.append(logged_play)
        return result_list


class Scratch:
    @staticmethod
    def find_plays(attribute,
                   value,
                   strict: bool = False) -> list:
        entire_log = WordLog.read_log()

        if strict:
            result_list = [play for play
                           in entire_log
                           if play.__getattribute__(attribute) == value
                           and play.active is True]
        else:
            result_list = [play for play
                           in entire_log
                           if value in play.__getattribute__(attribute)
                           and play.active is True]

        return result_list

    @staticmethod
    def find_areas(previous_play_list: list, rack: list) -> list:
        # Current Idea: Take a Position, make an area according to the ruler
        # if there's no previous play, the area around the center of the board is used.
        # TODO: DEBUG,
        previous_play_list = [Datatypes.Play("LÜSTERN", "G8", "X")]
        # iterate over every filled position
        already_checked_positions = []
        offset = len(rack)
        axes = {"x", "y"}

        for current_play in previous_play_list:
            filled_positions = current_play.used_positions
            # find both axes
            extenison_axis = current_play.axis
            open_axis = axes.difference(set(extenison_axis)).pop()
            for current_filled_position in filled_positions:
                # find the bottom-most and top-most position along it
                # extract function to Logic.find_ruler_positions (name pending)
                (bottom,
                 top,
                 position_list_to_search) = Scratch.get_ruler_positions(open_axis)

        pass

    @staticmethod
    def find_all_areas_per_play(play_to_search: Datatypes.Play,
                                axis: str,
                                rack: list) -> list:
        # for testing
        # create areas around every used position (much like the "ruler" in the TODO
        # of the Turn-Object)
        result_list = []
        if play_to_search.axis == axis:
            ruler_positions = Scratch.get_ruler_positions(
                play_to_search.used_positions, axis, rack)
            result_list.append(Datatypes.Area(position_list=ruler_positions))
        else:
            for current_position in play_to_search.used_positions:
                ruler_positions = Scratch.get_ruler_positions(
                    current_position, axis, rack)
                result_list.append(Datatypes.Area(position_list=ruler_positions))

        return result_list

    @staticmethod
    def get_ruler_positions(positions: Union[str, list],
                            axis: str,
                            rack: list) -> list:

        if isinstance(positions, list):
            start_at = positions[0]
            if len(positions) == 1:
                end_at = start_at
            else:
                end_at = positions[-1]
        elif isinstance(positions, str):
            start_at = positions
            end_at = start_at
        else:
            raise ValueError("positions takes either list or str.")

        offset = len(rack)

        start = Logic.modify_position_by_axis(start_at,
                                              -offset,
                                              axis,
                                              True)
        end = Logic.modify_position_by_axis(end_at,
                                            +offset,
                                            axis,
                                            True)
        position_list = Logic.convert_positions_to_list(start, end)

        return position_list


class WordSearch:
    # a word on a Position is only a "Play" when it could be set on the board
    # according to the scrabble-ruleset.

    # create 2 different search-pattnerns:
    # first is "open" positions -> find_usable_positions
    # second is "busy" positions ->
    # busy positions could try to connect 2 letters in an area instead of avoiding then
    @staticmethod
    def find_usable_positions(position: str, axis: str) -> list:
        # return list of squares with empty neighbors,
        # considering the number of letters on the rack
        original_position = position
        usable_positions = [original_position]
        max_offset = len(Settings.get_rack())

        bottom_found = False
        ceiling_found = False

        for current_offset in range(1, max_offset + 1):
            # TODO: refactor: use if to determine either negative or positive offset
            if ceiling_found is False:
                higher_position = Logic.modify_position_by_axis(original_position,
                                                                +current_offset,
                                                                axis,
                                                                True)
                higher_neighbors = Logic.get_all_neighbors(higher_position)
                if Checks.is_position_open(higher_position,
                                           original_position,
                                           higher_neighbors):
                    if higher_position not in usable_positions:
                        usable_positions.append(higher_position)
                else:
                    ceiling_found = True

            if bottom_found is False:
                lower_position = Logic.modify_position_by_axis(original_position,
                                                               -current_offset,
                                                               axis,
                                                               True)
                lower_neighbors = Logic.get_all_neighbors(lower_position)
                if Checks.is_position_open(lower_position,
                                           original_position,
                                           lower_neighbors):
                    if lower_position not in usable_positions:
                        usable_positions.append(lower_position)
                else:
                    bottom_found = True

        if usable_positions == [original_position]:
            return []
        else:
            sorted_usable_positions = Logic.sort_position_list(usable_positions, axis)
            # print("Usable Positions:", sorted_usable_positions)
            # print(sorted_usable_positions)
            return sorted_usable_positions

    @staticmethod
    def find_placeable_words(area: Datatypes.Area,
                             word_list: list) -> list:
        # TODO: requires cleanup (extract functions), this is heavily nested.

        result_list = []

        for current_word in word_list:
            all_starting_positions = WordSearch.find_starting_position(current_word,
                                                                       area)
            # print(f"starting positions for {current_word}", starting_positions)
            if len(all_starting_positions) > 0:
                for starting_position in all_starting_positions:
                    suggestion = Datatypes.Suggestion(current_word,
                                                      starting_position,
                                                      area.axis)
                    if (Checks.is_first_turn() is False) \
                            and (len(area.non_empty_positions) == 0):
                        if Checks.is_any_element_in_list(area.extension_crossover_positions,
                                                         suggestion.used_positions) is False:
                            continue

                    if Checks.is_word_placeable(suggestion):
                        # print(f"{current_word} on {starting_position} along {area.axis} is placeable.")
                        result_list.append(suggestion)
        return result_list

    @staticmethod
    def find_affected_crossovers(area: Datatypes.Area,
                                 suggestion: Datatypes.Suggestion) -> list:
        set_used_play = set(suggestion.used_positions)
        set_crossover = set(area.extension_crossover_positions)
        result_list = list(set_used_play.intersection(set_crossover))

        return result_list

    @staticmethod
    def find_endpoints_of_crossovers(position: str,
                                     crossover_play: Datatypes.Play) -> tuple:
        start = crossover_play.start
        end = crossover_play.end
        if Checks.is_position_neighbor(position, start):
            # print(f"affected_position {position} is a next to the START of the affected play. ({start})")
            result_start = position
            result_end = end
        elif Checks.is_position_neighbor(position, end):
            # print(f"affected_position {position} is a next to the END of the affected play. ({end})")
            result_start = start
            result_end = position
        else:
            raise ValueError(f"Affected cross-positions were tried, but were not neighbors of any affected play.")

        return result_start, result_end

    @staticmethod
    def find_extension_plays(area: Datatypes.Area,
                             placeable_word: Datatypes.Suggestion) -> list:
        result_list = []
        non_existing_words = []
        correct_words = []
        # print("current placeable_word:", placeable_word)
        # place the word, and any filled extension crossovers will check
        raw_play = Datatypes.Play(placeable_word.word,
                                  placeable_word.position,
                                  placeable_word.axis,
                                  play_type="temporary",
                                  is_temporary=True)
        # print("unchecked_play:")
        # print(unchecked_play)
        affected_cross_positions = WordSearch.find_affected_crossovers(area,
                                                                       placeable_word)
        # print("affected_cross_positions", affected_cross_positions)
        Logic.execute_play(raw_play,
                           is_temporary=True,
                           add_to_log=False)
        # if the word exists. the play is only valid if ALL extensions
        # are valid words.
        for affected_position in affected_cross_positions:
            # find the affected play by extension_position
            affected_plays = WordLog.find_active_play_by_extension_position(affected_position)
            for play_to_extend in affected_plays:
                create_play = False

                (extension_start,
                 extension_end) = WordSearch.find_endpoints_of_crossovers(affected_position,
                                                                          play_to_extend)
                #
                # print("temporary_start:", extension_start)
                # print("temporary_end:", extension_end)

                new_temporary_word = Logic.get_word_from_position(extension_start,
                                                                  extension_end,
                                                                  is_temporary=True)

                if new_temporary_word in non_existing_words:
                    continue
                elif new_temporary_word in correct_words:
                    create_play = True
                else:
                    if Checks.is_word_in_dictionary(new_temporary_word):
                        correct_words.append(new_temporary_word)
                        create_play = True
                    else:
                        non_existing_words.append(new_temporary_word)
                        continue

                if create_play is True:
                    extension_play = Datatypes.Play(new_temporary_word,
                                                    extension_start,
                                                    play_to_extend.axis,
                                                    play_type="extension",
                                                    is_temporary=True)
                    result_list.append(extension_play)
        Logic.remove_temporary_positions(len(raw_play.word))

        # checked_play = Datatypes.Play(placeable_word.word,
        #                               placeable_word.position,
        #                               placeable_word.axis)
        # # print("checked play is now:")
        # # print(checked_play)
        # result_list.append(checked_play)
        return result_list

    @staticmethod
    def find_plays_for_area(area: Datatypes.Area) -> list:
        result_list = []

        words = WordSearch.create_words(area)
        # print("all words:")
        # pprint.pprint(words)

        all_placeable_words = WordSearch.find_placeable_words(area, words)

        if len(area.extension_crossover_positions) == 0:
            # print("no extension crossovers.")
            for placeable_word in all_placeable_words:
                play = Datatypes.Play(placeable_word.word,
                                      placeable_word.position,
                                      placeable_word.axis)

                # check for busy neighbors and create bonus plays for existing
                # valid words,
                ## TODO: EXTRACT FUNCTION
                affected_neighbors = list(set(play.used_positions).intersection(set(area.neighbors)))
                # select the play(s) by used position
                # (return muliple plays in a list if the given position is a list)
                affected_plays = WordLog.find_active_play_by_position(affected_neighbors)
                result_list.append(play)
        else:
            # print("extension crossovers exist.")
            # complex, but more accurate:
            # iterate over the contested positions
            # figure out how what letters can extend the existing play
            # (make it like the execution on the actual play), place letters on the temporary board
            # take the area via regex and reduce all_placeable_words to only its matches.
            # also consider the changed rack for the temporary-placed words.

            # simpler:
            # print("all all_placeable_words:")
            # pprint.pprint(all_placeable_words)
            for current_suggestion in all_placeable_words:

                extension_plays = WordSearch.find_extension_plays(area, current_suggestion)
                crossover_positions = WordSearch.find_affected_crossovers(area, current_suggestion)

                if Checks.is_number_of_sub_plays_valid(extension_plays,
                                                       crossover_positions):
                    play = Datatypes.Play(current_suggestion.word,
                                          current_suggestion.position,
                                          current_suggestion.axis)
                    play.extend_play(extension_plays)
                    result_list.append(play)

        return result_list

    @staticmethod
    def find_starting_position(word: str,
                               area: Datatypes.Area) -> list:
        """
        returns a list of available starting Positions
        for a word within the area of the search-parameters

        :param word: the word to be tried
        :param area: created via WordSearch.create_search_parameters(Area)
        :return:
        """

        # TODO: Cleanup (extract functions)
        # or rewrite since this is messily nested.

        length = len(word)
        raw_starting_positions = []
        checked_starting_positions = []
        center = Logic.get_center_of_board()

        # Testing Situation:
        # "ERNST" on Rack, no letter placed.
        # center of the board must be touched, but offset is
        # at least 1 off the center (words cant start on center)
        # should return ["ERNST", "G8", "x"]
        # print(f"find_starting_position for <{word}>")
        # find fixed positions and figure out if those are continuous
        if len(area.non_empty_positions) == 0:
            # the word can basically be placed anywhere within the area
            for current_area_position in area.position_list:
                end_position = Logic.modify_position_by_axis(current_area_position,
                                                             length - 1,
                                                             area.axis)
                if end_position is None:
                    continue

                if Checks.is_first_turn() is True:
                    if length < 3:
                        # print("Length lower than 3")
                        return []
                    else:
                        # define the starting positions to be tried
                        raw_starting_positions = area.position_list[0:-length]

                    # center position must be used
                    # center position must be surrounded by at least 1 letter on each side
                    for start_position in raw_starting_positions:
                        end_index = area.position_list.index(start_position) + length - 1
                        in_loop_end_position = area.position_list[end_index]
                        position_list = Logic.convert_positions_to_list(start_position,
                                                                        in_loop_end_position)
                        # cut off the outermost used positions
                        position_list.pop(0)
                        position_list.pop(-1)
                        if center in position_list:
                            checked_starting_positions.append(start_position)
                else:
                    if end_position in area.position_list:
                        raw_starting_positions.append(current_area_position)

        else:
            # check if the fixed positions are continuous
            if area.is_continuous is True:
                # all fixed positions must be in the word we're looking for
                search_string = "".join(area.non_empty_letters)
            else:
                # the only letter that's in fixed and the word
                # search_string = set(area.fixed_letters).intersection(set(word))
                search_string = area.non_empty_letters[0]
            # print("search_string:", search_string)

            first_fixed_position = area.non_empty_positions[0]
            offsets = list(Logic.find_substring(search_string, word))

            if offsets == [-1]:
                return []
            else:
                for offset in offsets:
                    modified_position = \
                        Logic.modify_position_by_axis(first_fixed_position,
                                                      -offset,
                                                      area.axis)
                    if modified_position is not None:
                        raw_starting_positions.append(modified_position)

        # maybe this needs to be moved out of the if/else
        for position in raw_starting_positions:
            suggest = Datatypes.Suggestion(word, position, area.axis)
            if Checks.is_word_placeable(suggest) is True:
                checked_starting_positions.append(position)

        cleansed_starting_positions = list(set(checked_starting_positions))
        return cleansed_starting_positions

    @staticmethod
    def create_words(area: Datatypes.Area) -> list:
        # print("create_words:")
        # print("max:", area.max_length)
        # print("min:", area.min_length)
        # TODO: this currently works "blind", it doesn't care whether
        # there's occupied positions in the area or not.
        # make it consider already placed letters and use word_list_by_word.

        # attempts to create words for the given position-range
        # from the dictionary with the letters on the rack
        # given position range can be arbitrary (2 to length of the board)
        # filled positions in the position range can have gaps between them
        vowels = [l for l in area.unique_letters if l in "AEIOU"]
        consonants = [l for l in area.unique_letters if l not in "AEIOU"]

        if len(vowels) <= len(consonants):
            short_list = vowels
            long_list = consonants
        else:
            short_list = consonants
            long_list = vowels

        if len(short_list) == 0:
            short_list = long_list.pop(0)

        words_to_check = []
        available_lengths = range(area.max_length,
                                  area.min_length - 1,
                                  -1)
        for length in available_lengths:
            for short_letter in short_list:
                for long_letter in long_list:
                    word_list = WordSearch.word_list_by_letters(length,
                                                                short_letter,
                                                                long_letter)
                    words_to_check.extend(word_list)
                # end of for short_list
            # end of for long_list
        # end of for available_lengths

        unique_words_to_check = list(set(words_to_check))

        all_letters = area.available_letters
        buildable_words = [word for word
                           in unique_words_to_check
                           if Checks.is_word_buildable(word,
                                                       all_letters,
                                                       area.max_length) is True]

        return buildable_words

    @staticmethod
    def word_list_by_letters(length: int,
                             first_letter: str,
                             second_letter: str = "") -> list:
        # print("word_list_by_letters")
        # print("length:", length)
        # print("first_letter:", first_letter)
        # print("second_letter:", second_letter)
        # TODO: by god make it less dirty
        if "?" in first_letter or "?" in second_letter:
            return []

        first_set = set(Settings.GAME_SETTINGS['words'][length][first_letter])
        if second_letter == "":
            return list(first_set)

        second_set = set(Settings.GAME_SETTINGS['words'][length][second_letter])
        combined_set = first_set.intersection(second_set)
        return list(combined_set)


    @staticmethod
    def word_list_by_word(word: str,
                          max_length: int = None) -> list:
        # make a set of the letters of the word
        # iterate from the maximum length the word can have
        # (length of the existing word + letters on the rack)
        # to the minimum (length of existing word + 1)
        # find the wordlists of that length with all existing letters from
        # the set
        # search the wordlist with a regex
        # return the words

        if max_length is None:
            f_max_length = Settings.GAME_SETTINGS['size_x']
        else:
            f_max_length = max_length

        if f_max_length < len(word):
            print(f"max_length is {f_max_length}, which is smaller than length of {len(word)}.")
            return []

        letter_set = list(set(word))
        first_letter = letter_set[0]
        remaining_letters = letter_set[1::]

        words_to_check = []

        for current_length in range(f_max_length, len(word), -1):
            updater_set = set(Settings.GAME_SETTINGS['words']
                              [current_length]
                              [first_letter])
            for remaining_letter in remaining_letters:
                intersection_set = set(Settings.GAME_SETTINGS['words']
                                       [current_length]
                                       [remaining_letter])
                updater_set.intersection_update(intersection_set)
            words_to_check.extend(list(updater_set))

        unique_words = list(set(words_to_check))
        result_list = [list_gen_word for list_gen_word
                       in unique_words
                       if word in list_gen_word]

        return result_list

    @staticmethod
    def word_list_by_regex(raw_position_string: str, max_length):
        raise NotImplementedError("TODO")


class Dictionary:
    @staticmethod
    def load_shelve(language: str):
        shelve_path = path.join(Settings.app_path, language)
        with shelve.open(shelve_path) as db:
            try:
                db[language]
            except KeyError:
                print("creating dictionary-file for language:", language)
                db[language] = Dictionary.create_dictionary(language)
            finally:
                print("loading dictionary-file for language:", language)
                shelve_content = db[language]
        return shelve_content

    @staticmethod
    def read_words_from_text_file(file_path: path) -> str:
        text_file = open(file_path, mode="r")
        words_in_file = "".join(text_file.read().upper())
        return words_in_file

    @staticmethod
    def filter_word_list(word_list,
                         letter: str,
                         length: int) -> list:
        length_rex = ''.join([r"(^\w{", str(length), "}$)"])
        letter_rex = ''.join([r"\w*", letter, r"\w*"])
        filter_length = re.compile(length_rex, re.MULTILINE)
        filter_letter = re.compile(letter_rex, re.MULTILINE)

        word_list_by_length = filter_length.findall(word_list)
        specific_word_list = []
        for word in word_list_by_length:
            if filter_letter.match(word) is not None:
                specific_word_list.append(word)
        return specific_word_list

    @staticmethod
    def create_dictionary(language, file_path: path = None):
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZÄÜÖ"
        words_dict = {}

        # load dictioary-textfile
        if file_path is None:
            word_file = Settings.dictionaries[language]
        else:
            word_file = file_path

        full_wordlist = Dictionary.read_words_from_text_file(word_file)

        # shortest words are 2 letters, longest 20 (due to the board)
        for wordLength in range(2, 20 + 1):
            words_dict[int(wordLength)] = {}
            for letter in alphabet:
                filtered_word_list = Dictionary.filter_word_list(full_wordlist,
                                                                 letter,
                                                                 wordLength)
                words_dict[int(wordLength)][letter] = filtered_word_list
        return words_dict


class Display:
    # TODO: rework this mess
    @staticmethod
    def print_board(temporary: bool = False):
        rack = Settings.get_rack()
        # global gameTurn
        # basics table to display the board
        # one square:
        #      A
        #    +---+
        #  1   Q
        #    +---+
        print("\t A \t B \t C \t D \t E \t F \t G \t H \t I \t J \t K \t L \t M \t N \t O\n")
        # print("  1\t 2 \t 3 \t 4 \t 5 \t 6 \t 7 \t 8 \t 9 \t 10\t 11\t 12\t 13\t 14\t 15 \n")
        for row in range(Settings.GAME_SETTINGS['size_y']):
            print("\t", end="")
            print("+---" * 15)
            print(str(row + 1) + "  ", end="")
            for column in range(Settings.GAME_SETTINGS['size_x']):
                # print(" " + get_letter_from_position(y = row, x = column) + "\t", end = "")
                current_position = Logic.convert_coordinate_to_position(x=column,
                                                                        y=row)
                print(" " + Logic.get_letter_from_position(current_position, show_joker=True,
                                                           is_temporary=temporary) + "\t", end="")
            print("  " + str(row + 1))
            # print("   " + chr(row+65))
        print("\t", end="")
        print("+---" * 15)
        print("\n")
        print("\t A \t B \t C \t D \t E \t F \t G \t H \t I \t J \t K \t L \t M \t N \t O \n")

        # # display current score:
        # print("Score:\t", gameScore)
        # print("Turn #:\t", gameTurn)
        # print("Letters in Bag:\t", len(letterBag))
        # print("\n")

        # display the letters on the rack
        print("Rack:\t", end="")
        for letter in rack:
            print(letter, end="  ")
        # display the score of each letter on the rack
        print("\n")
        print("\t\t", end="")
        for letter in rack:
            print(Settings.GAME_SETTINGS['letter_score'].get(letter), end="  ")
        print("\n")

    @staticmethod
    def printLog():
        pass
