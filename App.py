import json
import tkinter as tk
from tkinter import messagebox 
with open("questions.json") as f:
    quiz_data = json.load(f)

root = tk.Tk()
root.title("Quiz")
root.geometry("400x350")

question_list = []
user_answers = []
current_question = 0
selected_answer = tk.IntVar(value=-1) 

main_frame = tk.Frame(root)
main_frame.pack(pady=20)


def clear_frame():
    for item in main_frame.winfo_children():
        item.destroy()


def show_topics():
    clear_frame()
    tk.Label(main_frame, text="Choose a topic", font=("Arial", 16)).pack(pady=10)
    for topic_name in quiz_data:
        btn = tk.Button(main_frame, text=topic_name, width=20,
                         command=lambda t=topic_name: start_quiz(t))
        btn.pack(pady=5)


def start_quiz(topic_name):
    global question_list, user_answers, current_question
    question_list = quiz_data[topic_name]
    user_answers = [None] * len(question_list)
    current_question = 0
    show_question() 


def show_question():
    global option_buttons
    clear_frame()
    question = question_list[current_question]
    user_choice = user_answers[current_question]

    if user_choice is not None:
        selected_answer.set(user_choice)
    else:
        selected_answer.set(-1)

    total_questions = len(question_list)
    tk.Label(main_frame, text="Question " + str(current_question + 1) + "/" + str(total_questions)).pack()
    tk.Label(main_frame, text=question["question"], font=("Arial", 13), wraplength=350).pack(pady=10)

    option_buttons = []
    option_number = 0
    for option_text in question["options"]:
        btn = tk.Radiobutton(main_frame, text=option_text, variable=selected_answer, value=option_number)
        btn.pack(anchor="w")
        option_buttons.append(btn)
        option_number = option_number + 1

    feedback_label = tk.Label(main_frame, text="", font=("Arial", 11))
    feedback_label.pack(pady=5)

    button_area = tk.Frame(main_frame)
    button_area.pack(pady=10)

    if current_question == 0:
        prev_button_state = "disabled"
    else:
        prev_button_state = "normal"

    tk.Button(button_area, text="Previous", state=prev_button_state, command=go_to_previous).pack(side="left", padx=5)

    if user_choice is None:
        tk.Button(button_area, text="Check", command=check_answer).pack(side="left", padx=5)
    else:
        for btn in option_buttons:
            btn.config(state="disabled")

        correct_answer = question["answer"]
        if user_choice == correct_answer:
            feedback_label.config(text="Correct!", fg="green")
        else:
            correct_text = question["options"][correct_answer]
            feedback_label.config(text="Wrong! Correct answer: " + correct_text, fg="red")

        if current_question == total_questions - 1:
            next_button_text = "Finish"
        else:
            next_button_text = "Next"

        tk.Button(button_area, text=next_button_text, command=go_to_next).pack(side="left", padx=5)


def check_answer():
    if selected_answer.get() == -1:
        messagebox.showwarning("Wait", "Please select an answer.")
        return
    user_answers[current_question] = selected_answer.get()
    show_question()


def go_to_next():
    global current_question
    current_question = current_question + 1
    if current_question < len(question_list):
        show_question()
    else:
        show_result()


def go_to_previous():
    global current_question
    current_question = current_question - 1
    show_question()


def show_result():
    clear_frame()

    correct_count = 0
    for i in range(len(question_list)):
        if user_answers[i] == question_list[i]["answer"]:
            correct_count = correct_count + 1

    wrong_count = len(question_list) - correct_count

    tk.Label(main_frame, text="Quiz finished!", font=("Arial", 16)).pack(pady=10)
    tk.Label(main_frame, text="Correct: " + str(correct_count)).pack()
    tk.Label(main_frame, text="Wrong: " + str(wrong_count)).pack()

    tk.Button(main_frame, text="Back to topics", command=show_topics).pack(pady=15)


show_topics()
root.mainloop() 