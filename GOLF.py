import pygame
import math
import random
import time


pygame.init()
display = pygame.display.set_mode((700, 700))
pygame.display.set_caption('GOLF')
clock = pygame.time.Clock()
bgColor = (0,random.randint(50, 200),0)

#inital momentum for ball
startPush = 5
mouse_button_down = False

replay_same_level = False

def draw_wind_arrow():
    # Center of the arrow
    arrow_center_x, arrow_center_y = 650, 50
    arrow_length = 40  # Adjust length as needed

    # Calculate the end point of the arrow
    end_x = arrow_center_x + arrow_length * math.cos(math.radians(wind_angle))
    end_y = arrow_center_y + arrow_length * math.sin(math.radians(wind_angle))

    # Draw the arrow line
    pygame.draw.line(display, (255, 255, 255), (arrow_center_x, arrow_center_y), (end_x, end_y), 2)

    # Draw the arrow head
    arrow_head_size = 10
    angle_offset = 30  # Angle of the arrow head lines in degrees

    # Calculate points for the arrow head
    left_x = end_x + arrow_head_size * math.cos(math.radians(wind_angle + 180 + angle_offset))
    left_y = end_y + arrow_head_size * math.sin(math.radians(wind_angle + 180 + angle_offset))
    right_x = end_x + arrow_head_size * math.cos(math.radians(wind_angle + 180 - angle_offset))
    right_y = end_y + arrow_head_size * math.sin(math.radians(wind_angle + 180 - angle_offset))

    # Draw the arrow head
    pygame.draw.polygon(display, (255, 255, 255), [(end_x, end_y), (left_x, left_y), (right_x, right_y)])


def reset_level(same_level=False):
    global  crocs, wind_speed, wind_angle, mainBall, rocks, sands, hole, replay_same_level, pShots, shots

    wind_speed = random.randint(WINDMIN, WINDMAX)
    wind_angle = random.randint(0, 360)
    pShots = shots
    shots = 0
    mainBall = Ball(350, 400)
    mainBall.wind_speed = wind_speed
    mainBall.wind_angle = wind_angle
    if not same_level:
        hole = Hole(random.randint(10, 690), random.randint(10, 690))
        rocks = [Rock(random.randint(10, 690), random.randint(10, 690)) for _ in range(17)]
        sands = [Sand(random.randint(10, 690), random.randint(10, 690)) for _ in range(12)]
        crocs = [Croc(random.randint(10, 690), random.randint(10, 690), bgColor) for _ in range(4)]
    else:
        replay_same_level = True

        
#Hole spot 
hX = 500
hY = 500

#Start x and y for hole
sX = 0
sY = 0

# Wind settings
WINDMAX = 2
WINDMIN = 0
wind_speed = random.randint(WINDMIN, WINDMAX)  # Negative for leftward wind, positive for rightward
wind_angle = random.randint(0, 360)  # Wind angle in degrees

shots = 0
#previous holes scores
pShots = 0
rounds = 0


class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.target_x = x
        self.target_y = y
        self.speed = 0
        self.moving = False
        self.dx = 0
        self.dy = 0
        self.recent_shot = False
        self.being_pushed = False
        self.wind_speed = wind_speed
        self.wind_angle = wind_angle
        self.friction = 0.97  # Friction factor (less than 1, adjust as needed)
        self.min_speed_to_move =1  # Minimum speed required for the ball to keep moving



    def main(self, display):
        pygame.draw.circle(display, (255, 255, 255), (self.x, self.y), 5)
        self.moving = True
        
    def move(self):
        if self.moving:
            if self.x < 0:
                self.x = 0
            if self.x > 700:
                self.x = 700
            if self.y < 0:
                self.y = 0
            if self.y > 700:
                self.y = 700
            # Apply wind effect only if a recent shot was made
            if self.recent_shot:
                wind_dx = self.wind_speed * math.cos(math.radians(self.wind_angle))
                wind_dy = self.wind_speed * math.sin(math.radians(self.wind_angle))

                # Limit wind effect based on the distance to screen edges
                if 10 < self.x < 690 and 10 < self.y < 690:
                    self.x += (self.dx * self.speed) + wind_dx
                    self.y += (self.dy * self.speed) + wind_dy
                else:
                    self.x += self.dx * self.speed
                    self.y += self.dy * self.speed
            else:
                self.x += self.dx * self.speed
                self.y += self.dy * self.speed

            # Apply friction and check for stop
            self.speed *= self.friction
            if self.speed < self.min_speed_to_move:
                self.speed = 0
                self.moving = False
                self.recent_shot = False  # Reset the flag as the ball has stopped

    def set_target(self, target_x, target_y, power):
        self.target_x = target_x
        self.target_y = target_y
        self.dx = target_x - self.x
        self.dy = target_y - self.y
        self.recent_shot = True
        distance = math.sqrt(self.dx**2 + self.dy**2)

        # Set speed based on power
        self.speed = power

        # Normalize direction
        if distance != 0:
            self.dx /= distance
            self.dy /= distance

        self.moving = True
        
