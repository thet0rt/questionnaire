from logger import log
from thefuzz import fuzz
import requests
import random
SCORE = 0

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def get_correct_phrase():
    correct_phrases = ['Correct!', 'True. Nice one!', 'Exactly!', 'Well done!', "Correct answer. You are awesome!"]
    return random.choice(correct_phrases)


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
    url = f'http://jservice.io/api/random?count={question_number}'
    try:
        response = requests.get(url)
        if not response.status_code == 200:
            log.error(f'Error while sending request. Url: {url}, status_code = {response.status_code},'
                      f'test = {response.text}')
        raw_question_list = response.json()
        question_list = [dict(question=q.get('question'), answer=q.get('answer')) for q in raw_question_list]
        return question_list
    except Exception as e:
        log.error(f'Error while sending request. url: {url}, exception {e}')


def check_answer(user_answer: str, correct_answer: str) -> bool:
    similarity_score = fuzz.token_sort_ratio(correct_answer, user_answer)
    if similarity_score > 50:
        return True
    return False


def ask_questions(question_list: list) -> None:
    for question in question_list:
        print(question.get('question'))
        try:
            correct_answer = question.get('answer').lower()
            if '<i>' in correct_answer:
                correct_answer = correct_answer[3:-4]
        except AttributeError:
            log.error(f"Error while getting answer for question. {question.get('answer')} didn't happen to be string")
            continue
        for i in range(2):
            user_answer = input('Please enter your answer: ').lower()
            if check_answer(user_answer, correct_answer):
                print(get_correct_phrase())
                add_points()
                break
            if i == 1:
                print(f'Wrong answer. The correct answer was "{correct_answer}"')
            else:
                print('Wrong answer. Try again')
    print(f'Game over. The final score: {SCORE} points')


class CountError(Exception):
    pass
