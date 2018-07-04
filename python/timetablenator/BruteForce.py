import logging
from time import time
import numpy as np

log = logging.getLogger(__name__)


class BruteForce:
    def __init__(self, par, act, ndays):
        self.par = par
        self.act = act
        self.NDAYS = ndays
        self.days = []

    def init_days(self):
        self.days = [[] for x in range(self.NDAYS)]
        for d in self.days:
            d.extend([{"par": []} for x in range(len(self.act))])

    def get_activity(self, day_id, act_id):
        return self.days[day_id][act_id]

    def calc_group_variance(self, new_par, day_id, act_id):
        activity = self.get_activity(day_id, act_id)
        school_grades = [x["grade"] for x in activity["par"]]
        return np.var(school_grades + [new_par["grade"]])

    def run(self):
        log.info("Running BruteForce.")
        tstart = time()
        self.init_days()
        # pick a participant, look at his wish,
        # drop him into an activity
        for pa in self.par:
            filled_days = []
            for act_id in pa["pref"][:(self.NDAYS)]:
                best_day_score = 9000
                best_day_id = -1
                for day_id in range(len(self.days)):
                    if day_id in filled_days:
                        continue
                    # drop in the participand and check score
                    variance_score = self.calc_group_variance(
                        pa, day_id, act_id)
                    if variance_score < best_day_score:
                        best_day_score = variance_score
                        best_day_id = day_id
                activity = self.get_activity(best_day_id, act_id)
                activity["par"].append(pa)
                filled_days.append(best_day_id)
        log.info("Finished running BruteForce in {:.2f}s".format(
            time() - tstart))
