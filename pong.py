import tkinter as tk
import random
import time


class PongGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Pong Game")
        self.root.resizable(False, False)

        # Game constants
        self.WIDTH = 800
        self.HEIGHT = 500
        self.PADDLE_WIDTH = 15
        self.PADDLE_HEIGHT = 80
        self.BALL_SIZE = 15
        self.PADDLE_SPEED = 10
        self.BALL_SPEED_X = 5
        self.BALL_SPEED_Y = 5
        self.INITIAL_BALL_SPEED = 5
        self.MAX_BALL_SPEED = 15
        self.ACCELERATION_FACTOR = 0.1

        # Game variables
        self.player1_score = 0
        self.player2_score = 0
        self.game_over = False
        self.paused = False

        # Create game canvas
        self.canvas = tk.Canvas(root, width=self.WIDTH, height=self.HEIGHT, bg="black")
        self.canvas.pack()

        # Initialize paddles and ball
        self.init_game_objects()

        # Create score displays
        self.p1_score_display = self.canvas.create_text(
            self.WIDTH / 4, 30, text=f"Player 1: {self.player1_score}",
            fill="white", font=("Arial", 16)
        )

        self.p2_score_display = self.canvas.create_text(
            3 * self.WIDTH / 4, 30, text=f"Player 2: {self.player2_score}",
            fill="white", font=("Arial", 16)
        )

        # Create center line
        self.draw_center_line()

        # Set up key bindings
        self.key_bindings()

        # Start game loop
        self.game_loop()

    def init_game_objects(self):
        """Initialize paddle and ball objects"""
        # Player 1 paddle (left)
        self.paddle1_y = self.HEIGHT / 2 - self.PADDLE_HEIGHT / 2
        self.paddle1 = self.canvas.create_rectangle(
            10, self.paddle1_y,
            10 + self.PADDLE_WIDTH, self.paddle1_y + self.PADDLE_HEIGHT,
            fill="white"
        )

        # Player 2 paddle (right)
        self.paddle2_y = self.HEIGHT / 2 - self.PADDLE_HEIGHT / 2
        self.paddle2 = self.canvas.create_rectangle(
            self.WIDTH - 10 - self.PADDLE_WIDTH, self.paddle2_y,
            self.WIDTH - 10, self.paddle2_y + self.PADDLE_HEIGHT,
            fill="white"
        )

        # Ball
        self.ball_x = self.WIDTH / 2 - self.BALL_SIZE / 2
        self.ball_y = self.HEIGHT / 2 - self.BALL_SIZE / 2
        self.ball = self.canvas.create_oval(
            self.ball_x, self.ball_y,
            self.ball_x + self.BALL_SIZE, self.ball_y + self.BALL_SIZE,
            fill="white"
        )

        # Initial ball direction (random)
        self.ball_dx = self.INITIAL_BALL_SPEED * random.choice([-1, 1])
        self.ball_dy = self.INITIAL_BALL_SPEED * random.choice([-0.8, 0.8])

    def draw_center_line(self):
        """Draw dashed line in the center of the court"""
        for y in range(0, self.HEIGHT, 30):
            self.canvas.create_line(
                self.WIDTH / 2, y, self.WIDTH / 2, y + 15,
                fill="white", width=2
            )

    def key_bindings(self):
        """Set up keyboard controls"""
        # Player 1 controls (W and S keys)
        self.root.bind("<w>", lambda e: self.move_paddle1(-self.PADDLE_SPEED))
        self.root.bind("<s>", lambda e: self.move_paddle1(self.PADDLE_SPEED))
        self.root.bind("<W>", lambda e: self.move_paddle1(-self.PADDLE_SPEED))
        self.root.bind("<S>", lambda e: self.move_paddle1(self.PADDLE_SPEED))

        # Player 2 controls (Up and Down arrow keys)
        self.root.bind("<Up>", lambda e: self.move_paddle2(-self.PADDLE_SPEED))
        self.root.bind("<Down>", lambda e: self.move_paddle2(self.PADDLE_SPEED))

        # Game controls
        self.root.bind("<space>", lambda e: self.toggle_pause())
        self.root.bind("<r>", lambda e: self.reset_game())

    def move_paddle1(self, dy):
        """Move player 1's paddle"""
        if self.game_over or self.paused:
            return

        current_pos = self.canvas.coords(self.paddle1)
        new_y = current_pos[1] + dy

        # Check boundaries
        if new_y > 0 and new_y + self.PADDLE_HEIGHT < self.HEIGHT:
            self.canvas.move(self.paddle1, 0, dy)
            self.paddle1_y = new_y

    def move_paddle2(self, dy):
        """Move player 2's paddle"""
        if self.game_over or self.paused:
            return

        current_pos = self.canvas.coords(self.paddle2)
        new_y = current_pos[1] + dy

        # Check boundaries
        if new_y > 0 and new_y + self.PADDLE_HEIGHT < self.HEIGHT:
            self.canvas.move(self.paddle2, 0, dy)
            self.paddle2_y = new_y

    def move_ball(self):
        """Update ball position and handle collisions"""
        # Move ball
        self.canvas.move(self.ball, self.ball_dx, self.ball_dy)

        # Get current ball position
        ball_pos = self.canvas.coords(self.ball)
        ball_left = ball_pos[0]
        ball_top = ball_pos[1]
        ball_right = ball_pos[2]
        ball_bottom = ball_pos[3]

        # Wall collisions (top and bottom)
        if ball_top <= 0 or ball_bottom >= self.HEIGHT:
            self.ball_dy = -self.ball_dy

        # Paddle collisions
        if ball_left <= 10 + self.PADDLE_WIDTH:
            # Check if ball hit paddle1
            paddle1_pos = self.canvas.coords(self.paddle1)
            if ball_bottom >= paddle1_pos[1] and ball_top <= paddle1_pos[3]:
                # Calculate impact point on paddle (0 to 1)
                relative_impact = (ball_top + self.BALL_SIZE / 2 - paddle1_pos[1]) / self.PADDLE_HEIGHT
                self.handle_paddle_collision(relative_impact)

        elif ball_right >= self.WIDTH - 10 - self.PADDLE_WIDTH:
            # Check if ball hit paddle2
            paddle2_pos = self.canvas.coords(self.paddle2)
            if ball_bottom >= paddle2_pos[1] and ball_top <= paddle2_pos[3]:
                # Calculate impact point on paddle (0 to 1)
                relative_impact = (ball_top + self.BALL_SIZE / 2 - paddle2_pos[1]) / self.PADDLE_HEIGHT
                self.handle_paddle_collision(relative_impact)

        # Score (ball out of bounds)
        if ball_left <= 0:
            self.player2_score += 1
            self.update_scores()
            self.reset_ball()

        elif ball_right >= self.WIDTH:
            self.player1_score += 1
            self.update_scores()
            self.reset_ball()

    def handle_paddle_collision(self, relative_impact):
        """Handle ball bouncing off a paddle with angle based on where it hit"""
        # Reverse horizontal direction
        self.ball_dx = -self.ball_dx

        # Increase speed slightly with each hit
        speed_factor = min(abs(self.ball_dx) + self.ACCELERATION_FACTOR, self.MAX_BALL_SPEED)
        if self.ball_dx > 0:
            self.ball_dx = speed_factor
        else:
            self.ball_dx = -speed_factor

        # Adjust vertical direction based on where the ball hit the paddle
        # Middle of paddle = straight, top = upward angle, bottom = downward angle
        new_angle = (relative_impact - 0.5) * 2  # Range from -1 to 1
        self.ball_dy = new_angle * abs(self.ball_dx) * 0.8  # Scale vertical component

    def reset_ball(self):
        """Reset the ball to the center after a point is scored"""
        # Move ball to center
        current_pos = self.canvas.coords(self.ball)
        dx = self.WIDTH / 2 - (current_pos[0] + self.BALL_SIZE / 2)
        dy = self.HEIGHT / 2 - (current_pos[1] + self.BALL_SIZE / 2)
        self.canvas.move(self.ball, dx, dy)

        # Reset ball position variables
        self.ball_x = self.WIDTH / 2 - self.BALL_SIZE / 2
        self.ball_y = self.HEIGHT / 2 - self.BALL_SIZE / 2

        # Set random direction
        self.ball_dx = self.INITIAL_BALL_SPEED * random.choice([-1, 1])
        self.ball_dy = self.INITIAL_BALL_SPEED * random.choice([-0.8, 0.8])

        # Brief pause
        self.canvas.update()
        time.sleep(1)

    def update_scores(self):
        """Update the score displays"""
        self.canvas.itemconfig(self.p1_score_display, text=f"Player 1: {self.player1_score}")
        self.canvas.itemconfig(self.p2_score_display, text=f"Player 2: {self.player2_score}")

        # Check for game over (first to 5 points)
        if self.player1_score >= 5 or self.player2_score >= 5:
            self.game_over = True
            self.show_game_over()

    def show_game_over(self):
        """Display game over message"""
        winner = "Player 1" if self.player1_score >= 5 else "Player 2"
        self.canvas.create_rectangle(
            self.WIDTH / 4, self.HEIGHT / 3,
            3 * self.WIDTH / 4, 2 * self.HEIGHT / 3,
            fill="black", outline="white", width=2
        )
        self.canvas.create_text(
            self.WIDTH / 2, self.HEIGHT / 2 - 20,
            text=f"{winner} Wins!",
            fill="white", font=("Arial", 24)
        )
        self.canvas.create_text(
            self.WIDTH / 2, self.HEIGHT / 2 + 20,
            text="Press 'r' to restart",
            fill="white", font=("Arial", 18)
        )

    def toggle_pause(self):
        """Pause or resume the game"""
        self.paused = not self.paused
        if self.paused:
            self.pause_text = self.canvas.create_text(
                self.WIDTH / 2, self.HEIGHT / 2,
                text="PAUSED\nPress SPACE to continue",
                fill="white", font=("Arial", 20),
                justify="center"
            )
        else:
            self.canvas.delete(self.pause_text)

    def reset_game(self):
        """Reset the game to initial state"""
        self.player1_score = 0
        self.player2_score = 0
        self.game_over = False
        self.paused = False

        # Clear canvas and redraw everything
        self.canvas.delete("all")
        self.init_game_objects()
        self.draw_center_line()

        # Recreate score displays
        self.p1_score_display = self.canvas.create_text(
            self.WIDTH / 4, 30, text=f"Player 1: {self.player1_score}",
            fill="white", font=("Arial", 16)
        )

        self.p2_score_display = self.canvas.create_text(
            3 * self.WIDTH / 4, 30, text=f"Player 2: {self.player2_score}",
            fill="white", font=("Arial", 16)
        )

    def game_loop(self):
        """Main game loop"""
        if not self.game_over and not self.paused:
            self.move_ball()

        # Continue loop
        self.root.after(16, self.game_loop)  # ~60 FPS


# Start the game
if __name__ == "__main__":
    root = tk.Tk()
    game = PongGame(root)
    root.mainloop()