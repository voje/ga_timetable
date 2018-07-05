import numpy as np
import logging
import random
from time import time

log = logging.getLogger(__name__)


class GenAlg:
    def __init__(
        self, par, ndays, population_size,
        mutation_rate, crossover_rate,
        number_of_runs
    ):
        # see CsvReader for format of par
        self.par = par
        self.grades = None
        self.act = None
        self.ND = ndays
        self.PS = population_size
        self.MR = mutation_rate  # % of rows affected by mutate()
        self.CR = crossover_rate  # % of top members to crossover()
        self.NR = number_of_runs
        # sort these together:
        self.matrices = []
        self.gsv_scores = []
        self.aav_scores = []
        self.best_gsv_score = 9000
        self.best_member = None

    def sanity_check(self):
        shape = self.matrices[0].shape
        for M in self.matrices:
            if M.shape != shape:
                log.error("Wrong matrix shape: {}".format(M.shape))
                exit(1)

    def mutate(self, M):
        M1 = M.copy()
        idxs = np.arange(M.shape[0])
        sample = np.random.choice(
            idxs, int(self.MR * M.shape[0]), replace=False)
        for i in sample:
            M1[i, :] = np.random.permutation(M1[i, :])
        return M1

    def apply_mutations(self):
        samp = np.random.choice(
            np.arange(len(self.matrices)), int(self.MR * len(self.matrices)),
            replace=False
        )
        for midx in samp:
            self.matrices.append(self.mutate(self.matrices[midx]))

    def crossover(self, M1, M2):
        spl = np.random.randint(M1.shape[0])
        # log.debug("{}, {}".format(
        #     M1[:spl, :].shape,
        #     M2[spl:, :].shape
        # ))
        return [
            np.vstack([M1[:spl, :], M2[spl:, :]]),
            np.vstack([M2[:spl, :], M1[spl:, :]])
        ]

    def apply_crossovers(self):
        self.update_scores()
        # Scores need to be updated for this.
        nc_max = len(self.matrices) * self.CR
        nc = 0
        gsv_idx = np.argsort(self.gsv_scores)  # ascending
        aav_idx = np.argsort(self.aav_scores)
        # top 10%
        top_ten = int(0.1 * len(self.matrices))
        nc += top_ten
        for i in range(top_ten):
            self.matrices.extend(self.crossover(
                self.matrices[gsv_idx[i]],
                self.matrices[aav_idx[i]]
            ))
        while nc < nc_max:
            pair = np.random.choice(
                np.arange(len(self.matrices)), 2, replace=False)
            self.matrices.extend(self.crossover(
                self.matrices[pair[0]],
                self.matrices[pair[1]]
            ))
            nc += 2

    def culling(self):
        self.update_scores()
        # Remove less fit members.
        # leave best 300 by gsv
        gsv_idx = np.argsort(self.gsv_scores)  # ascending

        self.matrices = [self.matrices[i] for i in gsv_idx]
        self.matrices = self.matrices[:self.PS]

        self.gsv_scores = [self.gsv_scores[i] for i in gsv_idx]
        self.gsv_scores = self.gsv_scores[:self.PS]

        self.aav_scores = [self.aav_scores[i] for i in gsv_idx]
        self.aav_scores = self.aav_scores[:self.PS]

    def update_scores(self):
        self.gsv_scores = []
        self.aav_scores = []
        for M in self.matrices:
            gsv, aav = self.score_matrix(M)
            self.gsv_scores.append(gsv)
            self.aav_scores.append(aav)

    def score_matrix(self, M):
        group_sizes = np.array([])
        group_age_variances = np.array([])
        for a in self.act:
            # group sizes
            mask = (M == a)
            group_sizes = np.append(group_sizes, sum(mask))
            # age variances
            act_ages = self.grades.copy()
            act_ages[~mask] = 0
            group_age_variances = np.append(
                group_age_variances, np.var(act_ages, axis=0))
        # log.debug("{}, {}".format(
        #     group_sizes.shape, group_age_variances.shape))

        # group size variance
        gsv = np.var(group_sizes)
        # average age variance
        aav = np.average(group_age_variances)
        # log.debug(
        #     "\ngsv: {:.2f}\n"
        #     "aav: {:.2f}\n".format(gsv, aav)
        # )
        return (gsv, aav)

    def init_population(self):
        # create a list of matrices,
        # [ p1: [a1, a5, a3]
        #   p2: [a2, a3, a5]
        #   p3: [a5, a3, a2] ]
        # col: day, row: user, an: activity for user pi on day j

        prefs = [x["pref"][:self.ND] for x in self.par]
        M = np.array(prefs)
        # log.debug(M.shape)
        # log.debug(M[0, :])
        self.matrices.append(M)
        for i in range(self.PS - 1):
            self.matrices.append(self.mutate(
                random.choice(self.matrices)))
        log.info("Initialized {} matrices".format(len(self.matrices)))

        # test: lines should be similar, sometimes mutated
        # line = 2
        # T = np.empty((len(self.matrices), self.matrices[0].shape[1]))
        # for i, m in enumerate(self.matrices):
        #   T[i, :] = m[line, :]
        # log.debug(T[:40, :])

        # Will need these two.
        self.grades = np.array([
            x["grade"] for x in self.par
        ])
        self.grades = np.tile(self.grades, (self.matrices[0].shape[1], 1)).T
        # log.debug(self.grades[:10])
        self.act = np.arange(
            np.min(self.matrices[0]), np.max(self.matrices[0]) + 1)

    def run(self):
        tstart = time()
        self.init_population()
        for i in range(self.NR):
            self.apply_crossovers()
            self.apply_mutations()
            self.culling()
            # self.sanity_check()

            # pick best
            bidx = np.argmin(self.gsv_scores)
            if self.gsv_scores[bidx] < self.best_gsv_score:
                self.best_gsv_score = self.gsv_scores[bidx]
                self.best_member = self.matrices[bidx].copy()

            log.info(
                "[{:>3}] gsv:{:.2f} aav:{:.2f}".format(
                    i,
                    np.average(self.gsv_scores),
                    np.average(self.aav_scores)
                )
            )
        log.info("Finished in {:.2f}s.".format(time() - tstart))
