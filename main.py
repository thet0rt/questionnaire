from game_engine import *
from pprint import pprint

CHEAT = False


def main():
    say_welcome_prompts()
    count = get_count()
    question_list = get_question(count)
    if not question_list:
        return print('The game is over due to api error. Please contact with the developer in tg: @thet0rt')
    if CHEAT:
        pprint(question_list)
    ask_questions(question_list)
    print_the_final_score()


if __name__ == '__main__':
    main()
