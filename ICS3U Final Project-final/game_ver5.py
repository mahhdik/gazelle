# Import all necessary libraries and functions
import pygame
import threading
import random
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Initialize pygame
pygame.init()

# Create screen and dimensions using display.set_mode(dimensions)
screen_width = 500
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
# Name the window
pygame.display.set_caption("All Aboard")



def play_music():
    pygame.mixer.init()  # Initialize the pygame mixer
    pygame.mixer.music.load("C:\\Users\\mahhd\\Downloads\\ICS3U Final Project\\sea.mp3")  # Load the audio file
    pygame.mixer.music.play(-1)


music_thread = threading.Thread(target=play_music, daemon=True)
music_thread.start()







# Create images that will be used during the game
bg = pygame.image.load("waterbg1.png")
boat_img = pygame.image.load("boat1.png")
rock_img_unscaled = pygame.image.load("rock1.png")
rock_img = pygame.transform.scale(rock_img_unscaled, (100, 100))
litter_img_unscaled = pygame.image.load("litter.png")
litter_img = pygame.transform.scale(litter_img_unscaled, (150, 75))
dolphin_img_unscaled = pygame.image.load("dolphin.png")
dolphin_img = pygame.transform.scale(dolphin_img_unscaled, (180, 90))
obstacle_img = [rock_img, litter_img, dolphin_img]

# Defines the fonts for any texts to be used in the game
font = pygame.font.SysFont("poppins", 30)
gameover_font = pygame.font.SysFont("poppins", 75)

# Create a class for the player instance
class Player:
    # Define variables for the x and y position of the player on the screen
    x_pos = 200
    y_pos = 400

    # Initialize the attributes of the player class
    def __init__(self):
        self.image = boat_img
        self.player_rect = self.image.get_rect()
        self.player_rect.x = self.x_pos
        self.player_rect.y = self.y_pos
        self.vel = 5
        self.left = False
        self.right = False
        self.lives = 3

    # Define a function for the movement of the player so that the player moves left by reducing the x position value and the player moves right by increasing the x position value.
    # Change user inputs and keybinding:
    # The player will move away from obstacles when the answer to a question is correct
    # The player will collide with the obstacle when the answer is wrong
    def update(self, user_input):
        if user_input[pygame.K_LEFT]:
            self.player_rect.x -= self.vel
            self.left = True
            self.right = False
            self.image = pygame.transform.flip(boat_img, True, False)
        elif user_input[pygame.K_RIGHT]:
            self.player_rect.x += self.vel
            self.left = False
            self.right = True
            self.image = boat_img
        
    # Define a function to draw the player to the screen based on the x and y position and image arguments in the blit function. 
    def draw(self, screen):
        screen.blit(self.image, (self.player_rect.x, self.player_rect.y))

class Obstacle():
    # Initialize the attributes of the obstacle class
    def __init__(self, x_pos, y_pos):
        self.image = random.choice(obstacle_img)
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos

    # Define a function for the movement of the obstacle so that the obstacle moves down after it spawns by increasing its y position value by a standard speed variable.
    def update(self):
        self.rect.y += game_speed
        if self.rect.top > screen_height: # If the top of the obstacle image moves off screen, it will be removed from the list (obstacles) that contains all instances of obstacles.
            obstacles.pop()
    
    # Define a function to draw the obstacle to the screen based on the x and y position and image arguments in the blit function. 
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

# Create a function to increase the difficulty of the game by increasing the speed at which obstacles approach the player by a rate of the score, using the game_speed variable
def difficulty():
    global score
    game_speed

    if score >= 10:
        game_speed *= score//20

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

# Create a function to run the game
def game():
    global obstacles, game_speed, y_pos, x_pos_bg, y_pos_bg
    x_pos_bg = 0
    y_pos_bg = 0

    def background():
        global x_pos_bg, y_pos_bg
        image_height = bg.get_height()
        screen.blit(bg, (x_pos_bg, y_pos_bg)) # display first image at (0,0)
        screen.blit(bg, (x_pos_bg, y_pos_bg - image_height)) #display next image at (0, 600 + y position)
        if y_pos_bg >= image_height: # if y posiiton is less than -600
            screen.blit(bg, (x_pos_bg, y_pos_bg - image_height)) #display next image at (0, 600 + y posiiton)
            y_pos_bg = 0 # set y position to zero
        y_pos_bg += game_speed # reduce y posiiton by game speed to adjust scrolling speed by the game speed variable


    running = True
    clock = pygame.time.Clock()
    game_speed = 2
    # x_pos = random.choice((75, 310))
    y_pos = 2
    
    #Initialize the player and obstacle
    player = Player()
    obstacle = Obstacle(random.choice((75, 310)), y_pos)

    obstacles = []

    while running:
        # difficulty()

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                running = False

        # screen.blit(bg, (0, 0))
        background()

        user_input = pygame.key.get_pressed()

        # The following functions draw the player on the screen and update the player when it moves
        player.draw(screen)
        player.update(user_input) # change arg to answer variable once ready

        # The following functions draw the obstacle on the screen and update the obstacle when it moves
        obstacle.draw(screen)
        obstacle.update()
        
        # Adds text showing the player how many lives they have remaining
        lives_text = font.render("Lives: " + str(player.lives), 1, (0,0,0))
        screen.blit(lives_text, (5,5))

        # Ends the game if the player reaches 0 lives
        if player.lives == 0:
            gameover() # Launches gameover screen

        # If and For Loops: Adds obstacle to the empty obstacles list and respawns obstacles when there are none. It also draws collision between player and obstacle.
        if len(obstacles) == 0:
            obstacles.append(Obstacle(random.choice((75, 310)), y_pos))

        for obstacle in obstacles:         
            obstacle.draw(screen)
            obstacle.update()
            if player.player_rect.colliderect(obstacle.rect):
                if player.lives > 0:
                    player.lives -= 1
                    obstacles.pop(obstacles.index(obstacle))
                    print(player.lives)
                else:
                    obstacles.pop(obstacles.index(obstacle))
                    pygame.mixer.music.stop()
                    print("GAME END")
                    break

        clock.tick(60) # Set FPS
        pygame.display.update()

game() # Call the game function so the program runs.