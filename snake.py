import pygame
import random

pygame.font.init()
pygame.mixer.init()
# Get the colors
BLACK = (0, 0, 0)
GRAY = (40, 40, 40)
GRAYER = (80, 80, 80)
RED = (136, 8, 8)
GREEN = (0, 255, 0)
WHITE = (255,255,255)
WHITER = (200, 200, 200)
YELLOW = (200, 200, 0)
BLUE = (0, 0, 52)

# Creates the window
WIDTH, HEIGHT = 909, 700
SNAKE_WIDTH, SNAKE_HEIGHT = 851, 598
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake!")

# Gets the square of the snake piece along with the dimensions
SNAKE_DIMENSIONS = SNAKE_WIDTH // 37
x_location, y_location = SNAKE_WIDTH / 2 - SNAKE_DIMENSIONS / 2 + 29, 328
SNAKE_SQUARE = [pygame.Rect(x_location, y_location, SNAKE_DIMENSIONS, SNAKE_DIMENSIONS)]
snake_list = [[]]
FPS = 60
keep_adding = False
game_window = pygame.Rect(29, 29, SNAKE_WIDTH, SNAKE_HEIGHT)

# Gets the font
SCORE_FONT = pygame.font.SysFont('comicsans', 40)
GAME_FONT = pygame.font.SysFont('comicsans', 35)
GAME_OVER_FONT = pygame.font.SysFont('comicsans', 25)

def snake_border(current_snake, playing):
    '''
    This function will draw the gray border around each individual snake piece.
    current_snake: This is the current square of the snake
    playing: A boolean value representing if the player is still playing or not
    '''
    current = 1
    for snake in current_snake:
        # Makes first snake block white if the player has lost
        if current == 1:
            first_snake = pygame.Rect(snake[0], snake[1],SNAKE_DIMENSIONS, SNAKE_DIMENSIONS)
        new_snake = pygame.Rect(snake[0], snake[1], SNAKE_DIMENSIONS, SNAKE_DIMENSIONS)
        pygame.draw.rect(WIN, GREEN, new_snake)
        if current == len(current_snake) and playing == False:
            pygame.draw.rect(WIN, WHITER, first_snake)
    # creates the border around each snake
        snake_border = pygame.Rect(snake[0], snake[1], SNAKE_DIMENSIONS, 1)
        pygame.draw.rect(WIN, GRAY, snake_border)
        snake_border = pygame.Rect(snake[0], snake[1] + SNAKE_DIMENSIONS - 1, SNAKE_DIMENSIONS, 1)
        pygame.draw.rect(WIN, GRAY, snake_border)
        snake_border = pygame.Rect(snake[0], snake[1], 1, SNAKE_DIMENSIONS)
        pygame.draw.rect(WIN, GRAY, snake_border)
        snake_border = pygame.Rect(snake[0] + SNAKE_DIMENSIONS - 1, snake[1], 1, SNAKE_DIMENSIONS)
        pygame.draw.rect(WIN, GRAY, snake_border)
        current += 1


def play_again():
    '''
    Creates the play again button and checks if the user would click it
    '''
    global x_location, y_location, SNAKE_SQUARE, snake_list
    # Creates the button
    play_again_button = pygame.Rect(350, 300, 180, 45)
    # Displays the button with the text
    pygame.draw.rect(WIN, GRAY, play_again_button)
    play_again_text = GAME_OVER_FONT.render("Play Again?", 1, WHITE)
    WIN.blit(play_again_text, (377, 303))
    x_pos, y_pos = pygame.mouse.get_pos()
    # Checks is the user clicked on the play again button and restarts the program if so
    if 350 <= x_pos <= 530 and 300 <= y_pos <= 345:
        pygame.draw.rect(WIN, GRAYER, play_again_button)
        WIN.blit(play_again_text, (377, 303))
        for event in pygame.event.get():
            # checks if play again is clicked on
            if event.type == pygame.MOUSEBUTTONDOWN:
                # restarts the program
                x_location, y_location = SNAKE_WIDTH / 2 - SNAKE_DIMENSIONS / 2 + 29, 328
                SNAKE_SQUARE = [pygame.Rect(x_location, y_location, SNAKE_DIMENSIONS, SNAKE_DIMENSIONS)]
                snake_list = [[]]
                main()

def draw_window(current_snake, food_rect, current_score, playing):
    '''
    This will draw out the snake board, the snake, the snake food and the text
    current_snake: This is the current rectangle of the snake
    food_rect: The square representing the food the player is going for
    current_score: An integer representing what the score is
    playing: A boolean value representing if the player is still playing or not
    '''
    WIN.fill(BLUE)
    pygame.draw.rect(WIN, BLACK, game_window)
    # checks through x, y locations of the multidimensional list
    snake_border(current_snake, playing)
    #Draws the food
    pygame.draw.rect(WIN, RED, food_rect)
    # Draws the text
    score_text = SCORE_FONT.render("Length: " + str(current_score), 1, WHITE)
    WIN.blit(score_text, (29, 630))
    high_score_text = SCORE_FONT.render("High Score: " + best_score(current_score), 1, WHITE)
    WIN.blit(high_score_text, (600, 630))

    if playing == False:
        # Adds the ending text
        new_score_text = GAME_FONT.render("Length: " + str(current_score), 1, WHITE)
        WIN.blit(new_score_text, (WIDTH / 2 - 90, 220))
        game_over_text = SCORE_FONT.render("Game Over!", 1, WHITE)
        WIN.blit(game_over_text, (WIDTH / 2 - 120, 150))
        keep_playing = True
        clock = pygame.time.Clock()
        # keeps running until user hits play again or the x
        while keep_playing:
            clock.tick(FPS)
            play_again()
            pygame.display.update()
            for event in pygame.event.get():
                # Checks if user quits
                if event.type == pygame.QUIT:
                    quit()
    pygame.display.update()

