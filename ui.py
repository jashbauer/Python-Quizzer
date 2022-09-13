from tkinter import *
from question_model import Question
from data import question_data
from quiz_brain import QuizBrain


question_bank = []
for question in question_data:
    question_text = question["question"]
    question_answer = question["correct_answer"]
    new_question = Question(question_text, question_answer)
    question_bank.append(new_question)


quiz = QuizBrain(question_bank)


THEME_COLOR = "#375362"
QUEST_FONT = ("arial", 16, "italic")


class QuizzInterface:

    def __init__(self):
        self.window = Tk()
        self.window.title("Quizzler")
        self.window.config(background=THEME_COLOR)

        self.user_answer = None
        self.user_score = 0

        true_image = PhotoImage(file="./images/true.png")
        false_image = PhotoImage(file="./images/false.png")

        self.canvas = Canvas(height=250, width=500)
        self.score = Label(text=f"Score: {self.user_score}", background=THEME_COLOR, fg="white", font=("arial", 20))
        self.score.grid(row=1, column=2, padx=20, pady=20)

        self.canvas.grid(row=2, column=1, columnspan=2, padx=20, pady=20)
        self.question = self.canvas.create_text(250, 125, text="Hello World", font=QUEST_FONT, width=450)

        self.true_button = Button(self.window, image=true_image,
                                  highlightthickness=0, command=self.true_answer)
        self.true_button.grid(row=3, column=1, padx=20, pady=20)
        self.false_button = Button(self.window, image=false_image,
                                   highlightthickness=0, command=self.false_answer)
        self.false_button.grid(row=3, column=2, padx=20, pady=20)

        self.display_next_question()

        self.window.mainloop()

    def end_game(self):
        self.window.destroy()

    def display_next_question(self):
        #TODO: Handle end of question list
        try:
            current_question = quiz.next_question()
            self.canvas.itemconfig(self.question, text=current_question)
        except IndexError:
            if 0 <= self.user_score <= 2:
                final_text = "Maybe you should read a few encyclopedias..."
            elif 2 < self.user_score <= 5:
                final_text = "That's about ok..."
            elif 5 < self.user_score <= 7:
                final_text = "You're better than a coin!"
            else:
                final_text = "Wow, you got quite the random knowledge!"
            self.canvas.itemconfig(self.question, text=final_text)

            self.true_button.config(command=self.end_game)
            self.false_button.config(command=self.end_game)

    def true_answer(self):
        self.user_answer = "true"
        if quiz.check_answer(user_answer=self.user_answer):
            self.user_score += 1
            self.score = Label(text=f"Score: {self.user_score}", background=THEME_COLOR, fg="white", font=("arial", 20))
            self.score.grid(row=1, column=2, padx=20, pady=20)
            self.window.after(ms=100, func=self.positive_feedback)
        else:
            self.window.after(ms=100, func=self.negative_feedback)
        self.window.after(ms=500, func=self.display_next_question)

    def false_answer(self):
        self.user_answer = "false"
        if quiz.check_answer(user_answer=self.user_answer):
            self.user_score += 1
            self.score = Label(text=f"Score: {self.user_score}", background=THEME_COLOR, fg="white", font=("arial", 20))
            self.score.grid(row=1, column=2, padx=20, pady=20)
            self.window.after(ms=100, func=self.positive_feedback)
        else:
            self.window.after(ms=100, func=self.negative_feedback)
        self.window.after(ms=500, func=self.display_next_question)

    def positive_feedback(self):
        self.canvas.config(bg="green")
        self.window.after(ms=300, func=self.restore_background)

    def negative_feedback(self):
        self.canvas.config(bg="red")
        self.window.after(ms=300, func=self.restore_background)

    def restore_background(self):
        self.canvas.config(bg="white")