mainBall = Ball(350, 400)
sX = mainBall.x
sY = mainBall.y
        
mainBall = Ball(350, 400)
sX = mainBall.x
sY = mainBall.y

# Power bar settings
max_power = 10
current_power = 0
power_bar_length = 200  # Length of the power bar
power_bar_height = 20   # Height of the power bar
power_bar_x = 250       # X position of the power bar
power_bar_y = 10        # Y position of the power bar

class Hole:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 10  # You can adjust the radius as needed

    def main(self, display):
        pygame.draw.circle(display, (0, 0, 0), (self.x, self.y), self.radius)

    def check(self):
        global shots, rounds
        if mainBall.x > self.x - 6 and mainBall.y > self.y - 6 and mainBall.x < self.x + 10 and mainBall.y < self.y + 10:
            rounds += 1
            reset_level(same_level=replay_same_level)



class Sand:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = random.randint(20, 60)  # You can adjust the radius as needed

    def main(self, display):
        pygame.draw.circle(display, (255, 155, 20), (self.x, self.y), self.radius)

    def check(self, ball):
        # Calculate the distance between the ball and the center of the sand area
        distance = math.sqrt((self.x - ball.x)**2 + (self.y - ball.y)**2)

        # Check if the ball is within the sand area
        if distance < self.radius + 5:  # Assuming the ball's radius is about 5
            ball.speed -= 1
            if ball.speed < 1:
                ball.speed = 0

class Croc:
    def __init__(self, x, y,bgColor):
        self.speed = 1  # Adjust as needed
        self.direction = 1  # 1 for right, -1 for left
        self.move_time = 5  # Time in seconds to move in one direction
        self.last_turn_time = time.time()
        self.x = x
        self.y = y
        self.color = (10,50,10)
        self.angle = random.uniform(0, 2 * math.pi)  # Random angle in radians


    def move(self):
        # Update position based on angle
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed

        current_time = time.time()
        if current_time - self.last_turn_time > self.move_time:
            self.angle = random.uniform(0, 2 * math.pi)  # Choose a new random angle
            self.last_turn_time = current_time
        if self.x < 0 or self.x > 700:  # Assuming screen_width is defined
            self.angle = math.pi - self.angle
        if self.y < 0 or self.y > 700:  # Assuming screen_height is defined
            self.angle = -self.angle

    def check(self):
        if mainBall.x > self.x -6 and mainBall.y > self.y -6 and mainBall.x < self.x + (10+ 10 )and mainBall.y < self.y  +(10+ 10):
            mainBall.speed = mainBall.speed - 1
            if mainBall.speed < 1:
                mainBall.speed = 0
                
    def push_ball(self, ball):
        # Check if the croc is close enough to the ball
        distance = math.sqrt((self.x - ball.x)**2 + (self.y - ball.y)**2)
        if distance < 10 + 5:  # Assuming the ball's radius is about 5
            # Push the ball in the same direction as the croc is moving
            ball.dx += math.cos(self.angle) * self.speed
            ball.dy += math.sin(self.angle) * self.speed
            ball.moving = True
            
    def main(self, display):
        pygame.draw.circle(display, self.color, (self.x, self.y), 10)

