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