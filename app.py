import pygame, sys, random

def drawFloor():
    screen.blit(floor_surface, (floorxPosition, 900))
    screen.blit(floor_surface, (floorxPosition + screenWidth, 900))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (screenWidth+200, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (screenWidth+200, random_pipe_pos-300))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False
    if bird_rect.top <= -100 or bird_rect.bottom >= 900:
        death_sound.play()
        return False
    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
    return new_bird, new_bird_rect

def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (288, 100))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {str(int(score))}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (288, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'HighScore: {str(int(highScore))}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center = (288, 850))
        screen.blit(high_score_surface, high_score_rect)

def update_score(score, highScore):
    if score > highScore:
        highScore = score
    return highScore

pygame.mixer.pre_init()
pygame.init()

# Game variables
screenWidth = 576
screenHeight = 1024
gravity = 0.25
bird_movement = 0
gameActive = True
score = 0
highScore = 0

# Set window size
screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf', 40)

# Load in background image and double it's size
bg_surface = pygame.image.load('sprites/background-day.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)

# Load in floor image and double it's size
floor_surface = pygame.image.load('sprites/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floorxPosition = 0

# Load in bird image and double it's size
bird_downflap = pygame.transform.scale2x(pygame.image.load('sprites/bluebird-downflap.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load('sprites/bluebird-midflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load('sprites/bluebird-upflap.png').convert_alpha())
bird_frames = [bird_downflap,bird_midflap,bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (100, screenHeight / 2))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP,200)

pipe_surface = pygame.image.load('sprites/pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [400, 600, 800]

SCOREUP = pygame.USEREVENT + 2
pygame.time.set_timer(SCOREUP, 1600)

game_over_surface = pygame.image.load('sprites/message.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center = (screenWidth/2,screenHeight/2))

flap_sound = pygame.mixer.Sound('audio/wing.wav')
death_sound = pygame.mixer.Sound('audio/hit.wav')
score_sound = pygame.mixer.Sound('audio/point.wav')
score_sound_countdown = 100

# Game loop
while True:
    # Look for events (ie: button clicks)
    for event in pygame.event.get():
        # Quit game on exit button
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and gameActive:
                bird_movement = 0
                bird_movement -= 12
                flap_sound.play()
            if event.key == pygame.K_SPACE and gameActive == False:
                gameActive = True
                pipe_list.clear()
                bird_rect.center = (100, 512)
                bird_movement = 0
                bird_movement -= 12
                score = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        if event.type == SCOREUP and gameActive == True:
            score_sound.play()
            score += 1

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird_surface, bird_rect = bird_animation()
    
    # Speed of the floor movement
    floorxPosition -= 2

    # Place background image
    screen.blit(bg_surface, (0, 0))
    if gameActive:
        # Add gravity to bird
        bird_movement += gravity
        bird_rect.centery += bird_movement

        rotated_bird = rotate_bird(bird_surface)

        screen.blit(rotated_bird, bird_rect)
        gameActive = check_collision(pipe_list)

        # Move all pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        score_display('main_game')
    else:
        highScore = update_score(score, highScore)
        score_display('game_over')
        screen.blit(game_over_surface, game_over_rect)

    # Draw and animate floor
    drawFloor()
    if floorxPosition <= -screenWidth:
        floorxPosition = 0

    # Refresh game
    pygame.display.update()
    clock.tick(120)