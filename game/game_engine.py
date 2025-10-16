import pygame
from .paddle import Paddle
from .ball import Ball
import time

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WINNING_SCORE = 5  # End condition

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)
        self.game_over = False
        self.winner_text = ""

    def handle_input(self):
        """Handle player paddle movement (W/S keys)."""
        if self.game_over:
            return  # Disable controls after game ends

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        """Update game state and check for game over."""
        if self.game_over:
            return

        # Move AI and Ball
        self.ai.auto_track(self.ball, self.height)
        self.ball.move(self.player, self.ai)

        # Scoring logic
        if self.ball.x <= 0:
            self.ai_score += 1
            self.ball.reset()
        elif self.ball.x + self.ball.width >= self.width:
            self.player_score += 1
            self.ball.reset()

        # Check for game over
        self.check_game_over()

    def check_game_over(self):
        """Check if a player has reached the winning score."""
        if self.player_score >= WINNING_SCORE:
            self.winner_text = "Player Wins!"
            self.game_over = True
        elif self.ai_score >= WINNING_SCORE:
            self.winner_text = "AI Wins!"
            self.game_over = True

    def render(self, screen):
        """Render paddles, ball, net, and scores. Show game over if applicable."""
        screen.fill(BLACK)

        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width // 2, 0), (self.width // 2, self.height))

        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width // 4, 20))
        screen.blit(ai_text, (self.width * 3 // 4, 20))

        # If game over, display winner message
        if self.game_over:
            winner_surface = self.font.render(self.winner_text, True, WHITE)
            screen.blit(
                winner_surface,
                (self.width // 2 - winner_surface.get_width() // 2, self.height // 2 - 20)
            )
            pygame.display.flip()
            time.sleep(3)  # Keep the message visible for a few seconds
            pygame.quit()
            quit()