class Rock:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 20  # You can adjust the radius as needed

    def main(self, display):
        pygame.draw.circle(display, (100, 0, 0), (self.x, self.y), self.radius)

    def check(self):
        if mainBall.x > self.x -10 and mainBall.y > self.y -10 and mainBall.x < self.x + 20 and mainBall.y < self.y + 20:
            #RESET
            global shots
            if mainBall.speed < 2:
                mainBall.speed = 1
            mainBall.set_target(-1*mainBall.target_x, -1*mainBall.target_y, mainBall.speed)

            


            
def display_wind_info():
    wind_text = f'Wind: {wind_speed} m/s, Angle: {wind_angle}°'
    wind_surface = my_font.render(wind_text, True, (255, 255, 255))
    display.blit(wind_surface, (10, 50))
    
hole = Hole(hX, hY)
rocks = []
sands = []
crocs = []
for i in range(10):
    rock = Rock(random.randint(10, 690), random.randint(10, 690))
    rocks.append(rock)    

for i in range(10):
    sand = Sand(random.randint(10, 690), random.randint(10, 690))
    sands.append(sand)


for i in range(2):
    croc = Croc(random.randint(10,690),random.randint(10,690),bgColor)  # Replace start_x and start_y with the initial position
    crocs.append(croc)

pygame.font.init()

while True:
    my_font = pygame.font.SysFont('modernno20', 30)  # You can change 'Arial' to any available font and adjust the size

 
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_g:
                reset_level()
                replay_same_level = False   # Turn off replay mode
            if event.key == pygame.K_i:
                reset_level(same_level=True)
                
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_button_down_time = pygame.time.get_ticks()
            mouse_button_down = True

        if event.type == pygame.MOUSEBUTTONUP:
            if mouse_button_down:
                duration = pygame.time.get_ticks() - mouse_button_down_time
                mouse_button_down = False
                power = min(duration / 150, max_power)
                # Set target with power
                mainBall.set_target(*event.pos, power)
                shots += 1
                current_power = 0  # Reset power after the shot
    if mouse_button_down:
        duration = pygame.time.get_ticks() - mouse_button_down_time
        current_power = min(duration / 150, max_power)

    # Move the ball and update the display
    display.fill(bgColor)  # Background color
    
    mainBall.move()
    for r in rocks:
        r.main(display)
        r.check()
    for s in sands:
        s.main(display)
        s.check(mainBall)
    for c in crocs:
        c.main(display)
        c.move()
        c.check()
        c.push_ball(mainBall)  # Push the ball if it's close enough

    
    hole.main(display)
    hole.check()
    mainBall.main(display)
    # Draw the power bar background
    pygame.draw.rect(display, (128, 128, 128), (power_bar_x, power_bar_y, power_bar_length, power_bar_height))

    # Draw the current power level
    filled_length = (current_power / max_power) * power_bar_length
    pygame.draw.rect(display, (255, 0, 0), (power_bar_x, power_bar_y, filled_length, power_bar_height))
        # Render the shot count and display it
    shots_surface = my_font.render(f'Strokes: {shots}', True, (255, 255, 255))  # White color for the text
    display.blit(shots_surface, (10, 10))  # Position the text at the top of the screen
    my_font = pygame.font.SysFont('modernno20', 20)  # You can change 'Arial' to any available font and adjust the size

    display_wind_info()

    pShotsT = my_font.render(f'Previous Strokes: {pShots}', True, (255, 255, 255))  # White color for the text
    display.blit(pShotsT, (10, 70))  # Position the text at the top of the screen

    if replay_same_level:
        replay_mode_surface = my_font.render('Replay Mode ON', True, (255, 255, 255))
        display.blit(replay_mode_surface, (10, 100))


    draw_wind_arrow()

 
    pygame.display.update()
    clock.tick(60)  # Set the FPS
