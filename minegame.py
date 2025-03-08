import tkinter as tk
from tkinter import messagebox
import random


class Minesweeper:
    def __init__(self, root):
        self.root = root
        self.root.title("Minesweeper")
        self.root.resizable(False, False)

        # Game parameters
        self.rows = 10
        self.cols = 10
        self.num_mines = 15
        self.cell_size = 30

        # Colors for numbers
        self.number_colors = {
            1: "#0000FF",  # Blue
            2: "#008000",  # Green
            3: "#FF0000",  # Red
            4: "#000080",  # Navy Blue
            5: "#800000",  # Maroon
            6: "#008080",  # Teal
            7: "#000000",  # Black
            8: "#808080"  # Gray
        }

        # Game state
        self.is_game_over = False
        self.is_first_click = True
        self.cells_revealed = 0

        # Create the game UI
        self.create_menu()
        self.create_status_bar()
        self.create_grid()
        self.initialize_board()

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        game_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Game", menu=game_menu)

        game_menu.add_command(label="New Game", command=self.reset_game)
        game_menu.add_separator()

        difficulty_menu = tk.Menu(game_menu, tearoff=0)
        game_menu.add_cascade(label="Difficulty", menu=difficulty_menu)

        difficulty_menu.add_command(label="Beginner (10x10, 15 mines)", command=lambda: self.set_difficulty(10, 10, 15))
        difficulty_menu.add_command(label="Intermediate (16x16, 40 mines)",
                                    command=lambda: self.set_difficulty(16, 16, 40))
        difficulty_menu.add_command(label="Expert (16x30, 99 mines)", command=lambda: self.set_difficulty(16, 30, 99))

        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=self.root.quit)

    def create_status_bar(self):
        self.status_frame = tk.Frame(self.root)
        self.status_frame.pack(fill=tk.X, padx=10, pady=10)

        # Mine counter
        self.mine_counter = tk.Label(
            self.status_frame,
            text=f"Mines: {self.num_mines}",
            font=("Arial", 12)
        )
        self.mine_counter.pack(side=tk.LEFT)

        # Reset button with smiley face
        self.reset_button = tk.Button(
            self.status_frame,
            text="🙂",
            font=("Arial", 12),
            width=3,
            command=self.reset_game
        )
        self.reset_button.pack(side=tk.LEFT, padx=20)

        # Game status
        self.status_label = tk.Label(
            self.status_frame,
            text="Game Ready",
            font=("Arial", 12)
        )
        self.status_label.pack(side=tk.RIGHT)

    def create_grid(self):
        # Create frame for grid
        self.grid_frame = tk.Frame(
            self.root,
            bd=2,
            relief=tk.SUNKEN
        )
        self.grid_frame.pack(padx=10, pady=10)

        # Create buttons grid
        self.buttons = []
        for row in range(self.rows):
            button_row = []
            for col in range(self.cols):
                button = tk.Button(
                    self.grid_frame,
                    width=2,
                    height=1,
                    font=("Arial", 10, "bold"),
                    bg="#d3d3d3",
                    bd=1,
                    relief=tk.RAISED
                )
                button.grid(row=row, column=col)
                button.bind("<Button-1>", lambda event, r=row, c=col: self.left_click(r, c))
                button.bind("<Button-3>", lambda event, r=row, c=col: self.right_click(r, c))
                button_row.append(button)
            self.buttons.append(button_row)

    def initialize_board(self):
        # Create data structure for board
        self.board = []
        for row in range(self.rows):
            self.board.append([0] * self.cols)

        # Flags to track flagged cells
        self.flags = []
        for row in range(self.rows):
            self.flags.append([False] * self.cols)

    def set_difficulty(self, rows, cols, mines):
        self.rows = rows
        self.cols = cols
        self.num_mines = mines

        # Destroy existing grid
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        self.reset_game()

    def place_mines(self, first_row, first_col):
        # Place mines randomly, avoiding first click
        mines_placed = 0
        while mines_placed < self.num_mines:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)

            # Avoid placing mine at first click or adjacent to it
            if abs(row - first_row) <= 1 and abs(col - first_col) <= 1:
                continue

            # Place mine if not already placed
            if self.board[row][col] != -1:
                self.board[row][col] = -1
                mines_placed += 1

        # Calculate numbers
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] == -1:
                    continue

                # Count adjacent mines
                mine_count = 0
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        r, c = row + dr, col + dc
                        if 0 <= r < self.rows and 0 <= c < self.cols and self.board[r][c] == -1:
                            mine_count += 1

                self.board[row][col] = mine_count

    def left_click(self, row, col):
        if self.is_game_over or self.flags[row][col]:
            return

        if self.is_first_click:
            self.is_first_click = False
            self.place_mines(row, col)
            self.status_label.config(text="Game Started")

        if self.board[row][col] == -1:
            # Hit a mine - game over
            self.reveal_mines()
            self.buttons[row][col].config(text="💣", bg="#ff0000")
            self.reset_button.config(text="😵")
            self.status_label.config(text="Game Over!")
            self.is_game_over = True
            messagebox.showinfo("Game Over", "You hit a mine!")
        else:
            # Reveal this cell
            self.reveal_cell(row, col)

            # Check if all non-mine cells are revealed
            if self.cells_revealed == (self.rows * self.cols) - self.num_mines:
                self.reveal_mines(mark=True)
                self.reset_button.config(text="😎")
                self.status_label.config(text="You Win!")
                self.is_game_over = True
                messagebox.showinfo("Congratulations", "You won the game!")

    def right_click(self, row, col):
        if self.is_game_over:
            return

        button = self.buttons[row][col]

        # Toggle flag
        if button["relief"] == tk.RAISED:
            if self.flags[row][col]:
                # Remove flag
                self.flags[row][col] = False
                button.config(text="")
                self.mine_counter.config(text=f"Mines: {self.num_mines - sum(sum(row) for row in self.flags)}")
            else:
                # Add flag
                self.flags[row][col] = True
                button.config(text="🚩", fg="red")
                self.mine_counter.config(text=f"Mines: {self.num_mines - sum(sum(row) for row in self.flags)}")

    def reveal_cell(self, row, col):
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return

        button = self.buttons[row][col]

        # Skip if already revealed or flagged
        if button["relief"] == tk.SUNKEN or self.flags[row][col]:
            return

        # Reveal the cell
        button.config(relief=tk.SUNKEN, bg="#f0f0f0")
        self.cells_revealed += 1

        if self.board[row][col] > 0:
            # Show number
            button.config(
                text=str(self.board[row][col]),
                fg=self.number_colors.get(self.board[row][col], "black")
            )
        elif self.board[row][col] == 0:
            # Empty cell - reveal adjacent cells
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    self.reveal_cell(row + dr, col + dc)

    def reveal_mines(self, mark=False):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] == -1:
                    if mark:
                        # Mark with flag if won
                        self.buttons[row][col].config(text="🚩", fg="red")
                    else:
                        # Show mine if lost
                        self.buttons[row][col].config(text="💣", bg="#d3d3d3")

    def reset_game(self):
        # Reset game state
        self.is_game_over = False
        self.is_first_click = True
        self.cells_revealed = 0

        # Recreate grid if size changed
        if len(self.buttons) != self.rows or len(self.buttons[0]) != self.cols:
            # Destroy existing grid
            for widget in self.grid_frame.winfo_children():
                widget.destroy()

            # Create new grid
            self.create_grid()

        # Reset buttons
        for row in range(self.rows):
            for col in range(self.cols):
                self.buttons[row][col].config(
                    text="",
                    relief=tk.RAISED,
                    bg="#d3d3d3"
                )

        # Initialize new board
        self.initialize_board()

        # Reset UI elements
        self.reset_button.config(text="🙂")
        self.mine_counter.config(text=f"Mines: {self.num_mines}")
        self.status_label.config(text="Game Ready")

        # Update window size
        width = self.cols * self.cell_size + 40
        height = self.rows * self.cell_size + 100
        self.root.geometry(f"{width}x{height}")


def main():
    root = tk.Tk()
    game = Minesweeper(root)
    root.mainloop()


if __name__ == "__main__":
    main()