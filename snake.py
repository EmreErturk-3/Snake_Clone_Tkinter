import tkinter as tk
import random


class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")
        self.root.resizable(False, False)

        # Game constants
        self.WIDTH = 600
        self.HEIGHT = 400
        self.GRID_SIZE = 20
        self.GAME_SPEED = 150  # milliseconds between updates

        # Game variables
        self.direction = "Right"
        self.next_direction = "Right"
        self.score = 0
        self.game_over = False

        # Initialize snake and food
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.food = self.create_food()

        # Create game canvas
        self.canvas = tk.Canvas(root, width=self.WIDTH, height=self.HEIGHT, bg="black")
        self.canvas.pack()

        # Create score display
        self.score_display = self.canvas.create_text(
            self.WIDTH - 50, 10, text=f"Score: {self.score}",
            fill="white", font=("Arial", 12), anchor="ne"
        )

        # Set up key bindings
        self.root.bind("<KeyPress-Up>", lambda e: self.change_direction("Up"))
        self.root.bind("<KeyPress-Down>", lambda e: self.change_direction("Down"))
        self.root.bind("<KeyPress-Left>", lambda e: self.change_direction("Left"))
        self.root.bind("<KeyPress-Right>", lambda e: self.change_direction("Right"))
        self.root.bind("<KeyPress-r>", lambda e: self.reset_game())

        # Start game
        self.game_loop()

    def create_food(self):
        """Create a new food at a random position."""
        x = random.randint(1, (self.WIDTH - self.GRID_SIZE) // self.GRID_SIZE) * self.GRID_SIZE
        y = random.randint(1, (self.HEIGHT - self.GRID_SIZE) // self.GRID_SIZE) * self.GRID_SIZE

        # Ensure food doesn't appear on snake
        while (x, y) in self.snake:
            x = random.randint(1, (self.WIDTH - self.GRID_SIZE) // self.GRID_SIZE) * self.GRID_SIZE
            y = random.randint(1, (self.HEIGHT - self.GRID_SIZE) // self.GRID_SIZE) * self.GRID_SIZE

        return (x, y)

    def change_direction(self, new_direction):
        """Change the snake's direction ensuring it can't reverse onto itself."""
        if (new_direction == "Left" and self.direction != "Right") or \
                (new_direction == "Right" and self.direction != "Left") or \
                (new_direction == "Up" and self.direction != "Down") or \
                (new_direction == "Down" and self.direction != "Up"):
            self.next_direction = new_direction

    def move_snake(self):
        """Move the snake in the current direction."""
        head_x, head_y = self.snake[0]

        # Set direction for next move
        self.direction = self.next_direction

        # Calculate new head position
        if self.direction == "Right":
            new_head = (head_x + self.GRID_SIZE, head_y)
        elif self.direction == "Left":
            new_head = (head_x - self.GRID_SIZE, head_y)
        elif self.direction == "Up":
            new_head = (head_x, head_y - self.GRID_SIZE)
        elif self.direction == "Down":
            new_head = (head_x, head_y + self.GRID_SIZE)

        # Check for collisions
        if self.check_collision(new_head):
            self.game_over = True
            self.show_game_over()
            return

        # Add new head
        self.snake.insert(0, new_head)

        # Check if snake ate food
        if new_head == self.food:
            self.score += 10
            self.canvas.itemconfig(self.score_display, text=f"Score: {self.score}")
            self.food = self.create_food()
        else:
            # Remove tail if no food was eaten
            self.snake.pop()

    def check_collision(self, position):
        """Check if the position collides with walls or snake body."""
        x, y = position

        # Check wall collision
        if x < 0 or x >= self.WIDTH or y < 0 or y >= self.HEIGHT:
            return True

        # Check self collision (excluding the tail which will move)
        if position in self.snake[:-1]:
            return True

        return False

    def draw_objects(self):
        """Draw snake and food on the canvas."""
        # Clear canvas
        self.canvas.delete("snake", "food")

        # Draw food
        self.canvas.create_oval(
            self.food[0], self.food[1],
            self.food[0] + self.GRID_SIZE, self.food[1] + self.GRID_SIZE,
            fill="red", tags="food"
        )

        # Draw snake
        for segment in self.snake:
            self.canvas.create_rectangle(
                segment[0], segment[1],
                segment[0] + self.GRID_SIZE, segment[1] + self.GRID_SIZE,
                fill="green", outline="darkgreen", tags="snake"
            )

        # Make head a different color
        head = self.snake[0]
        self.canvas.create_rectangle(
            head[0], head[1],
            head[0] + self.GRID_SIZE, head[1] + self.GRID_SIZE,
            fill="lime", outline="darkgreen", tags="snake"
        )

    def show_game_over(self):
        """Display game over message."""
        self.canvas.create_text(
            self.WIDTH // 2, self.HEIGHT // 2,
            text=f"Game Over! Score: {self.score}\nPress 'r' to restart",
            fill="white", font=("Arial", 20), justify="center"
        )

    def reset_game(self):
        """Reset the game to initial state."""
        self.direction = "Right"
        self.next_direction = "Right"
        self.score = 0
        self.game_over = False
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.food = self.create_food()
        self.canvas.itemconfig(self.score_display, text=f"Score: {self.score}")
        self.canvas.delete("all")
        self.score_display = self.canvas.create_text(
            self.WIDTH - 50, 10, text=f"Score: {self.score}",
            fill="white", font=("Arial", 12), anchor="ne"
        )
        self.game_loop()

    def game_loop(self):
        """Main game loop."""
        if not self.game_over:
            self.move_snake()
            self.draw_objects()
            self.root.after(self.GAME_SPEED, self.game_loop)


# Start the game
if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()