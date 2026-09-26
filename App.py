import json
import tkinter as tk
from tkinter import messagebox 
with open("questions.json") as f:
    quiz_data = json.load(f)

root = tk.Tk() 
root.title("Quiz")
root.geometry("500x450")
root.configure(bg = "lightgreen")
question_list = []
user_answers = []
current_question = 0
selected_answer = tk.IntVar(value=-1) 

main_frame = tk.Frame(root)
main_frame.pack(pady=20)
main_frame.configure(bg="lightgreen")


def clear_frame():
    for item in main_frame.winfo_children():
        item.destroy()


def make_hover_button(parent, **options):
    button = tk.Button(parent, **options)
    normal_color = button.cget("bg")
    button.bind("<Enter>", lambda event: button.config(bg="#00C2A8"))
    button.bind("<Leave>", lambda event: button.config(bg=normal_color))
    return button


def show_topics(): 
    clear_frame()
    tk.Label(main_frame, text="Choose a topic", font=("Arial", 16), foreground=("red"),background=("lightgreen"),borderwidth=2,highlightbackground="green",highlightthickness=2).pack(pady=10)
    for topic_name in quiz_data:
        btn = make_hover_button(main_frame, text=topic_name, width=25,height = 2,bg="#3A86FF", cursor="hand2",
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
    tk.Label(main_frame, text="Question " + str(current_question + 1) + "/" + str(total_questions),background="lightgreen",borderwidth=2,highlightbackground="green",highlightthickness=2).pack(anchor="nw")
    tk.Label(main_frame, text=question["question"], font=("Arial", 17), wraplength=350,background="lightgreen",borderwidth=2,highlightbackground="green",highlightthickness=2).pack(pady=10) 

    option_buttons = []
    option_number = 0
    for option_text in question["options"]:
        btn = tk.Radiobutton(main_frame, text=option_text, variable=selected_answer, value=option_number,
                             background="lightblue", activebackground="lightgreen", selectcolor="#3A86FF",
                             foreground="#2b2b2b", font=("Segoe UI", 12), relief="flat", highlightthickness=0,
                             indicatoron=False, borderwidth=2, cursor="hand2")
        btn.pack(anchor="w", fill="x",pady= 3)
        option_buttons.append(btn) 
        option_number = option_number + 1
    
    feedback_label = tk.Label(main_frame, text="", font=("Arial", 11),background="lightgreen")
    feedback_label.pack(pady=5) 

    button_area = tk.Frame(main_frame)
    button_area.configure(bg="lightgreen")
    button_area.pack(pady=10)

    if current_question == 0:
        prev_button_state = "disabled"
    else:
        prev_button_state = "normal"

    make_hover_button(button_area, text="Previous",foreground="black" ,font=("Arial ",10,"bold") ,state=prev_button_state,bg="red", command=go_to_previous).pack(side="left", padx=5)
    
    if user_choice is None:
        make_hover_button(button_area, text="Check", bg="#3A86FF",font=("Arial ",10,"bold"), command=check_answer).pack(side="left", padx=5)
        make_hover_button(button_area, text="Skip", bg="red", command=go_to_next).pack(side="left", padx=5)
    else:
        for btn in option_buttons:
            btn.config(state="disabled")

        correct_answer = question["answer"]
        if user_choice == correct_answer:
            feedback_label.config(text="Correct!", fg="darkblue")
        else:
            correct_text = question["options"][correct_answer]
            feedback_label.config(text="Wrong! Correct answer: " + correct_text, fg="red")

        if current_question == total_questions - 1:
            next_button_text = "Finish"
        else:
            next_button_text = "Next"
         
        make_hover_button(button_area, text=next_button_text, command=go_to_next).pack(side="left", padx=5)


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
    global current_question
    clear_frame()

    correct_count = 0
    skipped_count = 0
    for i in range(len(question_list)):
        if user_answers[i] is None:
            skipped_count = skipped_count + 1
        elif user_answers[i] == question_list[i]["answer"]:
            correct_count = correct_count + 1

    wrong_count = len(question_list) - correct_count 

    if skipped_count > 0:
        messagebox.showwarning(
            "Skipped answers",
            "You skipped " + str(skipped_count) + " answer(s). Please answer them."
        )
        current_question = next(
            index for index, answer in enumerate(user_answers) if answer is None
        )
        show_question()
        return

    tk.Label(main_frame, text="Quiz finished!", font=("Arial", 16),bg="lightgreen").pack(pady=10)
    tk.Label(main_frame, text="Correct: " + str(correct_count),bg="lightgreen").pack()
    tk.Label(main_frame, text="Wrong: " + str(wrong_count),bg="lightgreen").pack()
    
    

    make_hover_button(main_frame, text="Back to topics", bg="#3A86FF", command=show_topics).pack(pady=15)


show_topics()
root.mainloop()