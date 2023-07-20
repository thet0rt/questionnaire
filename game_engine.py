from logger import log
from thefuzz import fuzz
import requests
import random
SCORE = 0


def say_welcome_prompts():
    print("Welcome to the Questionnaire game!")
    print("I will be happy to ask you the questions.")
    print("Have fun!")


def get_correct_phrase() -> str:
    correct_phrases = ['Correct!', 'True. Nice one!', 'Exactly! When did you get so smart?',
                       'Well done!', "Correct answer. You are awesome!"]
    return random.choice(correct_phrases)


def get_wrong_phrase() -> str:
    wrong_phrases = ['Wrong answer', 'Wrong. You know nothing, John Snow...', 'Wrong, dummy.', 'Not even close !',
                     'Correct! Nah just kidding. Far from correct to be honest.']
    return random.choice(wrong_phrases)


def add_points() -> None:
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
    if correct_answer.isdigit():
        if not user_answer.isdigit():
            return False
        if int(correct_answer) == int(user_answer):
            return True
        return False
    similarity_score = fuzz.token_sort_ratio(correct_answer, user_answer)
    if similarity_score > 60:
        return True
    return False


def ask_questions(question_list: list) -> None:
    for question in question_list:
        print(f"Question: {question.get('question')}")
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
                print(f'{get_wrong_phrase()} The correct answer was "{correct_answer}"')
            else:
                print(f'{get_wrong_phrase()} Try again')


def print_the_final_score() -> None:
    print('Game over. It was nice to play with you!')
    print(f'The final score: {SCORE} points')
