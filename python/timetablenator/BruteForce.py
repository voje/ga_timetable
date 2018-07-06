import logging
from time import time
import numpy as np
import random
from copy import deepcopy as DC

log = logging.getLogger(__name__)
random.seed(time())


class BruteForce:
    def __init__(self, par, act, ndays):
        self.par = par
        self.act = act
        self.NDAYS = ndays
        self.days = []
        self.avg_grp_size = 1.0 * len(self.par) / len(self.act)
        self.best_pop_score = 9000
        self.best_pop = None

    def init_days(self):
        self.days = [[] for x in range(self.NDAYS)]
        for d in self.days:
            d.extend([{"par": []} for x in range(len(self.act))])

    def get_activity(self, day_id, act_id):
        return self.days[day_id][act_id]

    def calc_grade_variance(self, new_par, day_id, act_id):
        # grade (age) variance should be minimized
        activity = self.get_activity(day_id, act_id)
        school_grades = [x["grade"] for x in activity["par"]]
        variance = np.var(school_grades + [new_par["grade"]])
        return variance

    def calc_population_score(self):
        grp_sizes = []
        age_variances = []
        for day in self.days:
            for act in day:
                grp_sizes.append(len(act["par"]))
                age_variances.append(np.var(
                    [x["grade"] for x in act["par"]]))
        avg_grade_var = np.average(age_variances)
        size_var = np.var(grp_sizes)
        # log.debug(
        #    "\navg_grade_var: {}\n"
        #    "size_var: {}\n".format(
        #        avg_grade_var, size_var)
        # )
        return avg_grade_var + size_var

    def run(self):
        log.info("Running BruteForce.")
        tstart = time()
        self.init_days()
        # pick a participant, look at his wish,
        # drop him into an activity

        try_shuffling = False

        for i in range(0, 1000):
            self.init_days()
            # Order of adding participants !!!
            if try_shuffling:
                random.shuffle(self.par)
            for pa in self.par:
                filled_days = []
                for act_id in pa["pref"][:(self.NDAYS)]:
                    best_day_score = 9000
                    best_day_id = -1
                    for day_id in range(len(self.days)):
                        if day_id in filled_days:
                            continue
                        # drop in the participant and check score
                        group_score = self.calc_grade_variance(
                            pa, day_id, act_id)
                        if group_score < best_day_score:
                            best_day_score = group_score
                            best_day_id = day_id
                    activity = self.get_activity(best_day_id, act_id)
                    activity["par"].append(pa)
                    filled_days.append(best_day_id)
            pop_score = self.calc_population_score()
            log.info("[{:>3}] pop_score: {:.2f}".format(
                i, pop_score))
            if pop_score < self.best_pop_score:
                self.best_pop_score = pop_score
                self.best_pop = DC(self.days)
            if not try_shuffling:
                break
        log.info("Finished running BruteForce in {:.2f}s".format(
            time() - tstart))
        log.info("Winning pop_score: {:.2f}.".format(self.best_pop_score))
