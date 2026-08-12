import tkinter as tk


def create_dashboard(total_reps, best_score, rom, exercise):
    window = tk.Tk()
    window.title("FormFit - Performance Dashboard")
    window.geometry("1000x500")
    window.resizable(False, False)
    window.configure(bg="#F4F1EA")
   
    title = tk.Label(
        window,
        text="FORMFIT",
        font=("Arial", 28, "bold"),
        bg="#F4F1EA",
        fg="#243447",
    )
    title.pack(pady=(25, 5))
  
    title.pack(pady=(25, 5))

    subtitle = tk.Label(
        window,
        text="PERFORMANCE DASHBOARD",
        font=("Arial", 14)
    )
    subtitle.pack(pady=(0, 25))

    exercise_label = tk.Label(
        window,
        text=f"Exercise: {exercise}",
        font=("Arial", 16, "bold")
    )
    exercise_label.pack(pady=10)

    stats_frame = tk.Frame(window, bg="#F4F1EA")
    stats_frame.pack(pady=25)

    reps_label = tk.Label(
        stats_frame,
        text=f"Total Reps\n{total_reps}",
        font=("Arial", 20, "bold"),
        width=15,
        relief="groove",
        padx=20,
        pady=20
    )
    reps_label.grid(row=0, column=0, padx=10)

    score_label = tk.Label(
        stats_frame,
        text=f"Best Score\n{best_score}%",
        font=("Arial", 20, "bold"),
        width=15,
        relief="groove",
        padx=20,
        pady=20
    )
    score_label.grid(row=0, column=1, padx=10)

    rom_label = tk.Label(
        stats_frame,
        text=f"Range of Motion\n{rom:.1f}°",
        font=("Arial", 20, "bold"),
        width=15,
        relief="groove",
        padx=20,
        pady=20
    )
    rom_label.grid(row=0, column=2, padx=10)

    message = tk.Label(
        window,
        text="Great work! Keep improving your form.",
        font=("Arial", 14)
    )
    message.pack(pady=30)

    close_button = tk.Button(
        window,
        text="Close Dashboard",
        font=("Arial", 12),
        command=window.destroy,
        padx=20,
        pady=8
    )
    close_button.pack()

    window.mainloop()

if __name__ == "__main__":
    create_dashboard(
        total_reps=5,
        best_score=90,
        rom=110,
        exercise="Bicep Curl"
    )