# Import all necessary libraries and functions
import pygame
import threading
import random
from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    QUIT,
)

# Initialize pygame
pygame.init()

# Create variables containing the dimensions of the game window: screen_width and screen_height.
screen_width = 500
screen_height = 600
# Create the game window using display.set_mode(dimensions) and assign the window to the variable screen.
screen = pygame.display.set_mode((screen_width, screen_height))
# Name the window according to the name of the game.
pygame.display.set_caption("All Aboard")

def play_music():
    pygame.mixer.init()  # Initialize the pygame mixer
    pygame.mixer.music.load("sophiasshop.mp3")  # Load the audio file
    pygame.mixer.music.play(-1)


music_thread = threading.Thread(target=play_music, daemon=True)
music_thread.start()


# Load images that will be displayed during the game using the function pygame.image.load("image path").
# Assign these images to variables so they can be called.
# Scale down images with dimensions that are too large for the User Interface (UI) using the pygame.transform.scale() function and assign the scaled image to a new variable.
bg = pygame.image.load("waterbg1.png")
boat_img = pygame.image.load("boat1.png")
rock_img_unscaled = pygame.image.load("rock1.png")
rock_img = pygame.transform.scale(rock_img_unscaled, (100, 100))
litter_img_unscaled = pygame.image.load("litter.png")
litter_img = pygame.transform.scale(litter_img_unscaled, (150, 75))
dolphin_img_unscaled = pygame.image.load("dolphin.png")
dolphin_img = pygame.transform.scale(dolphin_img_unscaled, (180, 80))
# Create a list containing all images necessary for obstacles.
obstacle_img = [rock_img, litter_img, dolphin_img]

# Change the window icon to the boat image.
pygame.display.set_icon(boat_img)

# Defines the fonts for any texts to be used in the game
font = pygame.font.SysFont("poppins", 30)
gameover_font = pygame.font.SysFont("poppins", 75)

# Create a variable to hold the player's score
score = 0

# Player class: Create a class for the player instance that can be operated by the player during the game.
class Player:
    # Define variables for the x and y position of the player on the screen
    x_pos = 200
    y_pos = 400

    # Initialize the attributes of the player class.
    def __init__(self):
        self.image = boat_img # Assign the player class an image.
        self.player_rect = self.image.get_rect() # Map the player image dimesions (with the get_rect() function) for the player hitbox.
        # Assign the player x and y positions using the x_pos and y_pos variables.
        self.player_rect.x = self.x_pos
        self.player_rect.y = self.y_pos
        # Create left, right, and velocity variables for player movement.
        self.vel = 5
        self.left = False
        self.right = False
        self.lives = 3

    # Define a function for the movement of the player.
    def update(self, user_input):
        # If Statement: The player moves left when the left keybind is pressed by reducing the x position value and only setting the left attribute to true.
        if user_input[pygame.K_LEFT] and self.player_rect.x > -1: # Create another condition within the if statement so that the player cannot move outside of the game screen.
            self.player_rect.x -= self.vel
            self.left = True
            self.right = False
            self.image = pygame.transform.flip(boat_img, True, False) # pygame.transform.flip(): Rotates the image of the player so that the player image faces the direction of the movement. 
        # The player moves right when the right keybind is pressed by increasing the x position value and only setting the right attribute to true.
        elif user_input[pygame.K_RIGHT] and self.player_rect.x < screen_width - 125:  # Create another condition within the if statement so that the player cannot move outside of the game screen.
            self.player_rect.x += self.vel
            self.left = False
            self.right = True
            self.image = boat_img # Sets the image of the player to the original player image when the right keybind is pressed to that the image faces the direction of the movement.
        
    # Define a function to draw the player to the screen based on the x and y position and image arguments in the blit function. 
    def draw(self, screen):
        screen.blit(self.image, (self.player_rect.x, self.player_rect.y))

# Obstacle class: Create a class for the obstacle instances during the game.
class Obstacle():
    # Initialize the attributes of the obstacle class
    def __init__(self, x_pos, y_pos):
        self.image = random.choice(obstacle_img) # Assign the obstacle class a random image in the obstacle_img list by using the random.choice() function.
        self.rect = self.image.get_rect() # Map the obstacle image dimesions (with the get_rect() function) for the obstacle hitbox.
        # Assign the obstacle x and y positions using the x_pos and y_pos arguments that will be entered per obstacle instance.
        self.rect.x = x_pos
        self.rect.y = y_pos

    # Define a function for the movement of the obstacle so that the obstacle moves down after it spawns by increasing its y position value by the game_speed variable.
    def update(self):
        self.rect.y += game_speed
        if self.rect.top > screen_height: # If the top of the obstacle image moves off screen, it will be removed from the obstacles list that contains all instances of obstacles.
            obstacles.pop()
            global score
            score += 1
    
    # Define a function to draw the obstacle to the screen based on the x and y position and image arguments in the blit function. 
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

