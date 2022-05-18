import pygame, sys, random, math, time

pygame.init()
pygame.display.set_caption('Artificial Swarming') 


# colours
WHITE = (255,255,255)
BLUE = (0,0,200)
RED = (200,0,0)
GREEN = (0,200,0)
NAVY_BLUE = (10,10,50)
BLACK = (0,0,0)

# other constants
screen_width = 1000
screen_height = 500
NUM_BOIDS = 100
PERCEPTION_RADIUS = 75
boundary = 50


# screen
screen = pygame.display.set_mode((screen_width, screen_height))

# clock
clock = pygame.time.Clock()
FPS = 50

# chief circle position x,y velocity vx,vy acceleration ax,ay
chief_circle_x = 500
chief_circle_y = 250
chief_circle_vx = 5
chief_circle_vy = 1
chief_circle_ax = 0.7
chief_circle_ay = 0.7
chief_border_speed_change = 0.5
chief_circle_max_v = 7

# boids position and speed variation from chief circle
pos_spread = 100 # starting position of boids
speed_spread = 5
boid_max_v = 7
boid_acc = 0.5
min_dist = 5
sum_boid_speed_x = 0 # sum of boid speed in perception radius
sum_boid_speed_y = 0 # sum of boid speed in perception radius
count_boid_vicinity = 0 # number of boids in the perception radius

# generate boids
i = 0
boid_list = []
while (i < NUM_BOIDS):
    x = random.uniform(screen_width/2 - pos_spread, screen_height/2 + pos_spread)
    y = random.uniform(screen_width/2 - pos_spread, screen_height/2 + pos_spread)
    vx = random.uniform(-speed_spread, speed_spread)
    vy = random.uniform(-speed_spread, speed_spread)
    
    new_boid = [x, y, vx, vy]

    boid_list.append(new_boid)
    i += 1

#if __name__ == '__main__':

# Game Loop
run = True
while run:
    screen.fill(NAVY_BLUE)
    mx,my = pygame.mouse.get_pos()
    
    # Quit option ------------------------------------------------ #
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
                pygame.quit()
                sys.exit()

    # draw chief circle and make it move randomly
    #pygame.draw.circle(screen, WHITE, (int(chief_circle_x), int(chief_circle_y)), 5)

    chief_circle_vx += random.uniform(-chief_circle_ax, chief_circle_ax)
    chief_circle_vy += random.uniform(-chief_circle_ay, chief_circle_ay)

    chief_circle_x += chief_circle_vx
    chief_circle_y += chief_circle_vy

    # Update leader bird position and speed
    if (chief_circle_x < boundary):                               # change direction slowly at border
        chief_circle_vx += chief_border_speed_change
    if (chief_circle_y < boundary):                               # change direction slowly at border
        chief_circle_vy += chief_border_speed_change
    if (chief_circle_x > screen_width - boundary):                # change direction slowly at border
        chief_circle_vx -= chief_border_speed_change
    if (chief_circle_y > screen_height - boundary):               # change direction slowly at border
        chief_circle_vy -= chief_border_speed_change
    if (chief_circle_vx > chief_circle_max_v):              # limit velocity in x
        chief_circle_vx -= chief_circle_ax
    if (chief_circle_vy > chief_circle_max_v):              # limit velocity in y
        chief_circle_vy -= chief_circle_ay


    # draw boids
    for boid in range(NUM_BOIDS):
        x = boid_list[boid][0]
        y = boid_list[boid][1]
        vx = boid_list[boid][2]
        vy = boid_list[boid][3]

        boid_list[boid][2] += 0.001*(chief_circle_x -x) # boid velocity x
        boid_list[boid][3] += 0.001*(chief_circle_y -y) # boid velocity y

        boid_list[boid][0] += boid_list[boid][2] # use vel to change boid pos not x value
        boid_list[boid][1] += boid_list[boid][3] 
        
        pygame.draw.circle(screen, (WHITE), (int(x), int(y)), 3)

        # Update boid position and speed
        if (boid_list[boid][0] < boundary):                           # change direction slowly at border
            boid_list[boid][2] += chief_border_speed_change
        if (boid_list[boid][1] < boundary):                               # change direction slowly at border
            boid_list[boid][3] += chief_border_speed_change
        if (boid_list[boid][0] > screen_width - boundary):                # change direction slowly at border
            boid_list[boid][2] -= chief_border_speed_change
        if (boid_list[boid][1] > screen_height - boundary):               # change direction slowly at border
            boid_list[boid][3] -= chief_border_speed_change
        if (boid_list[boid][2] > boid_max_v):              # limit velocity in x
            boid_list[boid][2] -= boid_acc
        if (boid_list[boid][3] > boid_max_v):              # limit velocity in y
            boid_list[boid][3] -= boid_acc

        # for maintaining minimum distance

        sum_boid_speed_x = 0 # sum of boid speed in perception radius
        sum_boid_speed_y = 0 # sum of boid speed in perception radius
        count_boid_vicinity = 0 # number of boids in the perception radius
        avg_vx = 0 # average speed in the perception radius
        avg_vy = 0

        for other_boid in range(NUM_BOIDS):
            if ( other_boid != boid):
                dx = boid_list[other_boid][0] - x
                dy = boid_list[other_boid][1] - y
                dist = math.sqrt(dx**2 + dy**2)
                if (dist < min_dist):
                    boid_list[boid][2] -= dx*0.1 # change boid velocity
                    boid_list[boid][3] -= dy*0.1
                if (dist < PERCEPTION_RADIUS): # calculate avg speed in the vicinity
                    sum_boid_speed_x +=  boid_list[other_boid][2]
                    sum_boid_speed_y +=  boid_list[other_boid][3]
                    count_boid_vicinity += 1

        # calculate average speed of all the other boids after looping through them
        if (count_boid_vicinity != 0): # without if conddition we may get 0/0
            avg_vx = sum_boid_speed_x/count_boid_vicinity
            avg_vy = sum_boid_speed_y/count_boid_vicinity
            boid_list[boid][2] = 0.98*boid_list[boid][2] + 0.02*avg_vx
            boid_list[boid][3] = 0.98*boid_list[boid][3] + 0.02*avg_vy
  
              
    clock.tick(FPS)
    pygame.display.flip()
    pygame.display.update()
