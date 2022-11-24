# TC2008B. Sistemas Multiagentes y Gráficas Computacionales
# Python flask server to interact with Unity. Based on the code provided by Sergio Ruiz.
# Octavio Navarro. November 2022

from flask import Flask, request, jsonify
from boids.boid import Boid
import numpy as np
import mesa
import random
import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

global posi
vec = []
class CarAgent1(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.nombre = unique_id  
        #self.empty_neighbors = [c for c in self.neighborhood if self.model.grid.is_cell_empty(c)]
    def step(self):
        self.schedule.step()

class CarModel(mesa.Model):
    def __init__(self,N,width,height):
        self.numAgentsCar = N
        self.grid = mesa.space.MultiGrid(width,height,True)
        self.schedule = mesa.time.BaseScheduler(self)
        self.running = True
        for i in range(self.numAgentsCar):
            a = CarAgent1(i,self)
            self.schedule.add(a)
            x = vec[i][0]
            y = vec[i][1]
            self.grid.place_agent(a,(x,y))
    def step(self):
        self.schedule.step()

#Actualizando posiciones
def updatePositions(flock):
    positions = []
    for boid in flock:
        #Aplicando comportamientos de física
        boid.apply_behaviour(flock)
        boid.update()
        boid.edges()
        positions.append((boid.id, boid.position))
    return positions

#Convirtiendo posiciones a JSon

def positionsToJSON(positions):
    posDICT = []
    for id, p in positions:
        pos = { 
            "boidId" : str(id),#ID de cada agente
            "x" : float(p.x), #Posición en X del agente
            "y" : float(p.z), #Posición en Y del agente
            "z" : float(p.y) #Posición en Z del agente
        }
        posDICT.append(pos) #Guardando en un vector la posición de cada agente 
    return jsonify({'positions':posDICT}) #Devolviendo un json de posiciones, en el viene la posición de cada agente

# Tamaño del tablero
width = 30
height = 30

# Set the number of agents here:
flock = []

app = Flask("Boids example")

@app.route('/', methods=['POST', 'GET'])
def boidsPosition():
    if request.method == 'GET':
        positions = updatePositions(flock)
        return positionsToJSON(positions)
    elif request.method == 'POST':
        return "Post request from Boids example\n"

@app.route('/init', methods=['POST', 'GET'])
def boidsInit():
    global flock
    global vec
    if request.method == 'GET':
        #Recibiendo x,y como *np.random.rand, esto ingresa coordenadas aleatorias de posición inicial
        #np.random.rand(2) genera vectores en 2D con valores aleatorias entre [0,1), luego esto se multiplica por 30
        for i in range (5):
            vec.append(random.sample(range(0, 30), 2))
        flock = [Boid(*vec[i], width, height, id) for id in range(5)] #En in range viene el número de agentes, en este caso son 5 agentes
        car_model = CarModel(5,30,30)
        return jsonify({"num_agents":5, "w": 30, "h": 30}) #Enviando como JSON el número de agentes y tamaño del tablero
    elif request.method == 'POST':
        return "Post request from init\n"
#Creación del servidor
if __name__=='__main__':
    app.run(host="localhost", port=8585, debug=True)

