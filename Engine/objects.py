import pygame
import random


def center(length):
    """Takes the width and height of an object and returns the coordinates
    to center it."""
    return (length / 2)

def exit_game():
    print("Quitting Game!")
    pygame.quit()
    quit()


class Control:
    
    def __init__(self):
        pass

    def key_down(self, event):
        if event.type == pygame.KEYDOWN:
            return True
        else:
            return False

    def key_up(self, event):
        if event.type == pygame.KEYUP:
            return True
        else:
            return False

    def detect_key(self, event, key):  
        if key == "w":
            if event.key == pygame.K_w:
                return True
        if key == "s":
            if event.key == pygame.K_s:
                return True
        if key == "a":
            if event.key == pygame.K_a:
                return True

        if key == "d":
            if event.key == pygame.K_d:
                return True
    

class Formulas:

    def __init__(self, window):
        self.window = window
        self.big_g = 6.67e5
        self.fps = window.fps

    def gravitational_attraction_g(self, object1, object2):
        """Returns the FORCE OF GRAVITY. Takes in the current object and an object to be attracted to."""

        return self.big_g * ((object1.mass * object2.mass) / self.distance_between(object1.x, object1.y, object2.x, object2.y)**2)
    
    def distance_between(self, x1, y1, x2, y2):
        distance =  ((x1 - x2)**2 + (y1 - y2)**2 ) ** 0.5
        return distance
    
    def velocity(self, pixels, seconds=1):
        """Takes the amount of pixels to move in a given amount of seconds. Seconds is default to one."""
        return pixels / (self.fps * seconds)


class Window:

    def __init__(self, width=1024, height=768, fps=60, background_color=(255, 255, 255), title="Game Window"):
        self.width = width
        self.height = height
        self.fps = fps
        self.background_color = background_color
        self.game_display = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.title = title
        pygame.display.set_caption(self.title)
    
    def update(self):
        self.game_display.fill(self.background_color)
        self.clock.tick(self.fps)
      

class Color:

    def __init__(self):
        self.white = (240, 240, 240)
        self.black = (0, 0, 0)
        self.red = (159, 0, 0)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        self.yellow = (255, 255, 0)
        self.darkgrey = (40, 40, 40)
        self.grassgreen = (76, 139, 58)
        self.orange = (243, 132, 0)
    
    def rand_color(self):
        return random.choice([
        self.white,
        self.black, 
        self.red, 
        self.green,
        self.blue,
        self.yellow,
        self.orange
        ])


class GameObject:

    def __init__(
        self, window, width=10, 
        height=10, initial_speed=0, 
        x=0, y=0, 
        color=(0, 0, 0), size=0,
        speed=0,
        mass=0,
        bounds=True,
    ):

        # Takes the window argument for the FPS
        self.window = window
        self.fps = self.window.fps
        self.window_height = window.height
        self.window_width = window.width
        
        # Sets the height and width of the object
        self.width = width
        self.height = width
        self.initial_speed = initial_speed
        self.x = x
        self.y = y
        self.color = color
        self.speed = speed

        self.x_change = initial_speed
        self.y_change = initial_speed
        self.bounds = bounds

        # Physical Properties
        self.velocity = self.speed / self.fps
        self.mass = mass
        self.acceleration = 0
        self.accelerate = False

        if size > 0:
            self.width = size
            self.height = size

    def movement(self):

        # TODO: Create a way to stop an object when it reaches the 
        # desired location

        # Increases the speed by an amount every second.

        if self.accelerate:
            self.x_change += self.acceleration
            self.y_change += self.acceleration

        self.x += self.x_change
        self.y += self.y_change
    
    def vector(self, x_change, y_change):
        self.x_change = x_change
        self.y_change = y_change
    
    def stop(self):
        self.x_change = 0
        self.y_change = 0

    def update(self):
        if self.bounds:
            self.test_boundary()

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(self.window.game_display, self.color, self.rect)

    def run(self):
        self.movement()
        self.update()
    
    def move_to(self, target_x, target_y, velocity=0, time=1, acceleration=0):
        """Moves object towards the given target. Time is taken in seconds."""

        self.target_x = target_x
        self.target_y = target_y

        if time > 0:
            speed = self.fps * time
        
        if velocity > 0:
            speed = velocity * self.fps
        
        if acceleration > 0:
            self.accelerate = True
            self.acceleration = acceleration
            speed = self.fps * time

        if self.target_x > self.x and self.target_y > self.y:
            self.x_change = (self.target_x - self.x) / speed
            self.y_change = (self.target_y - self.y) / speed
        
        elif self.target_x < self.x and self.target_y < self.y:
            self.x_change = (self.target_x - self.x) / speed
            self.y_change = (self.target_y - self.y) / speed

        elif self.target_x > self.x and self.target_y < self.y:
            self.x_change = (self.target_x - self.x) / speed
            self.y_change = (self.target_y - self.y) / speed
            return
        
        elif self.target_x < self.x and self.target_y > self.y:
            self.x_change = (self.target_x - self.x) / speed
            self.y_change = (self.target_y - self.y) / speed
            return

   

    def accelerate(self, x_change, y_change):
        self.x_change -= x_change
        self.y_change -= y_change
        
    def collide(self, other_object):
        return self.rect.colliderect(other_object.rect)
    
    def test_boundary(self):
        if self.x > self.window_width:
            self.x = 0
            return True
        
        if self.x < 0:
            self.x = self.window_width 
            return True

        if self.y < 0:
            self.y = self.window_height
            return True
        
        if self.y > self.window_height:
            self.y = 0
            return True
