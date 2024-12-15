import tkinter as tk
from tkinter import ttk
import random

class NumberGuessingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Guessing Game")

        self.target_number = random.randint(1, 100)  # Random number between 1 and 100
        self.attempts = 0

        # History storage
        self.history = []

        # Create Notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=10, padx=10)

        # Game tab
        self.game_tab = tk.Frame(self.notebook)
        self.notebook.add(self.game_tab, text="Game")

        # History tab
        self.history_tab = tk.Frame(self.notebook)
        self.notebook.add(self.history_tab, text="History")

        # Create GUI components for the game tab
        self.label = tk.Label(self.game_tab, text="I am thinking of a number between 1 and 100", font=("Helvetica", 14))
        self.label.pack(pady=20)

        self.instruction_label = tk.Label(self.game_tab, text="Enter your guess:", font=("Helvetica", 12))
        self.instruction_label.pack()

        self.entry = tk.Entry(self.game_tab, font=("Helvetica", 12))
        self.entry.pack(pady=10)

        self.submit_button = tk.Button(self.game_tab, text="Submit Guess", command=self.check_guess, font=("Helvetica", 12))
        self.submit_button.pack(pady=10)

        self.result_label = tk.Label(self.game_tab, text="", font=("Helvetica", 12))
        self.result_label.pack(pady=10)

        self.attempts_label = tk.Label(self.game_tab, text="Attempts: 0", font=("Helvetica", 12))
        self.attempts_label.pack(pady=5)

        self.play_again_button = tk.Button(self.game_tab, text="Play Again", command=self.reset_game, font=("Helvetica", 12))
        self.play_again_button.pack(pady=10)
        self.play_again_button.config(state=tk.DISABLED)

        # Create the History Tab components
        self.history_label = tk.Label(self.history_tab, text="History of Guessed Numbers", font=("Helvetica", 14))
        self.history_label.pack(pady=20)

        self.history_listbox = tk.Listbox(self.history_tab, width=50, height=10, font=("Helvetica", 12))
        self.history_listbox.pack(pady=10)

    def check_guess(self):
        try:
            guess = int(self.entry.get())
            self.attempts += 1
            if guess < self.target_number:
                self.result_label.config(text="Too low! Try again.", fg="red")
            elif guess > self.target_number:
                self.result_label.config(text="Too high! Try again.", fg="red")
            else:
                self.result_label.config(text=f"Congratulations! You guessed the number in {self.attempts} attempts.", fg="green")
                self.history.append(f"Number: {self.target_number}, Attempts: {self.attempts}")
                self.update_history()
                self.play_again_button.config(state=tk.NORMAL)  # Enable play again button
        except ValueError:
            self.result_label.config(text="Please enter a valid number.", fg="red")

        self.attempts_label.config(text=f"Attempts: {self.attempts}")

    def update_history(self):
        # Clear the current list and update it with new history
        self.history_listbox.delete(0, tk.END)
        for entry in self.history:
            self.history_listbox.insert(tk.END, entry)

    def reset_game(self):
        self.target_number = random.randint(1, 100)  # New random number
        self.attempts = 0
        self.attempts_label.config(text="Attempts: 0")
        self.result_label.config(text="")
        self.entry.delete(0, tk.END)
        self.play_again_button.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    game = NumberGuessingGame(root)
    root.mainloop()
