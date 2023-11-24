from akinator import Akinator, Answer, InvalidAnswer, Theme
import keyboard
import pyttsx3

def say(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def get_key_input():
    while True:
        event = keyboard.read_event(suppress=True)
        if event.event_type == keyboard.KEY_DOWN:
            return event.name

def test() -> None:
    while True:
        # create akinator instance
        aki = Akinator(
            child_mode=True,
            theme=Theme.from_str('characters'),
        )

        while True:
            # start the game, and get the first question
            first_question = aki.start_game()
            print(f'{first_question}: ', end='', flush=True)
            say(first_question)
            # receive console input for the first question
            answer = get_key_input()

            # keep asking and receiving answers while akinator's progression is <= 80
            while aki.progression <= 80:
                if answer == '5':
                    # start the game from the beginning
                    break
                elif answer.isdigit():
                    # restart the game
                    break

                if answer == 'l' or answer == 'i' or answer == 'o' or answer == 'k' or answer == ',' or answer == ';':
                    # repeat the question
                    print(f'{aki.question}: ', end='', flush=True)
                    say(aki.question)
                else:
                    try:
                        # map key presses to answer enum variants
                        key_mapping = {'a': 'Yes', 'f': 'No', 'h': 'c',
                                       'q': 'Yes', 'w': 'Yes', 's': 'Yes', 'z': 'Yes', 'x': 'Yes',
                                       'e': 'No', 'r': 'No', 'd': 'No', 'f': 'No', 'c': 'No', 'v': 'No',
                                       't': 'idk', 'y': 'idk', 'u': 'idk',
                                       'g': 'idk', 'h': 'idk', 'j': 'idk',
                                       'b': 'idk', 'n': 'idk', 'm': 'idk'}
                        answer_str = key_mapping.get(answer)
                        if answer_str is None:
                            raise InvalidAnswer
                        answer = Answer.from_str(answer_str)
                    except InvalidAnswer:
                        print('Invalid answer')
                    else:
                        # answer the current question
                        aki.answer(answer)
                        print(f'{aki.question}: ', end='', flush=True)
                        say(aki.question)

                # receive console input for the next question
                answer = get_key_input()

            if answer == '5' or answer.isdigit():
                break

            # tell akinator to end the game and make its guess
            first_guess = aki.win()

            if first_guess:
                # print out its first guess's details
                print('name:', first_guess.name)
                say(first_guess.name)
                print('desc:', first_guess.description)
                say(first_guess.description)
                print('image:', first_guess.absolute_picture_path)

if __name__ == '__main__':
    test()

