
import pygame
import math
import random
import os
import serial

# ARDUINO_PORT = '/dev/cu.debug-console'  # Update this to your Arduino port
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

# Helper Functions ==================================

# 💡 1.4: The Kinetic Molecular Theory of Ideal Gases
# source: https://chem.libretexts.org/Courses/Bellarmine_University/BU%3A_Chem_104_(Christianson)/Phase_1%3A_The_Phases_of_Matter/1%3A_Gases/1.4%3A_The_Kinetic_Molecular_Theory_of_Ideal_Gases

# positions init


def set_particle_positions():
    """Initialize particles randomly inside the balloon
    """

    particle_positions.clear()

    for i in range(num_particles):

        # using pythagorean theorem/distance to set particle position within circle balloon

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

    """

    # M needs to be in kg/mol, so convert g/mol to kg/mol
    M = m / 1000  # 0.031989... kg/mol
    v_rms = 0  # TODO: v_rms = sqrt(3RT/M)

    # Scaling down for game (this would be ~500 m/s in reality, too fast for pygame!)
    scale_factor = 0.05
    return v_rms * scale_factor


def set_particle_velocities(temp):
    """ TODO: Initialize particle velocities based on Temperature
    """

    pass


def draw_particles():
    colour_scale = int(
        min(temperature, WATER_BOILING_POINT) / WATER_BOILING_POINT * 255)
    particle_colour = (colour_scale, 100, 255 - colour_scale)

    # TODO draw all particles as circles


# *************** STEP 3 ******************

# particle movements
def update_particle_movement(dt):
    """Update all particle positions and handle collisions"""

    for i in range(num_particles):
        # reposition partcile
        particle_positions[i] += particle_velocities[i] * dt

        # checking circular boundary collision
        dx = particle_positions[i].x - balloon_center_x
        dy = particle_positions[i].y - balloon_center_y
        # √x^2 + y^2
        distance = math.sqrt(dx**2 + dy**2)
        # if distance is beyond balloon wall
        if distance > balloon_rad and not game_over:
            # collision detected!

            # reflect velocity using the normal vector from centrer of parcile
            normal_x = dx / distance  # normalizing
            normal_y = dy / distance

            # GIVEN
            dot_product = (particle_velocities[i].x * normal_x +
                           particle_velocities[i].y * normal_y)

            particle_velocities[i].x -= 2 * dot_product * normal_x
            particle_velocities[i].y -= 2 * dot_product * normal_y

            # get ye back in da bubble
            particle_positions[i].x = balloon_center_x + \
                normal_x * (balloon_rad - 1)
            particle_positions[i].y = balloon_center_y + \
                normal_y * (balloon_rad - 1)


def compute_pressure(n, R, T, V):
    global current_pressure, volume

    # TODO: compute volume based on balloon radius
    # TODO: set current pressure, P = nRT/V (treating num_particles as n for our context)

    return current_pressure


def check_game_over():
    if current_pressure > MAX_PRESSURE:
        return True  # game over
    return False


# # *************** STEP 4 ******************
# PLAYER CONTROLS IMPLEMENTATION

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

    # handle serial input from arduino
    # if ser.in_waiting > 0:
    #     data = ser.readline().decode().strip()  # read a '\n' terminated line
    #     change_temperature(int(data) * 10)
    #     ser.reset_input_buffer()


def add_particle():
    # pretty much redoing set position and set velocity but for singular particle
    global num_particles
    num_particles += 1

    # should spawn in some random location in the ballooon
    random_x = random.uniform(-balloon_rad + 8, balloon_rad - 8)
    random_y = random.uniform(-balloon_rad + 8, balloon_rad - 8)

    distance = math.sqrt(random_x**2 + random_y**2)

    if distance > balloon_rad - 8:
        scale = (balloon_rad - 8) / distance
        random_x *= scale
        random_y *= scale

    pos_x = balloon_center_x + random_x
    pos_y = balloon_center_y + random_y

    particle_positions.append(pygame.Vector2(pos_x, pos_y))

    # now setting velocity
    #  based on current temperature
    speed = calculate_particle_speed(temperature)
    v = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
    if v.length() > 0:
        v.scale_to_length(speed)
    else:
        v = pygame.Vector2(speed, 0)
    particle_velocities.append(v)


def remove_particle():
    global num_particles

    if num_particles > 1:  # keep at least 1 particle
        num_particles -= 1
        particle_positions.pop()
        particle_velocities.pop()


def change_temperature(delta_temp):
    # students TODO (or part of it)
    global temperature
    old_temp = temperature
    temperature = max(temperature + delta_temp, 50)  # Min temp = 50K

    # scalling all velocities based on temperature change
    # since kinetic neergy is proportional to T, and KE proptional to v² by defn of KE
    # we have v protoinal √T
    speed_scale = math.sqrt(temperature / old_temp)

    for i in range(len(particle_velocities)):
        particle_velocities[i] *= speed_scale


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
