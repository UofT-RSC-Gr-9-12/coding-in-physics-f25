
import pygame
import math
import random
import os
import serial

# TODO: UNCOMMENT WHEN INTEGRATING ARDUINO
# ARDUINO_PORT = '/dev/cu.usbmodem11401'  # Update this to your Arduino port
# ser = serial.Serial(ARDUINO_PORT, 9600, timeout=1)

# pygame constants
ANIMATION_SPEED = 10  # frames per second for explosion animation
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FRAMES_PER_SECOND = 60

# simulation constants
STARTING_BALLOON_RADIUS = 50
STARTING_TEMPERATURE = 50  # Kelvin
STARTING_PARTICLES = 100
MAX_BALLOON_RADIUS = min(SCREEN_WIDTH, SCREEN_HEIGHT) / 2 - 20
MAX_PRESSURE = 500

# physical constants
WATER_BOILING_POINT = 373  # Kelvin
MASS_OF_O2 = 31.989829239
N_A = 6.022e23
R = 8.314

num_particles = STARTING_PARTICLES
temperature = STARTING_TEMPERATURE

# balloon dimensions
balloon_rad = STARTING_BALLOON_RADIUS
balloon_center_x = SCREEN_WIDTH / 2
balloon_center_y = SCREEN_HEIGHT / 2

# volume but we use area formula instead
volume = math.pi * (balloon_rad ** 2)
m = MASS_OF_O2  # mass of particle (assume O2)
current_pressure = 0

# Particle motion
particle_positions = []  # stores array of (x-positions, y-position)
particle_velocities = []  # stores array of (x-velocity, y-velocity)


def set_particle_positions():
    """Initialize particles randomly inside the balloon
    """
    particle_positions.clear()

    for i in range(num_particles):

        # using pythagoran theorem/distance to set particle position within circle balloon

        # padding = 8 since drawing line width = 5 + 3 padding
        random_x = random.uniform(-balloon_rad + 8, balloon_rad - 8)
        random_y = random.uniform(-balloon_rad + 8, balloon_rad - 8)

        # Calculate distance from center using Pythagoram thm
        distance = math.sqrt(random_x**2 + random_y**2)

        # If too far from center, scale it back to fit inside circle
        if distance > balloon_rad - 8:
            scale = (balloon_rad - 8) / distance
            random_x *= scale
            random_y *= scale

        # finally, position = center + offset
        pos_x = balloon_center_x + random_x
        pos_y = balloon_center_y + random_y

        particle_positions.append(pygame.Vector2(pos_x, pos_y))


def calculate_particle_speed(temp):
    """ Calculate particle speed based on temperature
        using Kinetic Molecular Theory of Ideal Gases
    v_rms = sqrt(3RT/M)
    """

    # TODO (Week 1)

    M = m / 1000  # 0.031989... kg/mol
    v_rms = math.sqrt(3 * R * temp / M)

    # Scaling down for game (this would be ~500 m/s in reality, too fast for pygame!)
    scale_factor = 0.05
    return v_rms * scale_factor


def set_particle_velocities(temp):
    """Initialize particle velocities based on Temperature
    """

    # TODO (Week 1)

    particle_velocities.clear()
    speed = calculate_particle_speed(temp)

    for i in range(num_particles):
        v = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))

        if v.length() > 0:
            v.scale_to_length(speed)
        else:
            v = pygame.Vector2(speed, 0)

        particle_velocities.append(v)


def draw_particles():
    colour_scale = int(
        min(temperature, WATER_BOILING_POINT) / WATER_BOILING_POINT * 255)
    particle_colour = (colour_scale, 100, 255 - colour_scale)

    # TODO (Week 1)
    for pos in particle_positions:
        pygame.draw.circle(screen, particle_colour,(int(pos.x), int(pos.y)), 3)


# *************** STEP 3 ******************

# particle movements
def update_particle_movement(dt):
    """Update all particle positions and handle collisions"""
    # TODO (Week 2)
    
    # for each particle:
        # 1. update displacement with velocity and time (hint: d = v*t)
        
        # 2. Check circular boundary by creating vector from balloon centre to partlce
        
        # 3. Get distance of particle from centre
        
        # 4. if hit wall: normalize direction from centre, reflect velocity, push particle back in
    

def compute_pressure(n, R, T, V):
    """Compute balloon pressure"""

    global current_pressure, volume
    
    # TODO (Week 2)
    
    # 1. volume = area of a circle (since we're in 2D)
    
    # 2. compute current pressure based on Ideal Gas Law formula
    
    # 3. return current pressure

def check_game_over():
    # TODO (Week 2)


# # *************** STEP 4 ******************
# PLAYER CONTROLS IMPLEMENTAIONT

# master function to handle all inputs
def handle_input(keys):
    global num_particles, balloon_rad, temperature

    if not game_over:
        # no of particle change event
        if keys[pygame.K_d]:
            add_particle()
        if keys[pygame.K_a]:
            remove_particle()

        # temperature change event
        if keys[pygame.K_w]:
            change_temperature(10)
        if keys[pygame.K_s]:
            change_temperature(-10)

        # volume change event
        if keys[pygame.K_UP]:
            balloon_rad = min(balloon_rad + 1, MAX_BALLOON_RADIUS)
        if keys[pygame.K_DOWN]:
            balloon_rad = max(balloon_rad - 1, 20)

    if keys[pygame.K_r]:
        reset_simulation()

    # TODO: UNCOMMENT WHEN INTEGRATING ARDUINO
    # # handle serial input from arduino
    # if ser.in_waiting > 0:
    #     data = ser.readline().decode().strip()  # read a '\n' terminated line
    #     change_temperature(int(data) * 10)
    #     ser.reset_input_buffer()


