import random
from Project import *


class Chromosome:
    def __init__(self, list, fitness):
        self.list = list
        self.fitness = fitness

    def __str__(self):
        for l in self.list:
            print(Project.__str__(l))
        print("Fitness" + str(self.getFitness()))

    def getFitness(self):
        return self.fitness

    def getList(self):
        return self.list


