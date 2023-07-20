from game_engine import *
from pprint import pprint

CHEAT = True


def main():
    count = get_count()
    question_list = get_question(count)
    if CHEAT:
        pprint(question_list)
    ask_questions(question_list)
    print_the_final_score()


if __name__ == '__main__':
    main()
