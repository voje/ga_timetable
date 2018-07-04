from timetablenator.CsvReader import CsvReader
from timetablenator.GeneticAlg import GeneticAlg
import logging

logging.basicConfig(filename="./main.log", level=logging.DEBUG)
log = logging.getLogger(__name__)

if __name__ == "__main__":
    csvr = CsvReader(activities_col=2)
    csv_path = "../data/delavnice2018_kristjan.csv"
    participants, activities = csvr.read_csv(csv_path)
    timet = GeneticAlg(participants, activities, ndays=4)