def add_particle():
    """Add new particle to balloon"""
    global num_particles
    num_particles += 1
    
    # TODO (Week 2)
    
    # 1. Generate random offset from centre (defining new particle position)

    # If too far from center, scale it back to fit inside circle
    
    # 2. Set partcile position
    
    # 3. Set particle velocity

    # Make sure to do the same 0 vector case handling!


def remove_particle():
    """Remove particle from balloon"""
    if num_particles > 1:  # keep at least 1 particle
        num_particles -= 1
        particle_positions.pop()
        particle_velocities.pop()


def change_temperature(delta_temp):
    global temperature
    
    # TODO (Week 2)
        
    # 1. Calculate the "slope" of speed change 
    # Hint: Kinetic Molecular Theory
    
    # 2. Update all particle velocities using the slope

# # *************** STEP 5 ******************
# explosion animation
# displaying final stats


# game set up ========================================

pygame.init()  # Initialize the display module

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ideal Gas Law Simulator")
clock = pygame.time.Clock()
running = True
dt = 0
font = pygame.font.SysFont("Arial", 36)

game_over = False

yoshi_imgs = []
explosion_frames = []
current_frame = 0


def reset_simulation():
    global num_particles, balloon_rad, temperature, game_over, current_pressure, current_frame

    num_particles = STARTING_PARTICLES
    balloon_rad = STARTING_BALLOON_RADIUS
    temperature = STARTING_TEMPERATURE
    current_pressure = 0
    current_frame = 0
    game_over = False

    set_particle_positions()
    set_particle_velocities(temperature)


def init_explosion_frames():
    sprite_sheet = pygame.image.load(
        os.path.join("assets", "explosion.png")).convert_alpha()

    frame_width = 61
    frame_height = 57
    # extract explosion frames from sprite sheet
    for i in range(10):
        frame = sprite_sheet.subsurface(pygame.Rect(
            i * frame_width, 0, frame_width, frame_height))
        explosion_frames.append(frame)


def init_yoshis():
    for i in range(1, 5):
        img = pygame.image.load(
            os.path.join(f"assets/yoshi-{i}.png")).convert_alpha()
        img.set_alpha(200)
        yoshi_imgs.append(img)


def draw_explosion():
    global current_frame

    current_frame += ANIMATION_SPEED * dt
    if current_frame >= len(explosion_frames):
        current_frame = len(explosion_frames) - 1  # hold on last frame

    img = explosion_frames[int(current_frame)]
    img = pygame.transform.scale(
        img, (balloon_rad * 2, balloon_rad * 2))
    screen.blit(img, (balloon_center_x - img.get_width() / 2,
                      balloon_center_y - img.get_height() / 2))


def draw_balloon():
    # select yoshi image based on balloon size
    balloon_stage = current_pressure / MAX_PRESSURE
    if balloon_stage < 0.25:
        img = yoshi_imgs[0]
    elif balloon_stage < 0.5:
        img = yoshi_imgs[1]
    elif balloon_stage < 0.75:
        img = yoshi_imgs[2]
    else:
        img = yoshi_imgs[3]

    img = pygame.transform.scale(
        img, (balloon_rad * 2 * min(1 + balloon_stage / 2, 1.7), balloon_rad * 2 * min(1 + balloon_stage / 2, 1.7)))

    screen.blit(img, (balloon_center_x - img.get_width() / 2,
                balloon_center_y - img.get_height() / 2))

    pygame.draw.circle(screen, (128, 128, 128), (int(balloon_center_x), int(
        balloon_center_y)), int(balloon_rad), 5)


init_yoshis()
init_explosion_frames()
set_particle_positions()
set_particle_velocities(temperature)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if check_game_over():
        game_over = True

    # for step 4
    keys = pygame.key.get_pressed()  # pygame give us the keys getting pressed
    handle_input(keys)
    # for step 3
    update_particle_movement(dt)
    compute_pressure(num_particles, R, temperature, volume)

    # otherwise, game over

    screen.fill((255, 255, 255)) if not game_over else screen.fill(
        (200, 200, 200))
    draw_particles()
    # info text
    info_font = pygame.font.SysFont("Arial", 20)
    stats = [
        f"n (particles): {num_particles}",
        f"V (volume): {volume:.1f}",
        f"T (temp): {temperature}K",
        f"P (pressure): {current_pressure:.1f} / {MAX_PRESSURE}",
    ]
    y_position = 60
    for stat in stats:
        info_text = info_font.render(stat, True, (0, 0, 0))
        screen.blit(info_text, (10, y_position))
        y_position += 25

    if not game_over:
        # Draw balloon
        draw_balloon()

        # title text
        text = font.render(
            "Welcome to the Ideal Gas Law Simulator", True, (100, 100, 100))
        # draw the text on the center-top of the screen
        screen.blit(text, text.get_rect(center=(SCREEN_WIDTH/2, 25)))

    else:
        draw_explosion()
        pop_text = font.render("bawoon popped", True, (255, 50, 50))
        screen.blit(pop_text, pop_text.get_rect(
            center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50)))

        reset_text = font.render(
            "Press 'R' to reset simulation", True, (50, 50, 50))
        screen.blit(reset_text, reset_text.get_rect(
            center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 20)))

    pygame.display.flip()  # Update the full display Surface to the screen
    dt = clock.tick(FRAMES_PER_SECOND) / 1000

pygame.quit()
