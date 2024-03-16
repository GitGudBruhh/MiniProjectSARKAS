import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen dimensions and settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BACKGROUND_COLOR = (200, 200, 200)
FONT_COLOR = (0, 0, 0)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Mastermind')

# Define colors
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 140, 0), (255, 20, 147), (0, 255, 255), (128, 0, 128)]
COLOR_PICKER_POS = [(50 + i * 50, 550) for i in range(len(COLORS))]
SLOT_POS = [[(150 + j * 50, 50 + i * 50) for j in range(4)] for i in range(10)]

# Game variables
num_slots = 4
num_colors = 6
selected_color = None
current_guess = []
guesses = []
feedback = []
solution = [random.choice(COLORS[:num_colors]) for _ in range(num_slots)]

# Fonts
font = pygame.font.SysFont(None, 36)

def draw_text(text, position):
    label = font.render(text, True, FONT_COLOR)
    screen.blit(label, position)

def draw_color_picker(selected_color):
    for i, color in enumerate(COLORS[:num_colors]):
        pygame.draw.circle(screen, color, COLOR_PICKER_POS[i], 20)
        if color == selected_color:
            pygame.draw.circle(screen, (0, 0, 0), COLOR_PICKER_POS[i], 20, 2)  # Draw a border if selected

def draw_slots():
    for i, guess in enumerate(guesses):
        for j, color in enumerate(guess):
            pygame.draw.circle(screen, color, SLOT_POS[i][j], 20)
    for i, color in enumerate(current_guess):
        pygame.draw.circle(screen, color, SLOT_POS[len(guesses)][i], 20)
    for i in range(num_slots):
        pygame.draw.circle(screen, (0, 0, 0), SLOT_POS[len(guesses)][i], 20, 1)  # Draw empty slots for the current guess

def draw_feedback():
    for i, fdbk in enumerate(feedback):
        x, y = SLOT_POS[i][num_slots - 1]
        x += 60
        for j, peg in enumerate(fdbk):
            color = (0, 0, 0) if peg == 'black' else (255, 255, 255)
            pygame.draw.circle(screen, color, (x + (j % 2) * 15, y + (j // 2) * 15), 7)

def get_feedback(guess):
    black_pegs = sum([1 for i in range(num_slots) if guess[i] == solution[i]])
    white_pegs = sum([min(guess.count(color), solution.count(color)) for color in set(guess)]) - black_pegs
    return ['black'] * black_pegs + ['white'] * white_pegs

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

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i, pos in enumerate(COLOR_PICKER_POS):
                        if pygame.Rect(pos[0] - 20, pos[1] - 20, 40, 40).collidepoint(event.pos):
                            selected_color = COLORS[i]
                    for i, pos in enumerate(SLOT_POS[len(guesses)]):
                        if pygame.Rect(pos[0] - 20, pos[1] - 20, 40, 40).collidepoint(event.pos) and selected_color:
                            if len(current_guess) > i:
                                current_guess[i] = selected_color
                            else:
                                current_guess.append(selected_color)
                    if len(current_guess) == num_slots:
                        feedback.append(get_feedback(current_guess))
                        guesses.append(current_guess)
                        if check_win():
                            draw_text('You Won!', (350, 300))
                            pygame.display.update()
                            pygame.time.wait(3000)
                            reset_game()
                        current_guess = []

        screen.fill(BACKGROUND_COLOR)
        draw_text('Mastermind', (350, 10))
        draw_color_picker(selected_color)
        draw_slots()
        draw_feedback()
        pygame.display.update()

game_loop()
