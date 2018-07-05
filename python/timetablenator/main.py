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

    good = (200, 50)
    test = (10, 10)
    # good = test
    ga2 = GenAlg(
        participants, ndays=4, population_size=good[0],
        mutation_rate=0.08, crossover_rate=0.1,
        number_of_runs=good[1]
    )
    ga2.run()

    # write to csv and check in Excel... I know, I know
    write_path = "../data/urnik2018.csv"
    csvr.write_ga2_csv(ga2.best_member, participants, write_path)
