import tkinter as tk
from tkinter import ttk
import random
import time

class NumberGuessingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Guessing Game")

        # Initialize game variables
        self.target_number = 0
        self.attempts = 0
        self.history = []
        self.time_left = 30  # Timer is now set to 30 seconds
        self.hint_counter = 0  # Counter for incorrect guesses
        self.timer_running = False  # To track if the timer is running

        # Create Notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=10, padx=10)

        # Game tab
        self.game_tab = tk.Frame(self.notebook)
        self.notebook.add(self.game_tab, text="Game")

        # History tab
        self.history_tab = tk.Frame(self.notebook)
        self.notebook.add(self.history_tab, text="History")

        # Difficulty selection
        self.difficulty_label = tk.Label(self.game_tab, text="Select Difficulty", font=("Helvetica", 12))
        self.difficulty_label.pack(pady=10)

        self.difficulty_var = tk.StringVar(value="Medium")
        self.difficulty_menu = ttk.Combobox(self.game_tab, textvariable=self.difficulty_var, values=["Easy", "Medium", "Hard"], state="readonly", font=("Helvetica", 12))
        self.difficulty_menu.pack(pady=10)

        self.start_button = tk.Button(self.game_tab, text="Start Game", command=self.start_game, font=("Helvetica", 12))
        self.start_button.pack(pady=10)

        # Create GUI components for the game tab
        self.label = tk.Label(self.game_tab, text="I am thinking of a number...", font=("Helvetica", 14))
        self.label.pack(pady=20)

        self.instruction_label = tk.Label(self.game_tab, text="Enter your guess:", font=("Helvetica", 12))
        self.instruction_label.pack()

        self.entry = tk.Entry(self.game_tab, font=("Helvetica", 12))
        self.entry.pack(pady=10)

        self.submit_button = tk.Button(self.game_tab, text="Submit Guess", command=self.check_guess, font=("Helvetica", 12), state=tk.DISABLED)
        self.submit_button.pack(pady=10)

        self.result_label = tk.Label(self.game_tab, text="", font=("Helvetica", 12))
        self.result_label.pack(pady=10)

        self.attempts_label = tk.Label(self.game_tab, text="Attempts: 0", font=("Helvetica", 12))
        self.attempts_label.pack(pady=5)

        self.play_again_button = tk.Button(self.game_tab, text="Play Again", command=self.reset_game, font=("Helvetica", 12), state=tk.DISABLED)
        self.play_again_button.pack(pady=10)

        # Timer Label
        self.timer_label = tk.Label(self.game_tab, text=f"Time Left: {self.time_left}s", font=("Helvetica", 14))
        self.timer_label.pack(pady=10)

        # Create the History Tab components
        self.history_label = tk.Label(self.history_tab, text="History of Guessed Numbers", font=("Helvetica", 14))
        self.history_label.pack(pady=20)

        self.history_listbox = tk.Listbox(self.history_tab, width=50, height=10, font=("Helvetica", 12))
        self.history_listbox.pack(pady=10)

    def start_game(self):
        # Set the target number based on the selected difficulty level
        difficulty = self.difficulty_var.get()

        if difficulty == "Easy":
            self.target_number = random.randint(1, 50)
            self.label.config(text="I am thinking of a number between 1 and 50")
        elif difficulty == "Medium":
            self.target_number = random.randint(1, 100)
            self.label.config(text="I am thinking of a number between 1 and 100")
        else:  # Hard
            self.target_number = random.randint(1, 200)
            self.label.config(text="I am thinking of a number between 1 and 200")

        # Reset the game variables
        self.attempts = 0
        self.hint_counter = 0
        self.time_left = 30  # Reset timer to 30 seconds
        self.timer_label.config(text=f"Time Left: {self.time_left}s")
        self.submit_button.config(state=tk.NORMAL)
        self.start_button.config(state=tk.DISABLED)
        self.result_label.config(text="")
        self.history_label.config(text="History of Guessed Numbers")

        # Start the countdown timer
        self.timer_running = True
        self.start_timer()

    def start_timer(self):
        # Start countdown timer
        if self.timer_running and self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"Time Left: {self.time_left}s")
            self.root.after(1000, self.start_timer)  # Call this function every 1 second
        elif self.time_left == 0:
            self.end_game(f"Time's up! The correct number was {self.target_number}.")

    def check_guess(self):
        try:
            guess = int(self.entry.get())
            self.attempts += 1
            self.hint_counter += 1

            # Check if the guess is correct
            if guess < self.target_number:
                self.result_label.config(text="Too low! Try again.", fg="red")
            elif guess > self.target_number:
                self.result_label.config(text="Too high! Try again.", fg="red")
            else:
                self.result_label.config(text=f"Congratulations! You guessed the number in {self.attempts} attempts.", fg="green")
                self.history.append(f"Number: {self.target_number}, Attempts: {self.attempts}")
                self.update_history()
                self.play_again_button.config(state=tk.NORMAL)  # Enable play again button
                self.timer_running = False  # Stop the timer when the correct guess is made

            # Provide a hint after 3 wrong guesses
            if self.hint_counter == 3 and guess != self.target_number:
                self.provide_hint()

        except ValueError:
            self.result_label.config(text="Please enter a valid number.", fg="red")

        self.attempts_label.config(text=f"Attempts: {self.attempts}")

    def provide_hint(self):
        if self.target_number % 2 == 0:
            self.result_label.config(text="Hint: The number is even!", fg="blue")
        else:
            self.result_label.config(text="Hint: The number is odd!", fg="blue")

    def update_history(self):
        # Clear the current list and update it with new history
        self.history_listbox.delete(0, tk.END)
        for entry in self.history:
            self.history_listbox.insert(tk.END, entry)

    def reset_game(self):
        self.target_number = 0
        self.attempts = 0
        self.attempts_label.config(text="Attempts: 0")
        self.result_label.config(text="")
        self.entry.delete(0, tk.END)
        self.play_again_button.config(state=tk.DISABLED)
        self.start_button.config(state=tk.NORMAL)  # Enable the start button

    def end_game(self, message):
        self.result_label.config(text=message)
        self.play_again_button.config(state=tk.NORMAL)  # Enable play again button
        self.update_history()
        self.timer_running = False  # Stop the timer

# Main code to run the app
if __name__ == "__main__":
    root = tk.Tk()
    game = NumberGuessingGame(root)
    root.mainloop()
