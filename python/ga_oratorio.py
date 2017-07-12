#!/usr/bin/python
import sys
import os
import math
import csv
import random

# add script folder to path for imports
full_path = os.path.abspath(os.path.dirname(sys.argv[0]))
sys.path.append(full_path)

import test


class ga_oratorio:
    def __init__(self):
        print("Initializiing ga_oratorio")
        self.activities = []
        self.participants = {} # 'John Doe': {'id': 24, 'grade': '7', 'activities': [9, 10, 0, 2]}

    def read_data(self, path):
        par_id = 0
        with open(path, "r") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            for row in reader:
                if not self.activities:
                    #if activities is uninitiated (first row of file)
                    for i in range(0, len(row)):
                        self.activities += [{
                                "id": i,
                                "name": row[i], 
                                "count": 0}]
                else:
                    #else, add to participants
                    for i in range(0, len(row)):
                        tmps = row[i]
                        sp = tmps.split(" ")
                        if (len(sp) < 2):
                            continue    #empty cell

                        grade = int(sp[0])
                        name = " ".join(sp[1:])
                        activity_id = i
                        
                        if name not in self.participants:
                            self.participants[name] = {
                                    "id": par_id,
                                    "name": name,
                                    "grade": grade,
                                    "activities": [activity_id]}
                            par_id += 1
                        else:
                            self.participants[name]["activities"] += [activity_id]

                        #update count in self.activities
                        self.activities[i]["count"] += 1

    def init_chromosome():
        #creates a random chromosome
        chromosome = []
        for name in self.participants:
            p1 = self.participants[name]
            random.shuffle(p1["activities"])
            chromosome[p1["id"]] = p1
        return chromosome

    def roulette_select(self, ftns, pcnt):
        # input: chromosome fitnesses, output: indices of surviving chromosomes
        # fitness closer to 0: better
        # smaller values should have a bigger chunk; invert (val = 1-val)
        s = min(ftns)
        # subtract every value from s to invert importance
        ftns[:] = [1 - x / s for x in ftns]
        print(ftns)

        # create roulette_wheel
        ss = 0
        wheel = []
        for n in ftns:
            ss = ss + n
            wheel += [ss]
        print(wheel)

        surv_ids = []
        # pcnt == percentage of survivers
        surv = math.ceil(len(ftns) * pcnt)
        # return i survivers
        for i in range(0, surv):
            # random
            r = (int.from_bytes(os.urandom(4), byteorder="big")) % wheel[-1]
            # pick a chromosome
            idx = 0
            for j in range(0, len(wheel)):
                idx = j
                if r < wheel[j]:
                    break
            surv_ids += [idx]
        print(surv_ids)
        return surv_ids

    def crossover(chromosome1, chromosome2):
        print ("TODO")    
        
class chromosome:
    def __init__(self):
        print("hello, chromosome")

    def fitness():
        print("fitness")


if __name__ == "__main__":
    ga = ga_oratorio()
    ga.read_data("../data/delavnice.csv")   #todo path
    #ga.roulette_select([-30, -50, -1, -20, -70], 5)








