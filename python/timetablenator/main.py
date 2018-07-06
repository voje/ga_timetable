from timetablenator.CsvReader import CsvReader
from timetablenator.GenAlg2 import GenAlg
# from timetablenator.BruteForce import BruteForce
import logging
from time import time

logging.basicConfig(filename="./main.log", level=logging.DEBUG)
log = logging.getLogger(__name__)


def try_ga2_runs(participants, test=None):
    tstart = time()
    log.info("Starting try_ga2_runs")
    test = test or False
    write_path = "../data/output"
    args_list = [
        (200, 200, 0.10, 0.20, 0.8, 0.2),
        # (200, 200, 0.10, 0.20, 0.5, 0.5), needs more focus on group sizes
        (100, 100, 0.50, 0.05, 0.8, 0.2),
        (200, 200, 0.50, 0.50, 0.8, 0.2),
    ]
    if test:
        args_list = [
            (20, 20, 0.10, 0.20, 0.8, 0.2),
        ]
    for i, args in enumerate(args_list):
        wp = "{}/ga2_{}_2018.csv".format(write_path, i)
        ga2 = GenAlg(
            participants, ndays=4,
            population_size=args[0],
            number_of_runs=args[1],
            mutation_rate=args[2],
            crossover_rate=args[3],
            group_size_weight=args[4],
            age_weight=args[5]
        )
        ga2.run()
        if test:
            continue
        csvr.write_ga2_csv(ga2.best_member, participants, wp)
    log.info("Finished try_ga2_runs in {:.2}s".format(
        time() - tstart))


if __name__ == "__main__":
    csvr = CsvReader(activities_col=2)
    csv_path = "../data/input/delavnice2018_kristjan.csv"
    participants, activities = csvr.read_csv(csv_path)

    """
    bf = BruteForce(participants, activities, ndays=4)
    bf.run()
    write_path = "../data/bf_urnik2018.csv"
    csvr.write_csv(bf.days, write_path)
    """

    try_ga2_runs(participants, test=False)
