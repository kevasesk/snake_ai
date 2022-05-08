import numpy as np
import random, math, sys

population = 10
currentGeneration = 0
individuals = []
newIndividuals = []

def activationFunction(x):
  #sigmoid
  #return 1 / (1 + math.exp(-x))
  return max(0, x)


def activationFunctionList(list):
    for i in range(len(list)):
        list[i] = activationFunction(list[i])
    return list


def normalize(field):
    field = np.array(field)
    field = field.flatten()
    field = activationFunctionList(field)
    return field


def networkInit(input, hidden1, output_count):
    input = normalize(input)
    w1 = np.random.rand(len(input), hidden1)
    z1 = activationFunctionList(np.matmul(input, w1))
    w2 = np.random.rand(hidden1, output_count)
    output = activationFunctionList(np.matmul(z1, w2))
    direction = np.argmax(output) + 1
    return {
        'w1': w1,
        'w2': w2,
        'direction': direction
    }

def networkBuild(input, w1, w2):
    input = normalize(input)
    z1 = activationFunctionList(np.matmul(input, w1))
    output = activationFunctionList(np.matmul(z1, w2))
    direction = np.argmax(output) + 1
    return {
        'w1': w1,
        'w2': w2,
        'direction': direction
    }

def involve(individualMothers, individualFathers):
    global newIndividuals
    for index, indiv in individualMothers:
        genType = random.randint(1, 3)
        if genType == 1:
            genVariantW1 = individualMothers[index]['w1']
            genVariantW2 = individualMothers[index]['w2']
        if genType == 2:
            genVariantW1 = individualFathers[index]['w1']
            genVariantW2 = individualFathers[index]['w2']
        if genType == 3:
            genVariantW1 = random.random()
            genVariantW2 = random.random()
        newIndividuals.append({
            'w1': genVariantW1,
            'w2': genVariantW2
        })

def nextGeneration():
    global currentGeneration, newIndividuals
    currentGeneration += 1
    individualMothers = []
    individualFathers = []
    newIndividuals = []
    for index, individual in enumerate(individuals):
        if index % 2 == 0:
            individualMothers.append(individual)
        else:
            individualFathers.append(individual)
    involve(individualMothers, individualFathers)
    involve(individualMothers, individualFathers)





