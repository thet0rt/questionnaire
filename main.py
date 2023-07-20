# This is a sample Python script.
import re
from pprint import pprint
from thefuzz import fuzz
import requests
SCORE = 0
from re import search

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


class CountError(Exception):
    pass


def add_points():
    global SCORE
    SCORE += 1
    print(f'You earned 1 point. Current score: {SCORE}')


def get_count() -> int:
    while True:
        count = input('Please enter the number of questions from 1 to 100: ')
        if not count.isdigit():
            print('Try again. You should enter the number')
            continue
        if int(count) not in range(1, 101):
            print('Try again. The number must be from 1 to 100')
            continue
        return int(count)


def get_question(question_number: int) -> list:
    try:
        response = requests.get(f'http://jservice.io/api/random?count={question_number}')
        if not response.status_code == 200:
            print('error')  # todo сделать логи
        raw_question_list = response.json()
        question_list = [dict(question=q.get('question'), answer=q.get('answer')) for q in raw_question_list]
        return question_list
    except Exception as e:
        pass  # todo сделать логи


def check_answer(user_answer: str, correct_answer: str) -> bool:
    if user_answer == correct_answer:
        return True
    if '<i>' in correct_answer:
        correct_answer = correct_answer[3:-4]
    correct_answers = correct_answer.split(' ')
    for answer in correct_answers:
        if answer in ['a', 'an', 'the']:
            continue
        result = search(answer, user_answer)
        if result:
            return True
    return False


def ask_questions(question_list: list) -> None:
    for question in question_list:
        print(question.get('question'))
        try:
            correct_answer = question.get('answer').lower()
        except AttributeError:
            pass # todo logs
        for i in range(2):
            user_answer = input('Please enter your answer: ').lower()
            if check_answer(user_answer, correct_answer):
                print('Correct !')
                add_points()
                break
            if i == 1:
                print(f'Wrong answer. The correct answer was "{correct_answer}"')
            else:
                print('Wrong answer. Try again')



def main():
    count = get_count()
    question_list = get_question(count)
    pprint(question_list)
    ask_questions(question_list)
    print(f'Game over. The final score: {SCORE} points')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # main()
    correct_answer = 'Abraham Linkoln'
    user_answer = 'Linkoln Abraham'
    print(fuzz.token_sort_ratio(correct_answer, user_answer))
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
