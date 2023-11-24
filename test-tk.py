from akinator import Akinator, Answer, Theme, InvalidAnswer
import tkinter as tk
from tkinter import Label
import keyboard


class AkinatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Akinator")
        self.question_label = Label(root, text="", wraplength=400, justify="left", font=("Helvetica", 12))
        self.question_label.pack(padx=20, pady=20)
        self.aki = Akinator(child_mode=True, theme=Theme.from_str('characters'))

    def get_key_input(self):
        while True:
            event = keyboard.read_event(suppress=True)
            if event.event_type == keyboard.KEY_DOWN:
                return event.name

    def display_question(self, question):
        self.question_label.config(text=question)

    def run_game(self):
        while True:
            first_question = self.aki.start_game()
            self.display_question(first_question)

            answer = self.get_key_input()

            while self.aki.progression <= 80:
                if answer.isdigit():
                    break
                elif answer == '5':
                    break

                try:
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
                    self.aki.answer(answer)
                    self.display_question(self.aki.question)

                answer = self.get_key_input()

            if answer == '5' or answer.isdigit():
                break

            first_guess = self.aki.win()

            if first_guess:
                print('name:', first_guess.name)
                print('desc:', first_guess.description)
                print('image:', first_guess.absolute_picture_path)

if __name__ == '__main__':
    root = tk.Tk()
    akinator_gui = AkinatorGUI(root)
    akinator_gui.run_game()
    root.mainloop()