def snake_food(snake_locations):
    '''
    Creates the rectangle of the food square at a random location
    '''
    # gets the random location that is not on the snake
    x_food = random.randint(0, 36) * 23 + 29
    y_food = random.randint(0, 25) * 23 + 29
    location = [x_food, y_food]
    while location in snake_locations:
        # Changes the square to a correct dimension on the board based on the random numbers.
        x_food = random.randint(0, 36) * 23 + 29
        y_food = random.randint(0, 25) * 23 + 29
        location = [x_food, y_food]
    food_square = pygame.Rect(x_food, y_food, SNAKE_DIMENSIONS, SNAKE_DIMENSIONS)
    return food_square

def move_snake(direction, length_adding):
    '''
    This will move the snake across the board in the users inputted direction
    direction: This is a string representing which way the snake is moving
    is_food: A boolean representing if the snake collided with the food
    '''
    global x_location, y_location, snake_list, keep_adding
    # Sets the new location of the snake based on the current direction
    if direction == "left":
        x_location -= SNAKE_DIMENSIONS
    elif direction == "right":
        x_location += SNAKE_DIMENSIONS
    elif direction == "up":
        y_location -= SNAKE_DIMENSIONS
    elif direction == "down":
        y_location += SNAKE_DIMENSIONS
    # Adds a snake piece to the list
    if length_adding > 0:
        snake_list.append([x_location - SNAKE_DIMENSIONS, y_location])
        length_adding -= 1

    # Gets the list containing the correct positions for each snake piece
    newer_snake = [[x_location, y_location]]
    for i in range(0, len(snake_list) -1):
        newer_snake.append(snake_list[i])
    snake_list = newer_snake
    # Delays program slightly
    pygame.time.delay(80)
    return snake_list, length_adding

def game_over(snake_boxes):
    '''
    This will detect if the player has lost the game.
    snake_boxes: A list containing the location of each snake piece
    '''
    # Checks if first snake touches another snake
    for index in range(1, len(snake_boxes)):
        if snake_boxes[0] == snake_boxes[index]:
            return False
    # Checks if the snake touches the border
    snake_x, snake_y = snake_boxes[0][0], snake_boxes[0][1]
    # checks if the snake hits the border
    if snake_x == 6 or snake_x == 880 or snake_y == 6 or snake_y == 627:
        return False
    return True

def best_score(current_score):
    '''
    This function gets the high score and stores the information in a text file
    current_score: an integer representing the users current score
    '''
    # If user already had high_score file it simply reads it, if not it will create the file
    try:
        best_file = open("high_score.txt", "r")
    except:
        best_file = open("high_score.txt", "w")
        best_file.write("1")
        best_file.close()
        best_file = open("high_score.txt", "r")
    # Gets the current high score and converts it to an integer
    high_score = best_file.readline()
    high_score = int(high_score)
    best_file.close()
    # If the users score is greater than the high score,the high score is changed to the users score
    if current_score >= high_score:
        best_file = open("high_score.txt", "w")
        best_file.write(str(current_score))
        high_score = current_score
        best_file.close()
    return str(high_score)

def main():
    global SNAKE_SQUARE
    clock = pygame.time.Clock()
    running = True
    # Starts the snake off to be not moving
    direction = "blank"
    # Create the initial food square
    food_square = snake_food(SNAKE_SQUARE)
    added_length = 0
    score = 1
    current = 0
    while running:
        food_collide = False
        # stalls the program
        clock.tick(FPS)
        for event in pygame.event.get():
            # Checks if user quits
            if event.type == pygame.QUIT:
                running = False
            # Checks if user presses arrow keys
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and direction != "right" and current == 0:
                    direction = "left"
                    current += 1
                if (event.key == pygame.K_UP or event.key == pygame.K_w) and direction != "down" and current == 0:
                    direction = "up"
                    current += 1
                if (event.key == pygame.K_DOWN or event.key == pygame.K_s)and direction != "up" and current == 0:
                    direction = "down"
                    current += 1
                if (event.key == pygame.K_RIGHT or event.key == pygame.K_d)and direction != "left" and current == 0:
                    direction = "right"
                    current += 1
        # gets the head of the snake
        top_snake = pygame.Rect(SNAKE_SQUARE[0][0], SNAKE_SQUARE[0][1], SNAKE_DIMENSIONS, SNAKE_DIMENSIONS)
        if top_snake.colliderect(food_square):
            #changes location of the food
            food_square = snake_food(SNAKE_SQUARE)
            added_length = 4
            score += 4
        SNAKE_SQUARE, added_length = move_snake(direction, added_length)
        is_playing = game_over(SNAKE_SQUARE)
        # Changes the display of the window
        draw_window(SNAKE_SQUARE, food_square, score, is_playing)
        current = 0

main()