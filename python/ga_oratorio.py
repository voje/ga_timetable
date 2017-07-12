#!/usr/bin/python
import sys
import os
import math
import csv
import random
import statistics

# add script folder to path for imports
full_path = os.path.abspath(os.path.dirname(sys.argv[0]))
sys.path.append(full_path)

def randy_marsh():
    return int.from_bytes(os.urandom(4), byteorder="big")

class ga_oratorio:

    def __init__(self, pop_size=20, data="../data/delavnice.csv"):
        print("Initializiing ga_oratorio with population size: %d." % (pop_size))
        self.pop_size = pop_size

        self.activities = []
        self.participants = {}
        # 'John Doe': {'id': 24, 'grade': '7', 'activities': [9, 10, 0, 2]}
        self.population = []
        
        self.read_data(data)
        self.init_population()
        self.n_days = len((self.population[0][0]["activities"]))

    def read_data(self, path):
        par_id = 0
        with open(path, "r") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            for row in reader:
                if not self.activities:
                    # if activities is uninitiated (first row of file)
                    for i in range(0, len(row)):
                        self.activities += [{
                            "id": i,
                            "name": row[i],
                            "count": 0}]
                else:
                    # else, add to participants
                    for i in range(0, len(row)):
                        tmps = row[i]
                        sp = tmps.split(" ")
                        if (len(sp) < 2):
                            continue  # empty cell

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
                            self.participants[name][
                                "activities"] += [activity_id]

                        # update count in self.activities
                        self.activities[i]["count"] += 1

    def init_chromosome(self):
        # creates a random chromosome
        chromosome = [None] * len(self.participants)  # preinit the list
        for name in self.participants:
            p1 = self.participants[name]
            random.shuffle(p1["activities"])
            chromosome[p1["id"]] = p1
        return chromosome

    def init_population(self):
        for i in range(0, self.pop_size):
            self.population += [self.init_chromosome()]

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
            r = randy_marsh() % wheel[-1]
            # pick a chromosome
            idx = 0
            for j in range(0, len(wheel)):
                idx = j
                if r < wheel[j]:
                    break
            surv_ids += [idx]
        print(surv_ids)
        return surv_ids

    def crossover(self, chromosome1, chromosome2):
        r = randy_marsh() % len(chromosome1)
        ret1 = chromosome1[:r] + chromosome2[r:]
        ret2 = chromosome2[:r] + chromosome1[r:]
        return (ret1, ret2)

    def mutation(self, chromosome):
        #select random child, swap two items in his activities
        r = randy_marsh() % len(chromosome)
        print ("mutating")
        print (chromosome[r])
        random.shuffle(chromosome[r]["activities"])
        print (chromosome[r])

    def fitness(self, chromosome, gsv_weight=1, aigv_weight=1):
        #build groups
        groups = []
        for day in range(self.n_days):
            groups += [[]]
            for activity in range(len(self.activities)):
                groups[day] += [[]] 
        for person in chromosome:
            for day,act in enumerate(person["activities"]):
                groups[day][act] += [person["grade"]]

        #group size variance
        grp_sizes = []
        for i in groups:
            for j in i:
                grp_sizes += [len(j)]
        gsv = statistics.variance(grp_sizes)

        #average intragroup grade(age) variance
        aigv = 0
        count = 0
        for i in groups:
            for j in i:
                aigv += statistics.variance(j)
                count += 1
        aigv = aigv/count

        #print(gsv)
        #print(aigv)
        return gsv*gsv_weight + aigv*aigv_weight
    

if __name__ == "__main__":
    ga = ga_oratorio()

    ga.fitness(ga.population[0])
    #ga.roulette_select([-30, -50, -1, -20, -70], 5)
    #ch = ga.init_chromosome()
    #ga.mutation(ch)
