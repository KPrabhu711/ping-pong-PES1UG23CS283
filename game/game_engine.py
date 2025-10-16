import pygame
from .paddle import Paddle
from .ball import Ball
import time

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.font = pygame.font.SysFont("Arial", 30)

        self.reset_game(best_of=5)  # Default best of 5

    def reset_game(self, best_of):
        """Reset everything for a new match."""
        self.best_of = best_of
        self.winning_score = best_of // 2 + 1  # e.g., Best of 5 → first to 3
        self.player = Paddle(10, self.height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(self.width - 20, self.height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(self.width // 2, self.height // 2, 7, 7, self.width, self.height)
        self.player_score = 0
        self.ai_score = 0
        self.game_over = False
        self.winner_text = ""
        self.show_replay_menu = False

    def handle_input(self):
        """Handle player paddle movement and replay input."""
        keys = pygame.key.get_pressed()

        # If replay menu is shown, wait for input choice
        if self.show_replay_menu:
            if keys[pygame.K_3]:
                self.reset_game(best_of=3)
            elif keys[pygame.K_5]:
                self.reset_game(best_of=5)
            elif keys[pygame.K_7]:
                self.reset_game(best_of=7)
            elif keys[pygame.K_ESCAPE]:
                pygame.quit()
                quit()
            return

        if self.game_over:
            return

        # Player paddle control
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        """Update game state and handle game flow."""
        if self.show_replay_menu or self.game_over:
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
        if self.player_score >= self.winning_score:
            self.winner_text = "Player Wins!"
            self.game_over = True
        elif self.ai_score >= self.winning_score:
            self.winner_text = "AI Wins!"
            self.game_over = True

        if self.game_over:
            self.show_replay_menu = True

    def render(self, screen):
        """Render paddles, ball, and scores. Handle game over and replay menu."""
        screen.fill(BLACK)

        # Draw paddles, ball, net
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width // 2, 0), (self.width // 2, self.height))

        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width // 4, 20))
        screen.blit(ai_text, (self.width * 3 // 4, 20))

        # Show game over text and replay options
        if self.show_replay_menu:
            self.render_game_over(screen)

    def render_game_over(self, screen):
        screen.fill(BLACK)

        # Display winner
        winner_surface = self.font.render(self.winner_text, True, WHITE)
        screen.blit(
            winner_surface,
            (self.width // 2 - winner_surface.get_width() // 2, self.height // 2 - 80)
        )

        # Replay prompt
        prompt_surface = self.font.render(
            "Select: [3] Best of 3   [5] Best of 5   [7] Best of 7   [ESC] Exit",
            True,
            WHITE
        )
        screen.blit(
            prompt_surface,
            (self.width // 2 - prompt_surface.get_width() // 2, self.height // 2)
        )

        # Small subtext for clarity
        sub_surface = self.font.render(
            "Press a key to continue...",
            True,
            WHITE
        )
        screen.blit(
            sub_surface,
            (self.width // 2 - sub_surface.get_width() // 2, self.height // 2 + 60)
        )

