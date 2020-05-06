import timeit

from logic_new import Settings
from logic_new import WordSearch


def wrapper(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)

    return wrapped


# def the_vetter(testing_tuples: list):
#     for word_tuple in testing_tuples:
#         word = word_tuple[0]
#         pos_list = word_tuple[-1]
#         word_length = len(word)
#         for position in pos_list:
#             end_position = Logic.modify_position_by_axis(position, word_length - 1, "X")
#             Logic.set_word_to_position(word, position, axis="X", is_temporary=True)
#             temp_word = Logic.get_word_from_position(position, end_position, is_temporary=True)
#             if temp_word == word:
#                 print(f"Word *{word}* on position {position} passed.")
#             else:
#                 print(f"[!] FAILED: Word *{word}* on position {position} is wrong. Found: {temp_word}")
#             Logic.remove_temporary_positions(word_length)


def word_exists_by_letter(word: str):
    first_letter = word[0]
    second_letter = word[1]
    length = len(word)
    word_list = WordSearch.word_list_by_letters(length, first_letter, second_letter)
    # print(word_list)
    if word in word_list:
        return True
    return False


def word_exists_by_entire_word(word: str):
    word_list = WordSearch.word_list_by_word(word, len(word))
    # print(word_list)
    if word in word_list:
        return True
    return False

LANGUAGE = "german"
# lang = "english"
GAMEMODE = "normal"

# dirty solution.
gameSettings = Settings.get_game_settings(GAMEMODE, LANGUAGE)
Settings.set_game_settings(settings=gameSettings)

Settings.set_rack("ERNSTLUD")

number_of_tests = 10

test_word = "FLÜSTERN"
# print("NEW".center(40, "*"))
# print("OLD".center(40, "*"))
# pprint.pprint(starting_positions_old)

# ## TESTING AREA
# TEST A
test_a_avg = 0
test_a_total = 0
test_a_function = wrapper(word_exists_by_letter, test_word)
# # TEST B
test_b_avg = 0
test_b_total = 0
test_b_function = wrapper(word_exists_by_entire_word, test_word)
#
# TEST C
test_c_avg = 0
test_c_total = 0
test_c_function = "pass"

for i in range(0, number_of_tests + 1):
    print("Running test #", i)
    # https://www.pythoncentral.io/time-a-python-function/
    # TEST A: find words 10 times, average time
    current_a = timeit.timeit(test_a_function, number=1)
    test_a_total += current_a

    # TEST B: find words new, average time
    current_b = timeit.timeit(test_b_function, number=1)
    test_b_total += current_b

    # # TEST C: pass-timing
    current_c = timeit.timeit(test_c_function, number=1)
    test_c_total += current_c

test_a_avg = test_a_total / number_of_tests
test_b_avg = test_b_total / number_of_tests
test_c_avg = test_c_total / number_of_tests

print("average for test A:", test_a_avg)
print("average for test B:", test_b_avg)
print("average for test C:", test_c_avg)

if test_a_avg > test_b_avg:
    print("Test B was faster.")
else:
    print("Test A was faster.")



print("result for test A:", word_exists_by_letter("FLÜSTERN"))
print("result for test B:", word_exists_by_entire_word("FLÜSTERN"))