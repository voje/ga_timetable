#!/usr/bin/python
import sys
import os
import math
import csv
import random
import statistics
import copy
import logging

log = logging.getLogger(__name__)

# add script folder to path for imports
full_path = os.path.abspath(os.path.dirname(sys.argv[0]))
sys.path.append(full_path)


class GeneticAlg:
    def __init__(self, par, act, ndays):
        self.par = par
        self.act = act
        self.NDAYS = ndays


def randy_marsh():
    return int.from_bytes(os.urandom(4), byteorder="big")

# SET NUMBER OF DAYS
activity_max = 0
grouped = {}
chr_id = 0
DEBUG1 = True
global g_w1
global g_w2

class Ga_oratorio:
    def __init__(self, data="../data/delavnice.csv", pop_size=20, n_phases=10,
                 crossover_chance=0.7, mutation_chance=0.7):

        global participants
        global activities
        global grouped
        global activity_max

        print("Initializiing ga_oratorio with population size: %d." % (pop_size))

        self.pop_size = pop_size
        self.n_phases = n_phases
        self.crossover_chance = crossover_chance
        self.mutation_chance = mutation_chance

        self.day_plan = []  # build at the end

        self.best_chromosome = None

        participants, activities = data_reader.read_data17(data)

        activity_max = math.floor ( len(participants) / len(activities) * n_days )

        self.group_participants(["Neža Klemenčič", "Eva Klemenčič", "Zala Bertoncelj"]) #fine tuning (some participants want to be together)
        self.group_participants(["Jan Potočnik", "Urban Porenta"])
        self.group_participants(["Neja Potočnik", "Iza Šink", "Nika Krmelj"])
        self.group_participants(["Anja Hadalin ", "Karmen Logonder"])
        """
        for key in grouped:
            for par in participants:
                if par["id"] == key:
                    print (par)
            print ("{}{}".format(key, grouped[key]))
        """

        #print (self.activities)
        #print (self.participants)

        self.population = []
        self.init_population()

    # group_participants and return_groups take care of participants that wish to be together (they handle them as one)
    def group_participants(self, names):
        global participants
        global grouped

        #!! this means the participants will go to same
        #!! activities as the first one in names
        pp = []
        for name in names:
            for i,par in enumerate(participants):
                if par["name"] == name:
                    pp += [par]
                    participants.remove(par)
        #check for same activities
        grades = [ x["grade"] for x in pp ]
        grp = {
            "id": pp[0]["id"],
            "name": "grp_{}".format(pp[0]["id"]),
            "grade": sum(grades)/len(grades),
            "count": len(pp),
            "pref": pp[0]["pref"],
            "activities": pp[0]["activities"]
                }
        grouped[pp[0]["id"]] = pp
        participants += [grp]

    def return_groups(self, chromo):
        global grouped
        for key in grouped:
            for par in chromo.chromosome:
                if par["id"] == key:
                    #replace group with participants, keep activities
                    for p in grouped[key]:
                        p["activities"] = par["activities"]
                    chromo.chromosome.remove(par)
                    chromo.chromosome += grouped[key]
                    break
        return chromo

        for participant in chromo.chromosome:
            if participant["id"] in grouped:
                saved_id = participant["id"]
                #put activities into participans, saved in goruped
                for saved_p in grouped[saved_id]:
                    saved_p["activities"] = participant["activities"]
                chromo.chromosome.remove(participant)
                chromo.chromosome += grouped[saved_id]
                del grouped[saved_id]
                #print ( ["--{}".format(p["name"]) for p in chromo.chromosome ] )
        return chromo

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
        bc = self.return_groups( bc )
        for person in bc.chromosome:
            for i,act in enumerate(person["activities"]):
                self.day_plan[i][act] += [ "{}-{}".format(person["grade"],
                    person["name"]) ]

    def export_data(self, outfilepath):
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
        global activities
        # reset counter
        for a in activities:
            a["count"] = 0

        # creates a random chromosome
        chromosome = []
        for i, participant in enumerate(participants):
            p1 = copy.deepcopy(participant)

            # in p1["pref"], we have activity ids [1,2,...] sorted by preference
            # since our representation starts with [0,1,...], we need to -1 every id
            acts = []
            day = 0
            for act in p1["pref"]:
                act_id = act-1
                if day == n_days:
                    break
                if activities[act_id]["count"] >= activity_max:
                    continue
                activities[act_id]["count"] += 1
                acts += [act_id]
                day += 1
            p1["activities"] = copy.deepcopy(acts)

            random.shuffle(p1["activities"])
            chromosome += [p1]

        #print (chromosome)
        return chromosome

    def update_fitness (self, gsv_weight=1, aigv_weight=1):
        gsv_weight = g_w1
        aigv_weight = g_w2

        # build groups
        groups = []
        for day in range(n_days):
            groups += [[]]
            for activity in range(len(activities)):
                groups[day] += [[]]
        for person in self.chromosome:
            for day, act in enumerate(person["activities"]):
                groups[day][act] += [person]

        # group size variance
        grp_sizes = []
        for day in groups:
            for act in day:
                grp_sizes += [sum([person["count"] for person in act])]
        gsv = statistics.variance(grp_sizes)

        # average intragroup grade(age) variance
        aigv = 0
        count = 0
        for day in groups:
            for act in day:
                if len(act) < 2:
                    continue
                aigv += statistics.variance([ person["grade"] for person in act ])
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
    # Inside class __init__ set groups of participants that want to be together
    # Set global variable n_days

    g_w1 = 1
    g_w2 = 0 
    for rep in range(1): 
        n_days = 4
        activities = None
        participants = None
        grouped = {}
        chr_id = 0
        DEBUG1 = True

        ga = Ga_oratorio(data="../data/delavnice_2017.csv", pop_size=50, n_phases=300, crossover_chance=0.7, mutation_chance=0.3)

        ga.evolve()
        ga.build_day_plan()

        for x in ga.best_chromosome.chromosome:
            print ("{:20s}: {}".format(x["name"], x["activities"]))

        for d,day in enumerate(ga.day_plan):
            for a,act in enumerate(day):
                print ("Day {} - {}:\n{}".format(d,activities[a]["name"],act))

        ga.export_data("../data/out_{}.csv".format(rep))

        g_w1 -= 0.1
        g_w2 += 0.1
        









