"""
Create a Rock Paper Scissors game where the player inputs their choice
and plays  against a computer that randomly selects its move, 
with the game showing who won each round.
Add a score counter that tracks player and computer wins, 
and allow the game to continue until the player types “quit”.
"""
import random
import tkinter as tk

class Scoreboard:
    """Track wins, losses, ties, and per-round history."""
    def __init__(self):
        self.player_wins = 0
        self.computer_wins = 0
        self.ties = 0
        self.history = []  # list of dicts: {'player':..., 'computer':..., 'winner':...}

    def record(self, player_choice, computer_choice, winner):
        if winner == 'player':
            self.player_wins += 1
        elif winner == 'computer':
            self.computer_wins += 1
        else:
            self.ties += 1
        self.history.append({'player': player_choice, 'computer': computer_choice, 'winner': winner})

    def running_score(self):
        return f"You: {self.player_wins}  Computer: {self.computer_wins}  Ties: {self.ties}"

    def display_full(self):
        lines = []
        lines.append("\nDetailed scoreboard:")
        lines.append("{:<6} {:<10} {:<10} {:<10}".format("Round", "Player", "Computer", "Result"))
        for i, r in enumerate(self.history, start=1):
            res = r['winner'] if r['winner'] in ('player', 'computer') else 'tie'
            lines.append("{:<6} {:<10} {:<10} {:<10}".format(i, r['player'], r['computer'], res))
        lines.append("\nTotals: You: {}  Computer: {}  Ties: {}\n".format(self.player_wins, self.computer_wins, self.ties))
        return "\n".join(lines)

    def reset(self):
        """Reset all scores and history."""
        self.player_wins = 0
        self.computer_wins = 0
        self.ties = 0
        self.history = []

def get_computer_choice() -> str:
    """Randomly select and return the computer's choice."""
    return random.choice(['rock', 'paper', 'scissors'])

def determine_winner(player: str, computer: str) -> str:
    """Return 'player', 'computer' or 'tie' to indicate the winner."""
    if player == computer:
        return 'tie'
    elif (player == 'rock' and computer == 'scissors') or \
         (player == 'paper' and computer == 'rock') or \
         (player == 'scissors' and computer == 'paper'):
        return 'player'
    else:
        return 'computer'

def result_message(winner: str) -> str:
    if winner == 'player':
        return "You win!"
    elif winner == 'computer':
        return "Computer wins!"
    else:
        return "It's a tie!"
def play_game_cli() -> None:
    """Command-line version (kept for compatibility)."""
    scoreboard = Scoreboard()
    while True:
        user_input = input("Enter rock (r), paper (p), scissors (s) or quit to exit: ").lower()
        if user_input == 'r':
            player_choice = 'rock'
        elif user_input == 'p':
            player_choice = 'paper'
        elif user_input == 's':
            player_choice = 'scissors'
        else:
            player_choice = user_input
        if player_choice == 'quit':
            print("Thanks for playing!")
            print(scoreboard.display_full())
            break
        if player_choice not in ['rock', 'paper', 'scissors']:
            print("Invalid choice. Please try again.")
            continue
        computer_choice = get_computer_choice()
        print(f"Computer chose: {computer_choice}")
        winner = determine_winner(player_choice, computer_choice)
        message = result_message(winner)
        print(message)
        scoreboard.record(player_choice, computer_choice, winner)
        print(f"Score - {scoreboard.running_score()}\n")


