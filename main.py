import pygame, random
from pygame import mixer

pygame.init()

# Creating Some Display Variables
width = 288
height = 512
screen = pygame.display.set_mode((width, height))
icon = pygame.image.load("models/icon.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Flappy Bird")
running = True
clock = pygame.time.Clock()
game_active = True
show_message_screen = True

# Creating Some Sound Variables
die_sound = pygame.mixer.Sound('sound/die.wav')
hit_sound = pygame.mixer.Sound('sound/hit.wav')
point_sound = pygame.mixer.Sound('sound/point.wav')
swoosh_sound = pygame.mixer.Sound('sound/swoosh.wav')
wing_sound = pygame.mixer.Sound('sound/wing.wav')

######### The Game making process starts from here #########

# Randomizing the Background before importing
bg_image_list = [
    "models/background-day.png",
    "models/background-night.png"
]

bg_image = random.choice(bg_image_list)

# drawing the Background on the Screen
background = pygame.image.load(bg_image).convert_alpha()
background_x = 0
background_y = 0

# Creating the Function to draw the Background
def draw_background():
    screen.blit(background, (background_x, background_y))
    
# drawing the Base on the Screen
base = pygame.image.load("models/base.png").convert_alpha()
base_x = 0
base_y = 430
# Base movement Variables
base_x_move = 1

# Creating the Function to draw the Base
def draw_base():
    global base_x
    screen.blit(base, (base_x, base_y))
    base_x -= base_x_move
    if base_x <= -50:
        base_x = 0

# Randomizing the Birds before Importing
all_birds = [
    ["models/bluebird-downflap.png","models/bluebird-midflap.png","models/bluebird-upflap.png"],
    ["models/redbird-downflap.png","models/redbird-midflap.png","models/redbird-upflap.png"],
    ["models/yellowbird-downflap.png","models/yellowbird-midflap.png","models/yellowbird-upflap.png"],
]

bird_set = random.choice(all_birds)

# Creating all the Bird frames for Animation
bird_downflap = pygame.image.load(bird_set[0]).convert_alpha()
bird_midflap = pygame.image.load(bird_set[1]).convert_alpha()
bird_upflap = pygame.image.load(bird_set[2]).convert_alpha()

# Adding all the Bird frames into a List to loop
bird_frames = [
    bird_downflap,
    bird_midflap,
    bird_upflap
]

frame_index = 0

# Creating a Userevent to Loop the Frames
ANIMATION = pygame.USEREVENT + 1
pygame.time.set_timer(ANIMATION, 100)

# Importing the Bird on the Screen
bird = bird_frames[frame_index]
bird_y_move = 0
gravity = 0.25
jump = -9
# Drawing the Bird inside a Rectangle
bird_rect = bird.get_rect(center = (50, 256))

# Creating the Function to Add the Animation
def add_animation():
    new_bird = bird_frames[frame_index]
    new_bird_rect = new_bird.get_rect(center = (50, bird_rect.centery))

    return new_bird, new_bird_rect

# Creating the Function to Rotate the Bird
def bird_rotate(bird):
    new_bird = pygame.transform.rotate(bird, -(bird_y_move * 3))
    return new_bird

# Creating a Function to draw the Bird
def draw_bird():
    global gravity
    global bird_y_move
    rotated_bird = bird_rotate(bird)
    screen.blit(rotated_bird, bird_rect)
    
    # Adding Gravity to the Bird
    bird_y_move += gravity
    bird_rect.centery += bird_y_move
    
    # Setting up A Boundary for the Bird
    if bird_rect.centery >= 420:
        bird_rect.centery = 420
    elif bird_rect.centery <= 12:
        bird_rect.centery = 12
        
# Randomizing the Pipes before importing
pipe_colour_list = [
    "models/pipe-green.png",
    "models/pipe-red.png"
]

random_pipe = random.choice(pipe_colour_list)

# Importing the Pipes
pipe = pygame.image.load(random_pipe).convert_alpha()
pipe_x_move = -2.5
# Creating the Userevent to Spawn the Pipe
SPAWN_PIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWN_PIPE, 1200)

# Creating an Empty list for the Pipe to Loop and Store data
pipe_list = []

# Creating a Function to Create the Pipes
def create_pipe():
    # Randomizing the Y axis of the Pipes
    pipe_y_list = [230, 260, 290, 310, 340, 370, 400]
    pipe_y = random.choice(pipe_y_list)

    # Creating the Top and the   Bottom pipe
    bottom_pipe_rect = pipe.get_rect(midtop = (330, pipe_y))
    top_pipe_rect = pipe.get_rect(midbottom = (330, pipe_y - 200))

    return bottom_pipe_rect, top_pipe_rect

