import pygame
import math
pygame.init()

# Window initialization
WIDTH, HEIGHT = 1000, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Orbit Simulator")

# Window instances
FPS = 60
FONT = pygame.font.SysFont("comicsans ms", 20)

# Colors
WHITE = (255, 255, 255)
SUN_COLOR = (253, 184, 19)
MERCURY_COLOR = (231,232,236)
VENUS_COLOR = (248,226,176)
EARTH_COLOR = (50, 150, 255)
MARS_COLOR = (240,100,31)

################################################################

# Game instances
class Planet:
    # Astronomical units, mandatory for any astrodynamics simulation
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 210 / AU    # 1 AU = 100 pixels
    TIMESTEP = 60 * 60 * 12    # 1/2 Day
 
    def __init__(self, name, x, y, radius, color, mass):
        self.name = name
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.x_velocity = 0
        self.y_velocity = 0

        self.distance_to_sun = 0
        self.orbit = []

    def draw(self):
        x = self.x * Planet.SCALE + WIDTH//2
        y = self.y * Planet.SCALE + HEIGHT//2

        P = int(2 * self.distance_to_sun * math.pi * Planet.SCALE) // 5
        if len(self.orbit) > P > 2:
            updated_points = []
            for point in [self.orbit[i] for i in range(len(self.orbit) - P, len(self.orbit))]:
                x, y = point
                x = x * Planet.SCALE + WIDTH//2
                y = y * Planet.SCALE + HEIGHT//2
                updated_points.append((x, y))
            pygame.draw.lines(WIN, self.color, False, updated_points, 2)
        
        elif len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * Planet.SCALE + WIDTH//2
                y = y * Planet.SCALE + HEIGHT//2
                updated_points.append((x, y))
            pygame.draw.lines(WIN, self.color, False, updated_points, 2)

        pygame.draw.circle(WIN, self.color, (x, y), self.radius)

        planet_text = FONT.render(f"{self.name}", 1, WHITE)
        WIN.blit(planet_text, (x - planet_text.get_width()/2, (y + planet_text.get_height()//3) if self.name != "Sun" else y - planet_text.get_height()/2))

    def attraction(self, other):
        distance_x = other.x - self.x
        distance_y = other.y - self.y
        distance = math.sqrt(distance_x**2 + distance_y**2)

        if other.name == "Sun":
            self.distance_to_sun = distance
        
        force = Planet.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force

        return force_x, force_y
    
    def update_positions(self, planets):
        total_fx, total_fy = 0, 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_velocity += total_fx / self.mass * self.TIMESTEP
        self.y_velocity += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_velocity * self.TIMESTEP
        self.y += self.y_velocity * self.TIMESTEP
        self.orbit.append((self.x, self.y))

################################################################

# Drawing function
def draw(planets):

    for planet in planets: 
        planet.update_positions(planets)
        planet.draw()

    pygame.display.update()

# Main function
def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet("Sun", 0, 0, 30, SUN_COLOR, 1.98892 * 10**30)

    mercury = Planet("Mercury", 0.387 * Planet.AU, 0, 8, MERCURY_COLOR, 3.30 * 10**23)
    mercury.y_velocity = -47.4 * 1000

    venus = Planet("Venus", 0.723 * Planet.AU, 0, 14, VENUS_COLOR, 4.8685 * 10**24)
    venus.y_velocity = -35.02 * 1000

    earth = Planet("Earth", -1 * Planet.AU, 0, 17, EARTH_COLOR, 5.9742 * 10**24)
    earth.y_velocity = 29.783 * 1000

    mars = Planet("Mars", -1.524 * Planet.AU, 0, 12, MARS_COLOR, 6.39 * 10**23)
    mars.y_velocity = 24.077 * 1000

    planets = [sun, mercury, venus, earth, mars]

    while run:
        clock.tick(FPS)
        WIN.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                break
        draw(planets)

    pygame.quit()

################################################################

if __name__ == "__main__":
    main()