def play_game() -> None:
    """Simple Tkinter GUI for Rock Paper Scissors with a detailed scoreboard."""
    root = tk.Tk()
    root.title("Rock Paper Scissors")
    root.resizable(False, False)
    root.configure(bg="#2c3e50")
    TEXT_FG = "#ffd700"

    scoreboard = Scoreboard()

    player_score = tk.IntVar(value=0)
    computer_score = tk.IntVar(value=0)
    ties = tk.IntVar(value=0)
    score_var = tk.StringVar(value=scoreboard.running_score())
    status_var = tk.StringVar(value="Make your choice.")

    title_label = tk.Label(root, text="🎮 Rock Paper Scissors 🎮", font=("Helvetica", 16, "bold"), bg="#2c3e50", fg=TEXT_FG)
    title_label.pack(pady=(15,10))

    score_label = tk.Label(root, textvariable=score_var, font=("Helvetica", 12, "bold"), bg="#34495e", fg=TEXT_FG, padx=10, pady=8)
    score_label.pack(pady=(0,12), fill="x", padx=10)

    status_label = tk.Label(root, textvariable=status_var, font=("Helvetica", 10), bg="#2c3e50", fg=TEXT_FG, wraplength=300)
    status_label.pack(pady=(0,15))

    btn_frame = tk.Frame(root, bg="#2c3e50")
    btn_frame.pack(padx=10, pady=5)

    def update_score_vars():
        player_score.set(scoreboard.player_wins)
        computer_score.set(scoreboard.computer_wins)
        ties.set(scoreboard.ties)
        score_var.set(scoreboard.running_score())

    def on_choice(player_choice: str):
        computer_choice = get_computer_choice()
        winner = determine_winner(player_choice, computer_choice)
        message = result_message(winner)
        scoreboard.record(player_choice, computer_choice, winner)
        update_score_vars()
        status_var.set(f"You chose {player_choice}. Computer chose {computer_choice}. {message}")

    def show_scoreboard():
        top = tk.Toplevel(root)
        top.title("Detailed Scoreboard")
        top.resizable(False, False)
        top.configure(bg="#34495e")
        header = tk.Label(top, text="Round  Player     Computer    Result", font=("Helvetica", 10, "bold"), anchor="w", bg="#34495e", fg=TEXT_FG)
        header.pack(padx=8, pady=(8,0), anchor="w")
        for i, r in enumerate(scoreboard.history, start=1):
            res = r['winner'] if r['winner'] in ('player', 'computer') else 'tie'
            line = f"{i:<6} {r['player']:<10} {r['computer']:<10} {res:<10}"
            tk.Label(top, text=line, anchor="w", font=("Courier", 10), bg="#34495e", fg=TEXT_FG).pack(padx=8, anchor="w")
        tk.Label(top, text=f"\nTotals: You: {scoreboard.player_wins}  Computer: {scoreboard.computer_wins}  Ties: {scoreboard.ties}", font=("Helvetica", 10, "bold"), bg="#34495e", fg=TEXT_FG).pack(padx=8, pady=(8,10), anchor="w")

    tk.Button(btn_frame, text="🪨 Rock", width=12, command=lambda: on_choice('rock'), bg="#3498db", fg=TEXT_FG, font=("Helvetica", 10, "bold"), activebackground="#2980b9").grid(row=0, column=0, padx=5)
    tk.Button(btn_frame, text="📄 Paper", width=12, command=lambda: on_choice('paper'), bg="#e74c3c", fg=TEXT_FG, font=("Helvetica", 10, "bold"), activebackground="#c0392b").grid(row=0, column=1, padx=5)
    tk.Button(btn_frame, text="✂️ Scissors", width=12, command=lambda: on_choice('scissors'), bg="#f39c12", fg=TEXT_FG, font=("Helvetica", 10, "bold"), activebackground="#d68910").grid(row=0, column=2, padx=5)

    control_frame = tk.Frame(root, bg="#2c3e50")
    control_frame.pack(pady=(15,15))

    def reset_scoreboard():
        """Reset the scoreboard and update UI."""
        scoreboard.reset()
        update_score_vars()
        status_var.set("Scoreboard reset.")

    tk.Button(control_frame, text="Show Scoreboard", command=show_scoreboard, bg="#27ae60", fg=TEXT_FG, font=("Helvetica", 9, "bold"), padx=8, pady=5).grid(row=0, column=0, padx=5)
    tk.Button(control_frame, text="Reset", command=reset_scoreboard, bg="#f39c12", fg=TEXT_FG, font=("Helvetica", 9, "bold"), padx=8, pady=5).grid(row=0, column=1, padx=5)
    tk.Button(control_frame, text="Quit", command=root.destroy, bg="#e74c3c", fg=TEXT_FG, font=("Helvetica", 9, "bold"), padx=8, pady=5).grid(row=0, column=2, padx=5)

    root.mainloop()


if __name__ == "__main__":
    play_game()