# Difficulty function: Increases the difficulty of the game by increasing the speed at which obstacles approach the player, using the game_speed variable
def difficulty():
    global score, game_speed # Make score and game_speed global variables so that they can be referenced within the difficulty() function.

    # If Statement: Compares the player's score to an integer value to increase speed at given intervals by changing the game_speed variable to a higher value.
    if score == 10:
        game_speed = 2.5
    elif score == 20:
        game_speed = 3
    elif score == 50:
        game_speed = 3.3
    elif score >= 50:
        game_speed = 3.5
    
# Create a function that will run when the player runs out of lives (game over screen)
def gameover():
    running = True
    while running:
        screen.blit(bg, (0,0))
        gameover_text = gameover_font.render("GAME OVER", 1, (255,0,0))
        screen.blit(gameover_text, (93,250))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

# Game function: Runs the gameplay involving the player class, obstacle class, background, and other components of the gameplay.
def game():
    global obstacles, game_speed, y_pos, x_pos_bg, y_pos_bg # Make obstacles, game_speed, y_pos, x_pos_bg, and y_pos_bg global variables so that they can be referenced anywhere within the gmae() function.
    # Define the variables that will be used within the game() function.
    # Define the x and y position of the background to zero for the background() function scrolling background.
    x_pos_bg = 0
    y_pos_bg = 0
    # Define a variable, running, and set it to True so that the game runs while running = True in the game loop.
    running = True
    # Define a clock variable to track time in the game.
    clock = pygame.time.Clock()
    # Define the game_speed variable to control the speed at which the background and objects move.
    game_speed = 2
    # Define the y_pos variable to contain the y position of the obstacles once spawned.
    y_pos = 2
    
    # Create the background function so that the background can scroll by the value of the game_speed variable.
    def background():
        global x_pos_bg, y_pos_bg # Make x_pos_bg and y_pos_bg global variables so they can be referenced within the background() function.
        image_height = bg.get_height() # Set the image_height variable to the value of the height of the background image using the get_height() function.
        screen.blit(bg, (x_pos_bg, y_pos_bg)) # Display the first background image at (0,0).
        screen.blit(bg, (x_pos_bg, y_pos_bg - image_height)) # Display the next background image at (0, 600 - the height of the background image).
        # If Statement: Displays the scrolling background by displaying another background image when the last image has moved off the screen.
        if y_pos_bg >= image_height:
            screen.blit(bg, (x_pos_bg, y_pos_bg - image_height))
            y_pos_bg = 0 # Set y position back to zero.
        y_pos_bg += game_speed # Increase the y position of the background by the game speed to adjust scrolling speed by the game_speed variable.
    
    # Create a player instance
    player = Player()
    # Create an obstacle instance with the y position of the y_pos variable and a random x position (at x = 75 or 300 pixels)
    obstacle = Obstacle(random.choice((75, 300)), y_pos)

    # Create an empty list to temporarily store obstacle instances.
    obstacles = []

    # While Loop: Game loop that runs while running == True so that the game script can be executed accoridng to the code inside the game loop.
    while running:

        # For Loop: Runs the pygame.event.get() function to check for any events.
        for event in pygame.event.get():
            
            # If Statement: Checks if the event.type is quit
            if event.type == pygame.QUIT:
                running = False # End the game and close the window if the event type is quit and set the running variable to false

        # Call the background function to implement the scrolling background.
        background()
        # Call the difficulty function to implement increasing difficulty into the game.
        difficulty()

        # Store user inputs in the user_input variable using the pygame.key.get_pressed() function to that keybinds can be used for in-game movements. 
        user_input = pygame.key.get_pressed()

        # The following functions draw the player on the screen and update the player's position when the player moves
        player.draw(screen)
        player.update(user_input) # change arg to answer variable once ready

        # The following functions draw the obstacle on the screen and update the obstacle's position when it moves
        obstacle.draw(screen)
        obstacle.update()
        
        # Adds text showing the player how many lives they have remaining
        lives_text = font.render("Lives: " + str(player.lives), 1, (0,0,0))
        screen.blit(lives_text, (5,5))

        # Adds text showing the player their current score
        score_text = font.render("Score: " + str(score), 1, (0,0,0))
        screen.blit(score_text, (5,30))

        # Ends the game if the player reaches 0 lives
        if player.lives == 0:
            pygame.mixer.music.stop()
            gameover() # Launches gameover screen

        # If Statement: Adds obstacle to the empty obstacles list and respawns obstacles when there are no obstacles.
        if len(obstacles) == 0:
            obstacles.append(Obstacle(random.choice((75, 300)), y_pos))
        
        # For Loop: Draws obstacles in the obstacles list to the screen and updates its position on the screen as it moves down.
        for obstacle in obstacles:         
            obstacle.draw(screen)
            obstacle.update()
            # If Statement: Draws collision between the player and obstacle so that the player loses a life once colliding with the obstacle. Removes the obstacle from the obstacles list if the player collides with the obstacle.
            if player.player_rect.colliderect(obstacle.rect):
                if player.lives > 0:
                    player.lives -= 1
                    obstacles.pop(obstacles.index(obstacle))
                    print(player.lives)
                else:
                    obstacles.pop(obstacles.index(obstacle))
                    print("GAME END")

        clock.tick(60) # Sets the FPS so that the obstacles, player, and background move smoothly down the screen.
        pygame.display.update() # Updates the screen while the game runs.

game() # Call the game function so the program runs.