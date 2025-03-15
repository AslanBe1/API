import pygame
import random

pygame.init()

WIDTH, HEIGHT = 600, 400
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("So‘z Topish O‘yini")

font = pygame.font.Font(None, 50)
small_font = pygame.font.Font(None, 30)

words = ["python", "developer", "game", "django", "telegram", "database", "computer","Oppoqor"]

def new_game():
    global word, hidden_word, attempts, guessed_letters, game_over
    word = random.choice(words)
    hidden_word = ["_"] * len(word)
    attempts = 6
    guessed_letters = []
    game_over = False

new_game()

running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if not game_over:
                if event.unicode.isalpha():
                    letter = event.unicode.lower()

                    if letter not in guessed_letters:
                        guessed_letters.append(letter)
                        if letter in word:
                            for i in range(len(word)):
                                if word[i] == letter:
                                    hidden_word[i] = letter
                        else:
                            attempts -= 1

            elif event.key == pygame.K_RETURN:
                new_game()

    word_surface = font.render(" ".join(hidden_word), True, BLACK)
    attempts_surface = font.render(f"Urinishlar: {attempts}", True, RED)

    screen.blit(word_surface, (WIDTH // 2 - 100, HEIGHT // 3))
    screen.blit(attempts_surface, (10, 10))

    if "_" not in hidden_word:
        win_surface = small_font.render(f"🎉 Barcha Haflarni topdigiz bu soz {word}!", True, GREEN)
        restart_surface = small_font.render("ENTER tugmasini bosib yana o‘ynang!", True, BLACK)
        screen.blit(win_surface, (WIDTH // 2 - 50, HEIGHT // 2))
        screen.blit(restart_surface, (WIDTH // 2 - 120, HEIGHT // 2 + 50))
        game_over = True

    elif attempts == 0:
        lose_surface = font.render(f"😢 Yutqazdingiz! {word}", True, RED)
        restart_surface = small_font.render("ENTER tugmasini bosib yana o‘ynang!", True, BLACK)
        screen.blit(lose_surface, (WIDTH // 2 - 100, HEIGHT // 2))
        screen.blit(restart_surface, (WIDTH // 2 - 120, HEIGHT // 2 + 50))
        game_over = True

    pygame.display.flip()
    pygame.time.delay(100)

pygame.quit()
