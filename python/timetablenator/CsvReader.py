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
                            "id": re_fd.findall(act_name)[-1],
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
                        par["pref"] += [int(act_id)]
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
        return (participants, activities)


if __name__ == "__main__":
    r = CsvReader(activities_col=2)
    p, a = r.read_csv("../data/delavnice2018_kristjan.csv")

    for par in p:
        print(par)
    print(a)