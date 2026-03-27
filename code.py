#30,000 m^3 / hr
import random
import math

rho_p = 600
y0 = 0
l = 1
vx = 0
v_air = 100 #no idea

class Particle:
    def __init__(self, posX, posY, velX, velY, diameter, mass):
        self.posX = posX
        self.posY = posY
        self.velX = velX
        self.velY = velY
        self.mass = mass
        self.diameter = diameter

def generateParticles():
    totParticles = 10 #the total num of particles to generate

    listOfParticles = []
    numPm25 = int(totParticles * (14 + 19) / (14 + 19 + 24 + 29)) #ratio of pm2.5 particles
    numPm10 = int(totParticles * (24 + 29) / (14 + 19 + 24 + 29)) # ratio of pm10 particles

    # generate pm2.5 particles
    for i in range(0, numPm25):
        p = generateSingleParticle(0, 2.5 * pow(10, -6))
        listOfParticles.append(p)
         
    # generate pm 10 particles
    for i in range(0, numPm10):
        p = generateSingleParticle(2.5 * pow(10, -6), 10.0 * pow(10, -6))
        listOfParticles.append(p)

    return listOfParticles

def generateSingleParticle(diamMin, diamMax):
    diameter = random.uniform(diamMin, diamMax)
    posX = random.uniform(0, l)
    mass = 1 / 6 * math.pi * rho_p * pow(diameter, 3)
    p = Particle(posX, y0, vx, v_air, diameter, mass)
    return p

ps = generateParticles()

for p in ps:
    print(f" {p.posX:.2f} - {p.diameter} - {p.mass}")