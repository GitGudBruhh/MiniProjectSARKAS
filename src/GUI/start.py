import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen dimensions and settings
SCREEN_WIDTH, SCREEN_HEIGHT = 1600, 900
BACKGROUND_COLOR = (100, 100,100)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Mastermind')

# Define colors
COLORS = [(26, 188, 156), (46, 204, 113), (52, 152, 219), (155, 89, 182), (241, 196, 15), (230, 126, 34), (231, 76, 60), (236, 240, 241)]
COLOR_PICKER_POS = [(100 + i * 100, SCREEN_HEIGHT - 150) for i in range(len(COLORS))]
SLOT_POS = [[(400 + j * 100, 200 + i * 100) for j in range(4)] for i in range(10)]

# Load fonts
font = pygame.font.Font(None, 60)

# Game variables
num_slots = 4
num_colors = 6
selected_color = None
current_guess = []
guesses = []
feedback = []
solution = [random.choice(COLORS[:num_colors]) for _ in range(num_slots)]

def draw_text(text, position, font, color=(0, 0, 0), center=False):
    label = font.render(text, True, color)
    rect = label.get_rect()
    if center:
        position = (position[0] - rect.width / 2, position[1])
    screen.blit(label, position)

def draw_color_picker(selected_color):
    for i, color in enumerate(COLORS[:num_colors]):
        pygame.draw.circle(screen, color, COLOR_PICKER_POS[i], 45)
        if color == selected_color:
            pygame.draw.circle(screen, (0, 0, 0), COLOR_PICKER_POS[i], 45, 4)  # Highlight selected color

def draw_slots(current_guess, guesses):
    for i, guess in enumerate(guesses + [current_guess]):
        for j, color in enumerate(guess):
            pygame.draw.circle(screen, color, SLOT_POS[i][j], 45)
        for j in range(len(guess), 4):
            pygame.draw.circle(screen, (0, 0, 0), SLOT_POS[i][j], 45, 3)  # Empty slot

def draw_feedback(feedback):
    for i, fdbk in enumerate(feedback):
        x, y = SLOT_POS[i][0]
        x -= 150  # Position feedback to the left of the row
        for j, peg in enumerate(fdbk):
            color = (0, 0, 0) if peg == 'black' else (255, 255, 255)
            pygame.draw.circle(screen, color, (x + (j % 2) * 30, y + (j // 2) * 30), 15)

def get_feedback(guess):
    black_pegs = sum(1 for i in range(num_slots) if guess[i] == solution[i])
    whites = sum(min(guess.count(color), solution.count(color)) for color in set(guess)) - black_pegs
    return ['black'] * black_pegs + ['white'] * whites

def check_win():
    return current_guess == solution

def reset_game():
    global current_guess, guesses, feedback, solution
    current_guess = []
    guesses = []
    feedback = []
    solution = [random.choice(COLORS[:num_colors]) for _ in range(num_slots)]

def game_loop():
    global selected_color, current_guess, guesses, feedback
    reset_game()  # Initialize the game state

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i, pos in enumerate(COLOR_PICKER_POS):
                        if pygame.Rect(pos[0] - 45, pos[1] - 45, 90, 90).collidepoint(event.pos):
                            selected_color = COLORS[i]
                    for i, pos in enumerate(SLOT_POS[len(guesses)]):
                        if pygame.Rect(pos[0] - 45, pos[1] - 45, 90, 90).collidepoint(event.pos) and selected_color:
                            if len(current_guess) > i:
                                current_guess[i] = selected_color
                            else:
                                current_guess.append(selected_color)
                    if len(current_guess) == num_slots:
                        feedback.append(get_feedback(current_guess))
                        guesses.append(current_guess)
                        if check_win():
                            draw_text('Congratulations, You Won!', (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), font, (0, 128, 0), True)
                            pygame.display.update()
                            pygame.time.wait(5000)
                            reset_game()
                        current_guess = []

        screen.fill(BACKGROUND_COLOR)
        draw_text('Mastermind', (50, 20), font)
        draw_color_picker(selected_color)
        draw_slots(current_guess, guesses)
        draw_feedback(feedback)
        pygame.display.update()

game_loop()
