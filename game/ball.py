import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

    def move(self, player, ai):
        """Move the ball and handle collision detection with walls and paddles."""
        # Move ball
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Bounce off top and bottom walls
        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1

        # Check for paddle collisions right after movement
        self.check_collision(player, ai)

    def check_collision(self, player, ai):
        """Check and correct collisions with paddles."""
        ball_rect = self.rect()
        player_rect = player.rect()
        ai_rect = ai.rect()

        # Check collision with player paddle
        if ball_rect.colliderect(player_rect):
            self.velocity_x = abs(self.velocity_x)  # ensure it moves right
            # Prevent ball from "sticking" inside paddle
            self.x = player_rect.right

        # Check collision with AI paddle
        elif ball_rect.colliderect(ai_rect):
            self.velocity_x = -abs(self.velocity_x)  # ensure it moves left
            self.x = ai_rect.left - self.width

    def reset(self):
        """Reset ball to center with reversed X direction."""
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x *= -1
        self.velocity_y = random.choice([-3, 3])

    def rect(self):
        """Return the ball's rectangle (for collision)."""
        return pygame.Rect(self.x, self.y, self.width, self.height)
