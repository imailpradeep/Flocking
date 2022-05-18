import pygame, sys, random, math, time

pygame.init()
pygame.display.set_caption('Magnets flocking') #Artificial Swarming


# colours
WHITE = (255,255,255)
BLUE = (0,0,200)
RED = (200,0,0)
GREEN = (0,200,0)
NAVY_BLUE = (10,10,50)
BLACK = (0,0,0)
screen_width = 900
screen_height = 500
NUM_BOIDS = 25
PERCEPTION_RADIUS = 300 # distance at which a magnet is influenced by another


# screen
screen = pygame.display.set_mode((screen_width, screen_height))

# clock
clock = pygame.time.Clock()
FPS = 60

# generate random initial positions for boids
initial_pos_generate = False
pos = []
def initial_position_boids():
    for pos_x in range(NUM_BOIDS):
        pos_y =[]
        
        pos_y.append(random.randint(0,screen_width))
        pos_y.append(random.randint(0,screen_height))
        pos.append(pos_y)  
    #print(pos)


# find distance from each circle to every other circle
distance_array = []
distance_array_generate = False

mean_perception_area = []
def distance_to_all():
    mean_x = []
    mean_y = []
    for boid in range(NUM_BOIDS):
        distance_array_col =[]
        x=[]
        y=[]
        for other_boids in range(NUM_BOIDS):
            dist = math.dist(pos[boid],pos[other_boids])
            distance_array_col.append(dist)
            x.append(pos[boid][0])
            y.append(pos[boid][1])
            # assign x and y co-ordinates of all circles within perception range to x and y lists
            if dist < PERCEPTION_RADIUS:
                x.append(pos[other_boids][0])
                y.append(pos[other_boids][1])
            
        # take average mean position in perception range
        mean_x = int(sum(x)/len(x))
        mean_y = int(sum(y)/len(y))
        #print(mean_x,mean_y)
        pos[boid][0]= mean_x
        pos[boid][1] = mean_y
        
        pygame.draw.circle(screen, WHITE,pos[boid],5)
        pygame.display.flip()
        pygame.display.update()

        #NUM_BOIDS = len(mean_x)

        distance_array.append(distance_array_col)

        
    #print(distance_array)



#if __name__ == '__main__':

# Game Loop
while True:
    screen.fill(NAVY_BLUE)
    mx,my = pygame.mouse.get_pos()
    
    # Quit option ------------------------------------------------ #
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    # generate initial position of circles by calling function
    if (initial_pos_generate == False):
        initial_position_boids()
        initial_pos_generate = True

    # draw circles at initial position 
    for boid in range(NUM_BOIDS):
       pygame.draw.circle(screen, WHITE,pos[boid],5)
       

    # calculate distance to all circles
    if (distance_array_generate == False):
        distance_to_all()
        time.sleep(0.2)
        #distance_array_generate = True

    
    
    #pygame.display.flip()
    #pygame.display.update()
