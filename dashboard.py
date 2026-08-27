import tkinter as tk


def create_dashboard(total_reps, best_score, rom, exercise):

    window = tk.Tk()

    window.title("FormFit - Performance Dashboard")
    window.geometry("1000x500")
    window.resizable(False, False)
    window.configure(bg="#F4F1EA")

    # =====================================================
    # HEADER
    # =====================================================

    title = tk.Label(
        window,
        text="FORMFIT",
        font=("Arial", 28, "bold"),
        bg="#F4F1EA",
        fg="#243447"
    )
    title.pack(pady=(25, 5))

    subtitle = tk.Label(
        window,
        text="PERFORMANCE DASHBOARD",
        font=("Arial", 14, "bold"),
        bg="#F4F1EA",
        fg="#52616B"
    )
    subtitle.pack(pady=(0, 20))

    # =====================================================
    # EXERCISE
    # =====================================================

    exercise_label = tk.Label(
        window,
        text=f"Exercise: {exercise}",
        font=("Arial", 16, "bold"),
        bg="#F4F1EA",
        fg="#243447"
    )
    exercise_label.pack(pady=5)

    # =====================================================
    # STATISTICS
    # =====================================================

    stats_frame = tk.Frame(
        window,
        bg="#F4F1EA"
    )
    stats_frame.pack(pady=25)

    # Total Reps
    reps_frame = tk.Frame(
        stats_frame,
        bg="#FFFFFF",
        bd=1,
        relief="solid"
    )
    reps_frame.grid(
        row=0,
        column=0,
        padx=12,
        ipadx=20,
        ipady=18
    )

    tk.Label(
        reps_frame,
        text="TOTAL REPS",
        font=("Arial", 11, "bold"),
        bg="#FFFFFF",
        fg="#52616B"
    ).pack(pady=(15, 5))

    tk.Label(
        reps_frame,
        text=str(total_reps),
        font=("Arial", 26, "bold"),
        bg="#FFFFFF",
        fg="#243447"
    ).pack(pady=(0, 15))

    # Best Score
    score_frame = tk.Frame(
        stats_frame,
        bg="#FFFFFF",
        bd=1,
        relief="solid"
    )
    score_frame.grid(
        row=0,
        column=1,
        padx=12,
        ipadx=20,
        ipady=18
    )

    tk.Label(
        score_frame,
        text="BEST FORM SCORE",
        font=("Arial", 11, "bold"),
        bg="#FFFFFF",
        fg="#52616B"
    ).pack(pady=(15, 5))

    tk.Label(
        score_frame,
        text=f"{best_score}%",
        font=("Arial", 26, "bold"),
        bg="#FFFFFF",
        fg="#243447"
    ).pack(pady=(0, 15))

    # Range of Motion
    rom_frame = tk.Frame(
        stats_frame,
        bg="#FFFFFF",
        bd=1,
        relief="solid"
    )
    rom_frame.grid(
        row=0,
        column=2,
        padx=12,
        ipadx=20,
        ipady=18
    )

    tk.Label(
        rom_frame,
        text="RANGE OF MOTION",
        font=("Arial", 11, "bold"),
        bg="#FFFFFF",
        fg="#52616B"
    ).pack(pady=(15, 5))

    tk.Label(
        rom_frame,
        text=f"{rom:.1f}°",
        font=("Arial", 26, "bold"),
        bg="#FFFFFF",
        fg="#243447"
    ).pack(pady=(0, 15))

    # =====================================================
    # MESSAGE
    # =====================================================

    message = tk.Label(
        window,
        text="Great work! Keep improving your form.",
        font=("Arial", 14),
        bg="#F4F1EA",
        fg="#243447"
    )
    message.pack(pady=(5, 20))

    # =====================================================
    # CLOSE BUTTON
    # =====================================================

    close_button = tk.Button(
        window,
        text="Close Dashboard",
        font=("Arial", 11, "bold"),
        bg="#243447",
        fg="white",
        activebackground="#52616B",
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        command=window.destroy,
        padx=25,
        pady=10
    )
    close_button.pack()

    window.mainloop()


# =========================================================
# TEST MODE
# =========================================================

if __name__ == "__main__":

    create_dashboard(
        total_reps=5,
        best_score=90,
        rom=110,
        exercise="Bicep Curl"
    )