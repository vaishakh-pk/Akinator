import speech_recognition as sr
import win32com.client
from akinator import (Akinator, Answer, CantGoBackAnyFurther, InvalidAnswer,
                      Theme)
from audio import Audio

def dummy():
    pass

def say(text):
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    speaker.Speak(text)

def takeCommand():
    # r = sr.Recognizer()
    # with sr.Microphone() as source:
    #     r.pause_threshold = 1
    #     audio = r.listen(source)
    #     try:
    #         print("Recognizing..")
    #         query = r.recognize_google(audio, language="en-in")
    #         print(f"User said: {query}")
    #
    #         # Check if the query contains any of the specified keywords
    #         keywords = ["yes", "no", "probably", "probably not", "don't know"]
    #         for keyword in keywords:
    #             if keyword in query.lower():
    #                 return keyword
    #
    #         # If none of the keywords are found, return the entire query
    #         return query
    #     except Exception as e:
    #         return "Sorry! Some error occurred."
    audio = Audio(silent_frames=2)

    audio.set_pre_recording(None)
    audio.set_post_recording(None)
    audio.set_while_silent(None)
    querry = audio.get_transcript()
    return querry

def test() -> None:
    # create akinator instance
    aki = Akinator(
        child_mode=True,
        theme=Theme.from_str('characters'),
    )

    # start the game, and get the first question
    first_question = aki.start_game()
    # recieve console input for first question
    print(first_question)
    say(first_question)
    #answer = input(f'{first_question}: ')
    answer = takeCommand()

    # keep asking and recieving answers while akinator's progression is <=80
    while aki.progression <= 80:
        if answer == 'back':
            # go back a question if response is "back"
            try:
                aki.back()
                print('went back 1 question')
            except CantGoBackAnyFurther:
                print('cannot go back any further!')
        else:
            try:
                # parse to an answer enum variant
                answer = Answer.from_str(answer)
            except InvalidAnswer:
                print('Invalid answer')
                say('Invalid answer')
            else:
                # answer current question
                aki.answer(answer)

        # recieving console input for next question
        print(aki.question)
        say(aki.question)
        #answer = input(f'{aki.question}: ')
        answer = takeCommand()

    # tell akinator to end the game and make its guess
    first_guess = aki.win()

    if first_guess:
        # print out its first guess's details
        print('name:', first_guess.name)
        print('desc:', first_guess.description)
        print('image:', first_guess.absolute_picture_path)

if __name__ == '__main__':
    test()