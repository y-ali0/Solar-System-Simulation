import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

class SolarSystem():
    """This class creates the SolarSystem object."""
    def __init__(self, size=1000):
        """With self you can access private attributes of the object."""
        self.size = size
        self.planets = []
        # This initializes the 2D figure
        self.fig = plt.figure()
        self.ax = plt.subplot()
        self.dT = 1

    def add_planet(self, planet):
        """Every time a planet is created it gets put into the array."""
        self.planets.append(planet)

    def update_planets(self):
        """This method moves and draws all of the planets."""
        self.ax.clear()
        for planet in self.planets:
            planet.move()
            planet.draw()

    def fix_axes(self):
        """The axes would change with each iteration otherwise."""
        self.ax.set_xlim((-self.size/2, self.size/2))
        self.ax.set_ylim((-self.size/2, self.size/2))

    def gravity_planets(self):
        """This method calculated gravity interaction for every planet."""
        for i, first in enumerate(self.planets):
            if isinstance(first, Sun):
                continue
            for second in self.planets:
                if second == first:
                    continue
                first.gravity(second)

class Planet():
    """This class creates the Planet object."""
    def __init__(self, SolarSys, mass, position, velocity, color="black"):
        self.SolarSys = SolarSys
        self.mass = mass
        self.position = position
        self.velocity = velocity
        # The planet is automatically added to the SolarSys.
        self.SolarSys.add_planet(self)
        self.color = color

    def move(self):
        """The planet is moved based on the velocity."""
        self.position = (self.position[0] + self.velocity[0]*self.SolarSys.dT, self.position[1] + self.velocity[1]*self.SolarSys.dT)

    def draw(self):
        """The method to draw the planet."""
        self.SolarSys.ax.plot(*self.position, marker="o", markersize=10, color=self.color)

    def gravity(self, other):
        """The method to compute gravitational force for two planets. numpy module is used to handle vectors."""
        distance = np.subtract(other.position, self.position)
        distanceMag = np.linalg.norm(distance)
        distanceUnit = np.divide(distance, distanceMag)
        forceMag = self.mass*other.mass / (distanceMag**2)
        force = np.multiply(distanceUnit, forceMag)
        acceleration = np.divide(force, self.mass)
        self.velocity = np.add(self.velocity, np.multiply(acceleration, self.SolarSys.dT))

class Sun(Planet):
    """This class is inherited from planet. Everything is the same as in planet, except the position of the Sun is fixed and it is yellow"""
    def init(self,SolarSys, mass=1000, position=(0,0), velocity = (0,0)):
        super(Sun, self).init(SolarSys,mass,position,velocity)
        self.color = "yellow"

    def move(self):
        self.position = self.position

    def draw(self):
        """The method to draw the sun."""
        self.SolarSys.ax.plot(*self.position, marker="o", markersize = 20, color="yellow")

""" Instantiating of the solar system."""
SolarSys = SolarSystem()

"""Instantiating of the sun"""
sun = Sun(SolarSys, mass=1000, position=(0,0), velocity =(0,0))

"""Instantiating of planets"""
planet1 = Planet(SolarSys, mass=10, position=(600,250), velocity=(-10,0))
planet2 = Planet(SolarSys, mass=10, position=(600,200), velocity=(-10,0))
planet3 = Planet(SolarSys, mass=10, position=(600,150), velocity=(-10,0))
planet4 = Planet(SolarSys, mass=10, position=(600,100), velocity=(-10,0))
planet5 = Planet(SolarSys, mass=10, position=(600,50), velocity=(-10,0))

"""Create a list of planets for each simulation"""
simulations = [
[sun, planet1],
[sun, planet2],
[sun, planet3],
[sun, planet4],
[sun, planet5]
]

"""Create a list of axes for each simulation"""
axes_list = []

"""Create a subplot for each simulation"""
for i in range(len(simulations)):
    ax = SolarSys.fig.add_subplot(1, len(simulations), i+1)
    axes_list.append(ax)
    
def animate(i):
    """This controls the animation."""
    print("The frame is:", i)
    for j in range(len(simulations)):
        # Set the active subplot
        SolarSys.ax = axes_list[j]
        # Set the planets for the current simulation
        SolarSys.planets = simulations[j]
        SolarSys.gravity_planets()
        SolarSys.update_planets()
        SolarSys.fix_axes()

"""This calls the animate function and creates animation."""
anim = animation.FuncAnimation(SolarSys.fig, animate, frames=100, interval=100)

"""This prepares the writer for the animation"""
writervideo = animation.FFMpegWriter(fps=60)

"""Shows the animation"""
plt.show()
