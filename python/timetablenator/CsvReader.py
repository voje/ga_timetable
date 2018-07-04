#!/usr/bin/python
import csv
import logging
import re

re_fd = re.compile(r"\d")

log = logging.getLogger(__name__)


class CsvReader:
    def __init__(self, activities_col):
        # column of first activiti (del_1) start with 0: [0, 1, 2, 3 ...]
        self.ACTIVITIES_COL = activities_col

    def read_csv(self, path):
        log.info("Reading data from {}.".format(path))
        participants = []
        activities = []
        participant_id = 0
        with open(path, "r") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            for row in reader:
                if not row[0]:
                    # empty row
                    break
                # log.debug("Reading line: {}".format(row[0]))

                # first row
                if not activities:
                    for i, act_name in enumerate(row[self.ACTIVITIES_COL:]):
                        activities += [{
                            "name": act_name,
                            "id": int(re_fd.findall(act_name)[-1]) - 1,
                            "n_part": 0,
                        }]

                # second row, ...
                else:
                    par = {
                        "id": participant_id,
                        "name": str(row[0]),
                        "grade": int(row[1]),
                        "pref": [],  # activity ids by pref. order
                        "activities": [],  # output selected activities
                    }
                    participant_id += 1
                    for act_id in row[self.ACTIVITIES_COL:]:
                        par["pref"] += [int(act_id) - 1]
                    participants += [par]
        log.info(
            "Number of participants: {}.\n"
            "-- first: {}\n"
            "-- last: {}\n"
            "Number of activities: {}.".format(
                len(participants), participants[0]["name"],
                participants[-1]["name"], len(activities)
            )
        )
        log.warning(
            "All activity IDs have been decreased by 1, "
            "to fall in range [0, 1,.... N].")
        return (participants, activities)

    def write_csv(self, days, path):
        with open(path, "w") as f:
            for i in range(len(days)):
                for j in range(len(days[i])):
                    f.write("dan_{}-del_{},".format(i + 1, j + 1))
            row = 0
            keep_writing = True
            while keep_writing:
                keep_writing = False
                f.write("\n")
                for day in days:
                    for act in day:
                        if row < len(act["par"]):
                            keep_writing = True
                            participant = act["par"][row]
                            f.write("{}_{},".format(
                                participant["name"], participant["grade"]))
                        else:
                            f.write(",")
                row += 1


if __name__ == "__main__":
    r = CsvReader(activities_col=2)
    p, a = r.read_csv("../data/delavnice2018_kristjan.csv")

    for par in p:
        print(par)
    print(a)
