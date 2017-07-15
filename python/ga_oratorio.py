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

#SET NUMBER OF DAYS
n_days = 4
activities = None
participants = None
chr_id = 0
DEBUG1 = True

class Ga_oratorio:
    def __init__(self, data="../data/delavnice.csv", pop_size=20, n_phases=10,
                 crossover_chance=0.7, mutation_chance=0.7):
        print("Initializiing ga_oratorio with population size: %d." % (pop_size))

        self.pop_size = pop_size
        self.n_phases = n_phases
        self.crossover_chance = crossover_chance
        self.mutation_chance = mutation_chance

        self.day_plan = []  # build at the end

        self.best_chromosome = None

        global participants
        global activities
        participants, activities = data_reader.read_data17(data)
        #print (self.activities)
        #print (self.participants)

        self.population = []
        self.init_population()

    def init_population(self):
        print("Initializing population:")
        for i in range(self.pop_size):
            chrm = Chromosome(participants=participants)
            self.population += [chrm]

    def calc_pop_fitnesses(self):
        all_fit = []
        all_sum = 0
        for chromosome in self.population:
            f = chromosome.fitness
            all_fit += [f]
            all_sum += f
            if self.best_chromosome is None:
                self.best_chromosome = chromosome
            elif f < self.best_chromosome.fitness:
                self.best_chromosome = copy.deepcopy(chromosome)
        avg = all_sum/len(all_fit)
        """
        for f in sorted(all_fit):
            print (f)
        print ("------")
        """
        return (all_fit, avg)

    def evolve(self):
        phase = 0
        print("Begin evolving.")
        pop_fit,avg_fit = self.calc_pop_fitnesses()
        while phase < self.n_phases:

            #testing:
            #pop_fit = [ 26,73,3,78,43,13 ] 

            #sorted indices from best fitness (lowest variance) to worst fitness
            sorted_fit = [ y[0] for y in sorted(enumerate(pop_fit), key=lambda x:x[1]) ]
            #print (pop_fit)
            #print (sorted_fit)

            # pick chromosomes for crossover
            cross_sel = self.roulette_select(pop_fit, self.crossover_chance)
            #print (cross_sel)

            #perform crossover
            new_population = []
            n_added = 0
            for i in cross_sel:
                # randomly pick another one from cross_sel and cross
                j = cross_sel[randy_marsh() % len(cross_sel)]
                if i == j:
                    continue    #don't crossover same chromosome
                
                new_2_chromosomes = self.population[i].crossover( self.population[j] )
                if new_2_chromosomes[0].fitness < self.population[i].fitness and new_2_chromosomes[0].fitness < self.population[j].fitness:
                    new_population += [new_2_chromosomes[0]]
                    n_added += 1
                if new_2_chromosomes[1].fitness < self.population[i].fitness and new_2_chromosomes[1].fitness < self.population[j].fitness:
                    new_population += [new_2_chromosomes[1]]
                    n_added += 1

            #print ("len_pop: %d, n_added: %d" % ( len(self.population), n_added) )
            #remove some bad chromosomes
            if n_added > 0:
                new_population += [ self.population[x] for x in sorted_fit[:-n_added] ]
                self.population = new_population

            #mutate random chromosomes (leave best intact)
            pl = len(self.population)
            for i in range(math.ceil(pl*self.mutation_chance)):
                #pick random and mutate
                ridx = randy_marsh()%pl
                if self.population[ridx].id is not self.best_chromosome.id:
                    self.population[ridx].mutate

            pop_fit,avg_fit = self.calc_pop_fitnesses()
            print("End of phase: %4d\t|\tbest_chromosome: %d (%3.3f)\t|\tavg fitness: %3.3f" % 
                    (phase, self.best_chromosome.id, self.best_chromosome.fitness, avg_fit))
            phase += 1
        print("Evolution concluded.")

    def build_day_plan(self):
        self.day_plan = []
        for i in range(n_days):
            self.day_plan += [[]]
            for j,a in enumerate(activities):
                self.day_plan[i] += [[]]

        bc = self.best_chromosome
        for person in bc.chromosome:
            for i,act in enumerate(person["activities"]):
                self.day_plan[i][act] += [ "{}-{}".format(person["grade"],
                    person["name"]) ]

        #print (self.day_plan[0])

    def export_data(self, outfilepath):
        self.build_day_plan()

        with open(outfilepath, 'w') as csvfile:
            spamwriter = csv.writer(
                csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            header = []
            for d in range (n_days):
                header += [ "Dan {}: {}".format(d, x["name"]) for x in activities ]
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

    def roulette_select(self, ftns, pcnt):
        # input: chromosome fitnesses, output: indices of surviving chromosomes
        # fitness closer to 0: better
        # fitness is POSITIVE, you want to minimize it
        s = max(ftns)
        # subtract every value from s to invert importance
        ftns[:] = [pow(1 - x / s, 2) for x in ftns] #pow to increase difference
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


class Chromosome:
    def __init__(self, participants=None, chromosome=None):
        global chr_id
        self.id = chr_id
        chr_id += 1
        if chromosome is not None:
            self.chromosome = copy.deepcopy(chromosome)
        elif participants is not None:
            self.chromosome = self.init_chromosome(participants)
        else:
            raise Exception("Need more data to initalize a chromosome.")

        self.fitness = 9999999
        self.update_fitness()

    def short_print(self):
        print ("[%4d] (%3.3f)" % (self.id, self.fitness) )
        if not self.chromosome:
            l = "Empty"
        else:
            l = [ p["id"] for p in self.chromosome ]
        print (l)

    def init_chromosome(self, participants):
        # creates a random chromosome
        chromosome = []
        for i, participant in enumerate(participants):
            p1 = copy.deepcopy(participant)
            #fill activities
            #since index == activity, sort indices by scores
            top_choices = [ y[0] for y in sorted(enumerate(p1["pref"]),
                key=lambda x:x[1]) ]
            p1["activities"] = top_choices[:n_days] 
            random.shuffle(p1["activities"])
            chromosome += [p1]
        return chromosome

    def update_fitness (self, gsv_weight=1, aigv_weight=1):
        # build groups
        groups = []
        for day in range(n_days):
            groups += [[]]
            for activity in range(len(activities)):
                groups[day] += [[]]
        for person in self.chromosome:
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
        self.fitness = f
        return f

    def mutate(self):
        #print ("Mutating %d." % self.id)
        # select random child, swap two items in his activities
        r = randy_marsh() % len(self.chromosome)
        random.shuffle(self.chromosome[r]["activities"])
        self.update_fitness()

    def crossover(self, chromosome2, prnt=False):
        r = randy_marsh() % len(self.chromosome)
        ret1 = self.chromosome[:r] + chromosome2.chromosome[r:]
        chr1 = Chromosome (chromosome=ret1)
        ret2 = chromosome2.chromosome[:r] + self.chromosome[r:]
        chr2 = Chromosome (chromosome=ret2)
        if prnt and self.id == chromosome2.id:
            print ("Crossover::Self.fitness: %f, c2.fitness: %f, r1.fitness: %f, r2.fitness: %f." % (self.fitness, chromosome2.fitness, chr1.fitness, chr2.fitness))
        return (chr1, chr2)

if __name__ == "__main__":
    ga = Ga_oratorio(data="../data/delavnice_2017.csv", pop_size=50, n_phases=3, crossover_chance=0.9, mutation_chance=0.9)

    ga.evolve()
    for x in ga.best_chromosome.chromosome:
        print ("{:20s}: {}".format(x["name"], x["activities"]))
    ga.build_day_plan()
    for d,day in enumerate(ga.day_plan):
        for a,act in enumerate(day):
            print ("Day {} - {}:\n{}".format(d,activities[a]["name"],act))
    ga.export_data("../data/delavnice_2017_out.csv")

    # ga.fitness(ga.population[0])
    #ga.roulette_select([-30, -50, -1, -20, -70], 5)
    #ch = ga.init_chromosome()
    # ga.mutation(ch)

"""
    test1 = [5,4,7,9,1]
    test2 = [3,6,5,1,3]
    test1 = test2
    print (test1)
    print (test2)
    r = randy_marsh() % len(test1)
    ret1 = test1[:r] + test2[r:]  
    ret2 = test2[:r] + test1[r:] 
    print ("--- %d ---" % r)
    print (ret1)
    print (ret2)
"""

