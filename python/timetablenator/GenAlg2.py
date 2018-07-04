import numpy as np
import logging
import random

log = logging.getLogger(__name__)


class GenAlg:
    def __init__(
        self, par, ndays, population_size,
        mutation_rate, crossover_rate
    ):
        # see CsvReader for format of par
        self.par = par
        self.grades = None
        self.act = None
        self.ND = ndays
        self.PS = population_size
        self.MR = mutation_rate  # % of rows affected by mutate()
        self.CR = crossover_rate  # % of top members to crossover()
        # sort these together:
        self.matrices = []
        self.scores = []

    def mutate(self, M):
        M1 = M.copy()
        idxs = np.arange(M.shape[0])
        sample = np.random.choice(
            idxs, int(self.MR * M.shape[0]), replace=False)
        for i in sample:
            M1[i, :] = np.random.permutation(M1[i, :])
        return M1

    def crossover(self, M1, M2):
        return "TODO"

    def update_scores(self):
        self.scores = []
        for M in self.matrices:
            self.scores.append(self.score_matrix(M))
        idx = np.argsort(self.scores)  # ascending
        self.scores = [self.scores[i] for i in idx]
        self.matrices = [self.matrices[i] for i in idx]
        # leftmost matrix is the fittes (smallest variances)

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
        log.debug(
            "\ngsv: {:.2f}\n"
            "aav: {:.2f}\n".format(gsv, aav)
        )
        # TODO, normalize
        return (gsv + aav)

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
        log.info("Initialized {} matrices")

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
        self.init_population()
        self.update_scores()
