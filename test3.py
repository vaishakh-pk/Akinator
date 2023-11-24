from akinator import Akinator, Answer, CantGoBackAnyFurther, InvalidAnswer, Theme
from gtts import gTTS
import os
import speech_recognition as sr
import simpleaudio as sa
from pydub import AudioSegment

def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    tts.save('output.mp3')

    # Convert MP3 to WAV
    sound = AudioSegment.from_mp3('output.mp3')
    sound.export('output.wav', format='wav')

    wave_obj = sa.WaveObject.from_wave_file('output.wav')
    play_obj = wave_obj.play()
    play_obj.wait_done()

# ... (the rest



def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something:")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio).lower()
    except sr.UnknownValueError:
        print("Could not understand audio.")
        return ""
    except sr.RequestError as e:
        print(f"Error with the speech recognition service: {e}")
        return ""

def akinator_game():
    aki = Akinator(child_mode=True, theme=Theme.from_str('characters'))

    first_question = aki.start_game()
    text_to_speech(first_question)

    answer = recognize_speech()
    print('Your answer:', answer)

    while aki.progression <= 80:
        if answer.lower() == 'back':
            try:
                aki.back()
                print('Went back 1 question')
            except CantGoBackAnyFurther:
                print('Cannot go back any further!')
        else:
            try:
                answer = Answer.from_str(answer)
            except InvalidAnswer:
                print('Invalid answer')
            else:
                aki.answer(answer)

        next_question = aki.question
        text_to_speech(next_question)
        answer = recognize_speech()
        print('Your answer:', answer)

    first_guess = aki.win()

    if first_guess:
        print('Akinator\'s guess:')
        print('Name:', first_guess.name)
        print('Description:', first_guess.description)
        print('Image:', first_guess.absolute_picture_path)
        text_to_speech(f"My guess is {first_guess.name}. {first_guess.description}")

if __name__ == '__main__':
    akinator_game()
