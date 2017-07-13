#!/usr/bin/python
import sys
import os
import math
import csv
import random
import statistics
import copy

# add script folder to path for imports
full_path = os.path.abspath(os.path.dirname(sys.argv[0]))
sys.path.append(full_path)

import data_reader


def randy_marsh():
    return int.from_bytes(os.urandom(4), byteorder="big")


class ga_oratorio:

    def __init__(self, data="../data/delavnice.csv", pop_size=20, n_phases=10,
                 crossover_chance=0.7, mutation_chance=0.7, n_days=4):
        print("Initializiing ga_oratorio with population size: %d." % (pop_size))
        self.n_days = n_days    #spread activities over n days
        self.pop_size = pop_size
        self.n_phases = n_phases
        self.crossover_chance = crossover_chance
        self.mutation_chance = mutation_chance

        self.day_plan = []  # build at the end
        self.population = []    #all of the chromosomes
        self.best_fitness = sys.maxsize
        self.best_chromosome = None

        self.participants, self.activities = data_reader.read_data17(data)
        print (self.activities)
        print (self.participants)
        self.init_population()

    def calc_pop_fitnesses(self):
        fitnesses = []
        for chromosome in self.population:
            f = self.fitness(chromosome)
            fitnesses += [f]
            if f < self.best_fitness:
                self.best_chromosome = copy.deepcopy(chromosome)
        #print (fitnesses)
        return fitnesses

    def calc_best_fitness(self):
        best = sys.maxsize
        idx = -1
        for i, chromosome in enumerate(self.population):
            f = self.fitness(chromosome)
            if f < best:
                idx = i
                best = f
        return (idx, best)


    def evolve(self):
        phase = 0
        print("Begin evolving.")
        while phase < self.n_phases:
            pop_fitnesses = self.calc_pop_fitnesses()
            # pick chromosomes for crossover
            cross_sel = self.roulette_select(pop_fitnesses,
                                             self.crossover_chance)
            # sorted indices for fitness
            sorted_fit_idcs = [i[0] for i in sorted(
                enumerate(pop_fitnesses), key=lambda x:x[1])]
            # new population excludes len(cross_sel) worst chromosomes
            new_population = [self.population[x]
                              for x in sorted_fit_idcs[len(cross_sel):]]
            # add len(cross_sel) with crossover
            for i in cross_sel:
                # randomly pick another one from cross_sel and cross
                j = cross_sel[randy_marsh() % len(cross_sel)]
                new_2_chromosomes = self.crossover(
                    self.population[i], self.population[j])
                # pick one and add him to new_population
                new_population += [new_2_chromosomes[randy_marsh() % 2]]

            for i in range(math.floor(100 * self.mutation_chance)):
                if randy_marsh() % 100 > self.mutation_chance * 100:
                    self.mutation(
                        new_population[randy_marsh() % len(new_population)])
            self.population = new_population
            bf = self.calc_best_fitness()
            print("End of phase: %d\t|\tbest_fitness: %f" % (phase, bf[1]))
            phase += 1
        print("Evolution concluded.")

    def build_day_plan(self):
        for i in range(self.n_days):
            self.day_plan += [[]]
            for j,a in enumerate(self.activities):
                self.day_plan[i] += [[]]

        bc = self.best_chromosome
        for person in bc:
            for i,act in enumerate(person["activities"]):
                self.day_plan[i][act] += [ "{}-{}".format(person["grade"],
                    person["name"]) ]

        print (self.day_plan[0])

    def export_data(self, outfilepath):
        self.build_day_plan()

        with open(outfilepath, 'w') as csvfile:
            spamwriter = csv.writer(
                csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            header = [x["name"] for x in self.activities] * self.n_days
            spamwriter.writerow(header)

            stop = False
            row = 0
            while not stop:
                out_row = []
                stop = True
                for day in self.day_plan:
                    for act in day:
                        if row < len(act):
                            stop = False
                            out_row += [act[row]]
                        else:
                            out_row += ["/"]
                spamwriter.writerow(out_row)
                row += 1
        print("Finished writing to file: %s" % outfilepath)

    def init_chromosome(self):
        # creates a random chromosome
        chromosome = [None] * len(self.participants)  # preinit the list
        for i, name in enumerate(self.participants):
            p1 = copy.deepcopy(self.participants[name])
            random.shuffle(p1["activities"])
            chromosome[p1["id"]] = copy.deepcopy(p1)
        return chromosome

    def init_population(self):
        print("Initializing population:")
        self.population = []
        for i in range(self.pop_size):
            chrm = self.init_chromosome()
            self.population += [chrm]

    def roulette_select(self, ftns, pcnt):
        # input: chromosome fitnesses, output: indices of surviving chromosomes
        # fitness closer to 0: better
        # TODO fitness is POSITIVE, you want to minimize it
        s = max(ftns)
        # subtract every value from s to invert importance
        ftns[:] = [1 - x / s for x in ftns]
        # print(ftns)

        # create roulette_wheel
        ss = 0
        wheel = []
        for n in ftns:
            ss = ss + n
            wheel += [ss]
        # print(wheel)

        sel_ids = []
        # pcnt == percentage of survivers
        surv = math.ceil(len(ftns) * pcnt)
        #print ("from %d, pick %f survivers: %d" % (len(ftns), pcnt, surv))
        # return i survivers
        for i in range(0, surv):
            # random
            r = (randy_marsh() % 100) / 100 * wheel[-1]
            # pick a chromosome
            idx = 0
            for j in range(0, len(wheel)):
                idx = j
                if r < wheel[j]:
                    break
            sel_ids += [idx]
        # print(sel_ids)
        return sel_ids

    def crossover(self, chromosome1, chromosome2):
        r = randy_marsh() % len(chromosome1)
        ret1 = chromosome1[:r] + chromosome2[r:]
        ret2 = chromosome2[:r] + chromosome1[r:]
        return (ret1, ret2)

    def mutation(self, chromosome):
        # select random child, swap two items in his activities
        r = randy_marsh() % len(chromosome)
        random.shuffle(chromosome[r]["activities"])

    def fitness(self, chromosome, gsv_weight=1, aigv_weight=1):
        # build groups
        groups = []
        for day in range(self.n_days):
            groups += [[]]
            for activity in range(len(self.activities)):
                groups[day] += [[]]
        for person in chromosome:
            for day, act in enumerate(person["activities"]):
                groups[day][act] += [person["grade"]]

        # group size variance
        grp_sizes = []
        for i in groups:
            for j in i:
                grp_sizes += [len(j)]
        gsv = statistics.variance(grp_sizes)

        # average intragroup grade(age) variance
        aigv = 0
        count = 0
        for i in groups:
            for j in i:
                if (len(j) < 2):
                    continue
                aigv += statistics.variance(j)
                count += 1
        aigv = aigv / count

        # print(gsv)
        # print(aigv)
        f = gsv * gsv_weight + aigv * aigv_weight
        return f


if __name__ == "__main__":
    ga = ga_oratorio(data="../data/delavnice_2017.csv", pop_size=100, n_phases=30,
                     crossover_chance=0.7, mutation_chance=0.7)
    ga.evolve()

    #ga.build_day_plan()
    ga.export_data("../data/delavnice_2017_out.csv")

    # ga.fitness(ga.population[0])
    #ga.roulette_select([-30, -50, -1, -20, -70], 5)
    #ch = ga.init_chromosome()
    # ga.mutation(ch)
