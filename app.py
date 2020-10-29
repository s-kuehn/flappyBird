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

pygame.init()

# Game variables
screenWidth = 576
screenHeight = 1024
gravity = 0.25
bird_movement = 0

# Set window size
screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()

# Load in background image and double it's size
bg_surface = pygame.image.load('sprites/background-day.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)

# Load in floor image and double it's size
floor_surface = pygame.image.load('sprites/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floorxPosition = 0

# Load in bird image and double it's size
bird_surface = pygame.image.load('sprites/bluebird-midflap.png').convert()
bird_surface = pygame.transform.scale2x(bird_surface)
# Add bird collision
bird_rect = bird_surface.get_rect(center = (100, screenHeight / 2))

pipe_surface = pygame.image.load('sprites/pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [400, 600, 800]

# Game loop
while True:
    # Look for events (ie: button clicks)
    for event in pygame.event.get():
        # Quit game on exit button
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= 12
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
    
    # Speed of the floor movement
    floorxPosition -= 2

    # Place background image
    screen.blit(bg_surface, (0, 0))

    # Add gravity to bird
    bird_movement += gravity
    bird_rect.centery += bird_movement

    screen.blit(bird_surface, bird_rect)

    # Move all pipes
    pipe_list = move_pipes(pipe_list)
    draw_pipes(pipe_list)

    # Draw and animate floor
    drawFloor()
    if floorxPosition <= -screenWidth:
        floorxPosition = 0

    # Refresh game
    pygame.display.update()
    clock.tick(120)