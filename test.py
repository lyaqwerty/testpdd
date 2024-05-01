import json
import random
import tkinter as tk
from tkinter import messagebox, PhotoImage
import customtkinter as ctk
from customtkinter import CTkFont


class DrivingTestApp:
    MAX_QUESTIONS = 20

    def __init__(self, master):
        self.image_object = None
        self.master = master
        self.master.title("Тест ПДД")
        self.master.geometry("1000x1000")

        self.custom_font = CTkFont(family="Helvetica", size=14)

        self.questions = []
        self.load_questions()
        random.shuffle(self.questions)

        self.current_question = 0
        self.score = 0
        self.timer_seconds = 1200

        self.timer_label = ctk.CTkLabel(self.master, text="", font=self.custom_font)
        self.timer_label.pack()

        self.question_label = ctk.CTkLabel(
            self.master, text="", font=self.custom_font, wraplength=480
        )
        self.question_label.pack(pady=10)

        self.image_label = tk.Label(self.master)
        self.image_label.pack(pady=10)

        self.option_buttons = []
        for i in range(3):
            button = ctk.CTkButton(
                self.master, text="", font=self.custom_font, command=lambda idx=i: self.check_answer(idx),
            )
            button.pack(fill=tk.X, padx=10, pady=5)
            self.option_buttons.append(button)

        self.next_button = ctk.CTkButton(
            self.master, text="Следующий", font=self.custom_font, command=self.next_question
        )
        self.next_button.pack(pady=10)

        self.display_question()
        self.start_timer()

    def load_questions(self):
        with open("questions.json", "r", encoding="utf-8") as file:
            all_questions = json.load(file)
            self.questions = all_questions[:self.MAX_QUESTIONS]

    def display_question(self):
        if self.current_question < len(self.questions):
            question_info = self.questions[self.current_question]
            self.question_label.configure(text=question_info["question"])

            image_path = question_info.get("image_path", "")
            if image_path:
                try:
                    image = PhotoImage(file=image_path)
                    self.image_label.configure(image=image)
                    self.image_object = image
                except Exception as e:
                    messagebox.showerror("Ошибка загрузки изображения", str(e))
                    self.image_label.configure(image='')
            else:
                self.image_label.configure(image='')

            options = question_info["options"]
            for i in range(3):
                self.option_buttons[i].configure(text=options[i])

    def check_answer(self, selected_index):
        correct_answer_index = self.questions[self.current_question]["answer"]
        if selected_index == correct_answer_index:
            self.score += 1
            messagebox.showinfo("Верно!", "Ответ правильный!")
        else:
            messagebox.showerror("Неверно.", "Ответ неправильный.")
        self.next_question()

    def next_question(self):
        self.current_question += 1

        if self.current_question >= len(self.questions):
            if self.score == 18:
                self.add_additional_questions(10)
            elif self.score == 19:
                self.add_additional_questions(5)
            else:
                messagebox.showinfo("Тест окончен", f"Результат: {self.score}/{len(self.questions)}")
                self.master.destroy()
        else:
            self.display_question()

    def add_additional_questions(self, count):
        with open("questions.json", "r", encoding="utf-8") as file:
            all_questions = json.load(file)
            random.shuffle(all_questions)

            additional_questions = [q for q in all_questions if q not in self.questions]
            self.questions += additional_questions[:count]

    def start_timer(self):
        if self.timer_seconds > 0:
            self.timer_label.configure(
                text=f"Времени осталось: {self.timer_seconds} секунд"
            )
            self.timer_seconds -= 1
            self.master.after(1000, self.start_timer)
        else:
            messagebox.showinfo(
                "Время вышло!", "Время на прохождение теста закончилось."
            )
            self.master.destroy()


def main():
    root = ctk.CTk()
    app = DrivingTestApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
