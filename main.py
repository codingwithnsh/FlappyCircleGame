import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen Dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (135, 206, 250)
GREEN = (0, 200, 0)
RED = (255, 0, 0)

# Game Variables
GRAVITY = 0.5
FLAP_STRENGTH = -10
PIPE_SPEED = 5
PIPE_GAP = 150

# Initialize Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.Font(None, 36)


# Bird Class
class Bird:
    def __init__(self):
        self.x = 50
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.width = 30
        self.height = 30

    def draw(self):
        pygame.draw.ellipse(screen, RED, (self.x, self.y, self.width, self.height))

    def move(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def flap(self):
        self.velocity = FLAP_STRENGTH


# Pipe Class
class Pipe:
    def __init__(self, x):
        self.x = x
        self.top_height = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)
        self.bottom_height = SCREEN_HEIGHT - self.top_height - PIPE_GAP
        self.width = 80

    def draw(self):
        # Top pipe
        pygame.draw.rect(screen, GREEN, (self.x, 0, self.width, self.top_height))
        # Bottom pipe
        pygame.draw.rect(screen, GREEN, (self.x, self.top_height + PIPE_GAP, self.width, self.bottom_height))

    def move(self):
        self.x -= PIPE_SPEED

    def is_off_screen(self):
        return self.x + self.width < 0


# Main Game Loop
def main():
    bird = Bird()
    pipes = [Pipe(SCREEN_WIDTH + 100)]
    score = 0
    running = True

    while running:
        screen.fill(BLUE)  # Background color

        # Draw and move the bird
        bird.draw()
        bird.move()

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird.flap()

        # Draw and move pipes
        for pipe in pipes:
            pipe.draw()
            pipe.move()

            # Check if pipe is off screen
            if pipe.is_off_screen():
                pipes.remove(pipe)
                pipes.append(Pipe(SCREEN_WIDTH + 100))
                score += 1

            # Collision Detection
            if (bird.x + bird.width > pipe.x and bird.x < pipe.x + pipe.width and
                    (bird.y < pipe.top_height or bird.y + bird.height > pipe.top_height + PIPE_GAP)):
                running = False

        # Check if bird hits the ground or flies off screen
        if bird.y > SCREEN_HEIGHT or bird.y < 0:
            running = False

        # Display Score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Update Display
        pygame.display.flip()
        clock.tick(FPS)

    # Game Over Screen
    game_over(score)


def game_over(score):
    while True:
        screen.fill(BLACK)
        game_over_text = font.render("Game Over", True, WHITE)
        score_text = font.render(f"Your Score: {score}", True, WHITE)
        restart_text = font.render("Press SPACE to Restart", True, WHITE)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 3))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 1.5))
        pygame.display.flip()

        # Handle Restart or Quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                main()


# Run the Game
if __name__ == "__main__":
    main()
