from boids.vector import Vector
import numpy as np
import mesa
import random
import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

        
class Boid():
    #Inicializando un agente con ciertas posiciones
    def __init__(self, x, y, width, height, id):
        self.id = id
        self.position = Vector(x, y) #Inicializando apoyandonos de la clase vector, la clase vector crea un vector con x,y,z donde z = 0
        vec = [4,5] #Obteniendo valores aleatorios para la creación del vector de cada agente
        self.velocity = Vector(*vec) #Creando un vector velocidad, apoyándonos de un argumento para automaticamente adaptar la información al vector

        vec = [vec[0]/2,vec[1]/2]#Obteniendo valores aleatorios, de donde obtendremos la aceleración
        self.acceleration = Vector(*vec) #Creando un vector aceleración, apoyándonos de un argumento para automaticamente adaptar la información al vector
        self.max_force = 0.3 #Fuerza inicial
        self.max_speed = 5 #Velocidad inicial
        self.perception = 100

        self.width = width
        self.height = height

    def update(self):
        self.position += self.velocity
        self.velocity += self.acceleration
        #limit
        if np.linalg.norm(self.velocity) > self.max_speed:
            self.velocity = self.velocity / np.linalg.norm(self.velocity) * self.max_speed

        self.acceleration = Vector(*np.zeros(2))
        # print(self.position)  # To show the position at the console


    def apply_behaviour(self, boids):
        alignment = self.align(boids)
        cohesion = self.cohesion(boids)
        separation = self.separation(boids)

        self.acceleration += alignment
        self.acceleration += cohesion
        self.acceleration += separation

    def edges(self):
        if self.position.x > self.width:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = self.width

        if self.position.y > self.height:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = self.height

    def align(self, boids):
        steering = Vector(*np.zeros(2))
        total = 0
        avg_vector = Vector(*np.zeros(2))
        for boid in boids:
            if np.linalg.norm(boid.position - self.position) < self.perception:
                avg_vector += boid.velocity
                total += 1
        if total > 0:
            avg_vector /= total
            avg_vector = Vector(*avg_vector)
            avg_vector = (avg_vector / np.linalg.norm(avg_vector)) * self.max_speed
            steering = avg_vector - self.velocity

        return steering

    def cohesion(self, boids):
        steering = Vector(*np.zeros(2))
        total = 0
        center_of_mass = Vector(*np.zeros(2))
        for boid in boids:
            if np.linalg.norm(boid.position - self.position) < self.perception:
                center_of_mass += boid.position
                total += 1
        if total > 0:
            center_of_mass /= total
            center_of_mass = Vector(*center_of_mass)
            vec_to_com = center_of_mass - self.position
            if np.linalg.norm(vec_to_com) > 0:
                vec_to_com = (vec_to_com / np.linalg.norm(vec_to_com)) * self.max_speed
            steering = vec_to_com - self.velocity
            if np.linalg.norm(steering)> self.max_force:
                steering = (steering /np.linalg.norm(steering)) * self.max_force

        return steering

    def separation(self, boids):
        steering = Vector(*np.zeros(2))
        total = 0
        avg_vector = Vector(*np.zeros(2))
        for boid in boids:
            distance = np.linalg.norm(boid.position - self.position)
            if self.position != boid.position and distance < self.perception:
                diff = self.position - boid.position
                diff /= distance
                avg_vector += diff
                total += 1
        if total > 0:
            avg_vector /= total
            avg_vector = Vector(*avg_vector)
            if np.linalg.norm(steering) > 0:
                avg_vector = (avg_vector / np.linalg.norm(steering)) * self.max_speed
            steering = avg_vector - self.velocity
            if np.linalg.norm(steering) > self.max_force:
                steering = (steering /np.linalg.norm(steering)) * self.max_force

        return steering
    
    #AQUÍ COMIENZA LO DE AGENTES
