from timetablenator.CsvReader import CsvReader
from timetablenator.GenAlg2 import GenAlg
# from timetablenator.BruteForce import BruteForce
import logging

logging.basicConfig(filename="./main.log", level=logging.DEBUG)
log = logging.getLogger(__name__)

if __name__ == "__main__":
    csvr = CsvReader(activities_col=2)
    csv_path = "../data/delavnice2018_kristjan.csv"
    participants, activities = csvr.read_csv(csv_path)

    # ga = GeneticAlg(participants, activities, ndays=4)
    # bf = BruteForce(participants, activities, ndays=4)
    # days = bf.run()

    good = (200, 200, 0.10, 0.20, 1, 0)
    args = good
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

    # write to csv and check in Excel... I know, I know
    write_path = "../data/urnik2018.csv"
    csvr.write_ga2_csv(ga2.best_member, participants, write_path)