# Creating the Function to move the Pipe 
def move_pipe(pipes):
    global score_value
    global high_score_value
    for each_pipe in pipes:
        each_pipe.centerx += pipe_x_move
        if each_pipe.centerx <= 25 and each_pipe.centerx >= 24:
            point_sound.play()
            score_value += 0.5
            if score_value > high_score_value:
                high_score_value = score_value
    return pipes
        
# Creating the Function to Draw the Pipe
def draw_pipe(pipes):
    for each_pipe in pipes:
        if each_pipe.bottom >= 512:
            screen.blit(pipe, each_pipe)
        else:
            flipped_pipe = pygame.transform.rotate(pipe, 180)
            screen.blit(flipped_pipe, each_pipe)
            
# Creating the Function to add the Collision
def add_collision(pipes):
    for each_pipe in pipes:
        if bird_rect.colliderect(each_pipe):
            return False
        elif bird_rect.centery >= 420:
            return False
    return True

# Importing the Game over Text
game_over_text = pygame.image.load("models/gameover.png").convert_alpha()
game_over_text_x = 50
game_over_text_y = 200

# Creating a function to Add the Game over Text
def draw_game_over_text():
    screen.blit(game_over_text, (game_over_text_x, game_over_text_y))

# Importing the Message Screen 
message_screen = pygame.image.load("models/message.png").convert_alpha()
message_screen_x = 50
message_screen_y = 100

# Creating the Function to Add the message on the Screen
def draw_message_screen():
    screen.blit(message_screen, (message_screen_x, message_screen_y))
    
# Creating the Score Related Variables
font = pygame.font.Font("font/font.ttf", 25)
WHITE = (255, 255, 255)
score_value = 0
you_scored_value = 0
high_score_value = 0

# Creating the Function to Add the Current Score on the Screen
def draw_score():
    score = font.render("Score : " + str(int(score_value)), True, WHITE)
    score_rect = score.get_rect(center = (140, 30))
    screen.blit(score, score_rect)
    
# Creating the Your score Function
def draw_you_scored():
    you_scored = font.render("You Scored : " + str(int(you_scored_value)), True, WHITE)
    you_scored_rect = you_scored.get_rect(center = (140, 30))
    screen.blit(you_scored, you_scored_rect)
    
# Creating the High score Function
def draw_high_score():
    high_score = font.render("High Score : " + str(int(high_score_value)), True, WHITE)
    high_score_rect = high_score.get_rect(center = (140, 400))
    screen.blit(high_score, high_score_rect)
    


# Creating the Main loop for the Game
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Creating the Movement Keys
        if event.type == pygame.KEYDOWN:
            # Creating the Game starting Key
            if event.key == pygame.K_SPACE and show_message_screen == True:
                show_message_screen = False
                pipe_list.clear()
                bird_y_move = 0
                bird_rect = bird.get_rect(center = (50, 256))
            # Creating the Bird Jumping Key
            if event.key == pygame.K_SPACE and game_active == True:
                wing_sound.play()
                bird_y_move = 0
                bird_y_move += jump
            # Creating the Game restart key
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_y_move = 0
                bird_rect = bird.get_rect(center = (50, 100))

        # Initializing the Userevent to Spawn the Pipes
        if event.type == SPAWN_PIPE:
            pipe_list.extend(create_pipe())
        # Using the Animation Userevent to Update the Frames
        if event.type == ANIMATION:
            if frame_index < 2:
                frame_index += 1
            else:
                frame_index = 0

            bird, bird_rect = add_animation()
    
    # Calling the Background Function            
    draw_background()
    
    # Adding the Message Screen on startup
    if show_message_screen == True:
        draw_message_screen()
    else: 
        # Making Sure that the Game is Active
        game_active = add_collision(pipe_list)
        # Checking if the Game is over or Not
        if game_active == True:
            # Updating the Pipe list continiously
            pipe_list = move_pipe(pipe_list)
            
            # Calling the Pipe function
            draw_pipe(pipe_list)
            
            # Calling the Bird function
            draw_bird()
            
            # Callling the Score Function
            draw_score()
            
            # Adding the Score Value to Your Score Function
            you_scored_value = score_value
        else:
            # Resetting the Score
            score_value = 0
            
            # Calling the Your Score Function
            draw_you_scored()
            
            # Calling the High Score Function
            draw_high_score()
            
            # Adding the Game Over Text
            draw_game_over_text()
    
    # Calling the Base Function
    draw_base()
            
    # Updating the Screen Continiously
    pygame.display.update()
    
    # Keeping a Constant Framerate
    clock.tick(120)